#!/usr/bin/env python3
"""Keeps the monbooru project board in step with the issues.

Adds the open issues and pull requests of the three apps, puts each card
in the column its labels, milestone and pull requests call for, and takes
off what is closed without shipping. Nothing on the board is set by hand.
"""
import argparse
import datetime
import json
import os
import re
import sys
import urllib.request

ORG = "monbooru"
REPOS = ("monbooru", "monloader", "monsender")
COLUMNS = ("Proposed", "Accepted", "Help wanted", "In review",
           "Ready for dev", "Ready for main", "Released")
KEEP = datetime.timedelta(days=14)

ISSUE = """
fragment I on Issue {
  id number state stateReason closedAt
  repository { name owner { login } }
  labels(first: 30) { nodes { name } }
  milestone { title }
}"""
PULL = """
fragment P on PullRequest {
  id number pullState: state mergedAt closedAt body
  repository { name owner { login } }
  labels(first: 30) { nodes { name } }
  closingIssuesReferences(first: 10) { nodes { number repository { name owner { login } } } }
}"""
PAGE = "pageInfo { hasNextPage endCursor }"
REPO_QUERIES = {
    "open issues": ("issues(first: 100, after: $after, states: OPEN) { %s nodes { ...I } }" % PAGE, ISSUE, None),
    "closed issues": ("issues(first: 100, after: $after, states: CLOSED, filterBy: {since: \"SINCE\"}) { %s nodes { ...I } }" % PAGE, ISSUE, None),
    "open pulls": ("pullRequests(first: 100, after: $after, states: OPEN) { %s nodes { ...P } }" % PAGE, PULL, None),
    "closed pulls": ("pullRequests(first: 100, after: $after, states: [CLOSED, MERGED], orderBy: {field: UPDATED_AT, direction: DESC}) { %s nodes { ...P } }" % PAGE, PULL, 1),
}
ITEMS = """
query($org: String!, $number: Int!, $after: String) {
  organization(login: $org) { projectV2(number: $number) {
    items(first: 100, after: $after) { %s nodes {
      id isArchived
      fieldValueByName(name: "Status") { ... on ProjectV2ItemFieldSingleSelectValue { name } }
      content { __typename ...I ...P }
    } }
  } }
}""" % PAGE + ISSUE + PULL
PROJECT = """
query($org: String!, $number: Int!) {
  organization(login: $org) { projectV2(number: $number) {
    id
    field(name: "Status") { ... on ProjectV2SingleSelectField { id options { id name } } }
  } }
}"""


def when(text):
    return datetime.datetime.fromisoformat(text.replace("Z", "+00:00")) if text else None


def card(node):
    repo = node["repository"]
    pull = "mergedAt" in node
    out = {
        "id": node["id"],
        "pull": pull,
        "repo": repo["name"] if repo["owner"]["login"] == ORG else None,
        "number": node["number"],
        "open": (node["pullState"] if pull else node["state"]) == "OPEN",
        "labels": {l["name"] for l in node["labels"]["nodes"]},
        "ended": when(node.get("mergedAt") or node.get("closedAt")),
    }
    if pull:
        out["merged"] = node["pullState"] == "MERGED"
        named = [int(n) for line in re.findall(r"(?mi)^Issue:(.*)$", node.get("body") or "")
                 for n in re.findall(r"(?:#|/issues/)(\d+)", line)]
        linked = [r["number"] for r in node["closingIssuesReferences"]["nodes"]
                  if r["repository"]["name"] == repo["name"] and r["repository"]["owner"]["login"] == ORG]
        out["issues"] = linked or named
    else:
        out["completed"] = node.get("stateReason") == "COMPLETED"
        out["milestone"] = (node.get("milestone") or {}).get("title")
    return out


def columns(cards, released, now):
    """The column of every card, None for one that is not on the board.

    released maps a repo to the date of its newest release, or None.
    """
    issues = {(c["repo"], c["number"]): c for c in cards if not c["pull"]}
    pulls = {}
    for c in cards:
        if c["pull"]:
            c["issues"] = [n for n in c["issues"] if (c["repo"], n) in issues]
            for n in c["issues"]:
                pulls.setdefault((c["repo"], n), []).append(c)

    def shipped(c):
        return not c["open"] and (c["merged"] or "reimplemented" in c["labels"])

    def waits(c):
        last = released.get(c["repo"])
        return last is None or c["ended"] > last

    def column(c):
        labels = c["labels"]
        if labels & {"declined", "duplicate"}:
            return None
        recent = c["ended"] is not None and now - c["ended"] < KEEP
        if c["pull"]:
            if c["issues"]:
                return None
            if c["open"]:
                return "Ready for dev" if "ready for dev" in labels else "In review"
            if not shipped(c):
                return None
            if waits(c):
                return "Ready for main"
            return "Released" if recent else None
        if not c["open"]:
            return "Released" if c["completed"] and c["milestone"] and recent else None
        if "ready for main" in labels:
            return "Ready for main"
        mine = pulls.get((c["repo"], c["number"]), [])
        live = [p for p in mine if p["open"]]
        done = [p for p in mine if shipped(p)]
        if done and not live and any(waits(p) for p in done):
            return "Ready for main"
        if "ready for dev" in labels:
            return "Ready for dev"
        if live:
            return "In review"
        if "postponed" in labels:
            return "Accepted"
        if "help wanted" in labels:
            return "Help wanted"
        if "accepted" in labels:
            return "Accepted"
        return "Proposed"

    return {c["id"]: column(c) for c in cards if c["repo"] in REPOS}


def plan(cards, wanted, board):
    """The changes to make, as (add, move or archive, card, column).

    board maps a card id to (item id, column, archived) for what the project holds.
    """
    steps = []
    for c in cards:
        if c["id"] not in wanted:
            continue
        want = wanted[c["id"]]
        item = board.get(c["id"])
        here = item is not None and not item[2]
        if want is None:
            if here:
                steps.append(("archive", c, None))
        elif not here:
            steps.append(("add", c, want))
        elif item[1] != want:
            steps.append(("move", c, want))
    return steps


class GitHub:
    def __init__(self, token):
        self.token = token

    def query(self, text, **variables):
        request = urllib.request.Request(
            "https://api.github.com/graphql",
            data=json.dumps({"query": text, "variables": variables}).encode(),
            headers={"Authorization": "Bearer " + self.token, "User-Agent": "monbooru-board"},
        )
        with urllib.request.urlopen(request, timeout=60) as answer:
            body = json.load(answer)
        if body.get("errors"):
            raise SystemExit("GitHub refused a query: " + json.dumps(body["errors"]))
        return body["data"]

    def pages(self, text, path, limit=None, **variables):
        after = None
        while True:
            data = self.query(text, after=after, **variables)
            for key in path:
                data = data[key]
            yield from data["nodes"]
            if limit is not None:
                limit -= 1
            if not data["pageInfo"]["hasNextPage"] or limit == 0:
                return
            after = data["pageInfo"]["endCursor"]


def read(github, number, now):
    project = github.query(PROJECT, org=ORG, number=number)["organization"]["projectV2"]
    if project is None:
        raise SystemExit("no project %d on %s, or the token cannot read it" % (number, ORG))
    options = {o["name"]: o["id"] for o in (project["field"] or {}).get("options", [])}
    missing = [name for name in COLUMNS if name not in options]
    if missing:
        raise SystemExit("the Status field lacks: " + ", ".join(missing))

    cards, board, released = {}, {}, {}
    for item in github.pages(ITEMS, ("organization", "projectV2", "items"), org=ORG, number=number):
        content = item["content"]
        if not content or content["__typename"] not in ("Issue", "PullRequest"):
            continue
        cards[content["id"]] = card(content)
        board[content["id"]] = (item["id"], (item["fieldValueByName"] or {}).get("name"), item["isArchived"])

    since = (now - KEEP).strftime("%Y-%m-%dT%H:%M:%SZ")
    for repo in REPOS:
        latest = github.query(
            "query($org: String!, $repo: String!) { repository(owner: $org, name: $repo) { latestRelease { publishedAt } } }",
            org=ORG, repo=repo)["repository"]["latestRelease"]
        released[repo] = when(latest["publishedAt"]) if latest else None
        for body, fragment, limit in REPO_QUERIES.values():
            text = ("query($org: String!, $repo: String!, $after: String) "
                    "{ repository(owner: $org, name: $repo) { %s } }" % body.replace("SINCE", since)) + fragment
            name = body.split("(")[0]
            for node in github.pages(text, ("repository", name), limit, org=ORG, repo=repo):
                cards[node["id"]] = card(node)
    return project["id"], project["field"]["id"], options, list(cards.values()), board, released


def apply(github, project, field, options, steps):
    for verb, c, want in steps:
        if verb == "archive":
            github.query(
                "mutation($project: ID!, $item: ID!) { archiveProjectV2Item(input: {projectId: $project, itemId: $item}) { item { id } } }",
                project=project, item=c["item"])
            continue
        item = c.get("item")
        if verb == "add":
            added = github.query(
                "mutation($project: ID!, $content: ID!) { addProjectV2ItemById(input: {projectId: $project, contentId: $content}) { item { id isArchived } } }",
                project=project, content=c["id"])["addProjectV2ItemById"]["item"]
            item = added["id"]
            if added["isArchived"]:
                github.query(
                    "mutation($project: ID!, $item: ID!) { unarchiveProjectV2Item(input: {projectId: $project, itemId: $item}) { item { id } } }",
                    project=project, item=item)
        github.query(
            "mutation($project: ID!, $item: ID!, $field: ID!, $option: String!) { updateProjectV2ItemFieldValue(input: "
            "{projectId: $project, itemId: $item, fieldId: $field, value: {singleSelectOptionId: $option}}) { projectV2Item { id } } }",
            project=project, item=item, field=field, option=options[want])


def report(cards, wanted, steps):
    name = lambda c: "%s%s#%d" % ("" if c["repo"] == REPOS[0] else c["repo"], " PR " if c["pull"] else "", c["number"])
    lines = []
    for repo in REPOS:
        counts = [(col, sum(1 for c in cards if c["repo"] == repo and wanted.get(c["id"]) == col)) for col in COLUMNS]
        lines.append(repo + ": " + (", ".join("%s %d" % pair for pair in counts if pair[1]) or "no card"))
    for verb in ("add", "move", "archive"):
        done = [name(c).strip() + (" to " + want if verb == "move" else "") for v, c, want in steps if v == verb]
        if done:
            lines.append("%s %d: %s" % (verb, len(done), ", ".join(done[:60]) + (" ..." if len(done) > 60 else "")))
    if not steps:
        lines.append("nothing to change")
    return lines


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--project", type=int, required=True, help="the number in the project's address")
    parser.add_argument("--dry-run", action="store_true", help="say what would change, change nothing")
    args = parser.parse_args()
    token = os.environ.get("PROJECT_TOKEN")
    if not token:
        raise SystemExit("PROJECT_TOKEN is not set")

    github = GitHub(token)
    now = datetime.datetime.now(datetime.timezone.utc)
    project, field, options, cards, board, released = read(github, args.project, now)
    wanted = columns(cards, released, now)
    for c in cards:
        if c["id"] in board:
            c["item"] = board[c["id"]][0]
    steps = plan(cards, wanted, board)
    lines = report(cards, wanted, steps)
    if args.dry_run:
        lines.insert(0, "dry run, nothing changed")
    else:
        apply(github, project, field, options, steps)
    print("\n".join(lines))
    if os.environ.get("GITHUB_ACTIONS"):
        print("::notice title=Board::" + "%0A".join(lines))
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as summary:
            summary.write("\n".join("- " + line for line in lines) + "\n")


if __name__ == "__main__":
    sys.exit(main())
