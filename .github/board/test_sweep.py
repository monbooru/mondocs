import datetime
import unittest

import sweep

NOW = datetime.datetime(2026, 11, 15, tzinfo=datetime.timezone.utc)
RELEASE = NOW - datetime.timedelta(days=6)
BEFORE = RELEASE - datetime.timedelta(days=1)
AFTER = RELEASE + datetime.timedelta(days=1)
OLD = NOW - datetime.timedelta(days=40)


def issue(number, *labels, closed=None, completed=True, milestone=None, repo="monbooru"):
    return {"id": "I%s%d" % (repo, number), "pull": False, "repo": repo, "number": number,
            "open": closed is None, "labels": set(labels), "ended": closed,
            "completed": closed is not None and completed, "milestone": milestone}


def pull(number, *labels, issues=(), merged=None, closed=None, repo="monbooru"):
    return {"id": "P%s%d" % (repo, number), "pull": True, "repo": repo, "number": number,
            "open": merged is None and closed is None, "labels": set(labels),
            "ended": merged or closed, "merged": merged is not None, "issues": list(issues)}


def column(card, *others):
    return sweep.columns([card, *others], {"monbooru": RELEASE, "monloader": None}, NOW)[card["id"]]


class OpenIssue(unittest.TestCase):
    def test_labels_in_order(self):
        self.assertEqual(column(issue(1)), "Proposed")
        self.assertEqual(column(issue(1, "needs info")), "Proposed")
        self.assertEqual(column(issue(1, "accepted")), "Accepted")
        self.assertEqual(column(issue(1, "accepted", "help wanted")), "Help wanted")
        self.assertEqual(column(issue(1, "accepted", "help wanted", "postponed")), "Accepted")
        self.assertEqual(column(issue(1, "accepted", "ready for dev")), "Ready for dev")
        self.assertEqual(column(issue(1, "accepted", "ready for dev", "ready for main")), "Ready for main")

    def test_declined_or_duplicate_is_off(self):
        self.assertIsNone(column(issue(1, "accepted", "declined")))
        self.assertIsNone(column(issue(1, "duplicate")))

    def test_open_pull_request_puts_it_in_review(self):
        self.assertEqual(column(issue(1, "accepted", "help wanted"), pull(2, issues=[1])), "In review")
        self.assertEqual(column(issue(1, "ready for dev"), pull(2, issues=[1])), "Ready for dev")

    def test_merged_pull_request_puts_it_on_ready_for_main(self):
        self.assertEqual(column(issue(1, "accepted"), pull(2, issues=[1], merged=AFTER)), "Ready for main")
        self.assertEqual(column(issue(1, "accepted"), pull(2, "reimplemented", issues=[1], closed=AFTER)), "Ready for main")

    def test_a_second_open_pull_request_keeps_it_in_review(self):
        self.assertEqual(column(issue(1), pull(2, issues=[1], merged=AFTER), pull(3, issues=[1])), "In review")

    def test_merge_before_the_release_leaves_it_to_the_labels(self):
        self.assertEqual(column(issue(1, "accepted"), pull(2, issues=[1], merged=BEFORE)), "Accepted")

    def test_abandoned_pull_request_leaves_it_to_the_labels(self):
        self.assertEqual(column(issue(1, "help wanted"), pull(2, issues=[1], closed=AFTER)), "Help wanted")

    def test_pull_request_of_another_repo_does_not_count(self):
        self.assertEqual(column(issue(1), pull(2, issues=[1], repo="monloader")), "Proposed")


class ClosedIssue(unittest.TestCase):
    def test_shipped_shows_two_weeks(self):
        self.assertEqual(column(issue(1, closed=AFTER, milestone="v1")), "Released")
        self.assertIsNone(column(issue(1, closed=OLD, milestone="v1")))

    def test_without_milestone_or_not_completed_is_off(self):
        self.assertIsNone(column(issue(1, closed=AFTER)))
        self.assertIsNone(column(issue(1, closed=AFTER, completed=False, milestone="v1")))


class PullRequest(unittest.TestCase):
    def test_with_an_issue_has_no_card(self):
        self.assertIsNone(column(pull(2, issues=[1]), issue(1)))
        self.assertIsNone(column(pull(2, issues=[1], merged=AFTER), issue(1)))

    def test_issue_the_board_does_not_know_makes_it_an_orphan(self):
        self.assertEqual(column(pull(2, issues=[9])), "In review")

    def test_orphan_open(self):
        self.assertEqual(column(pull(2)), "In review")
        self.assertEqual(column(pull(2, "ready for dev")), "Ready for dev")
        self.assertIsNone(column(pull(2, "declined")))

    def test_orphan_merged_waits_for_the_release(self):
        self.assertEqual(column(pull(2, merged=AFTER)), "Ready for main")
        self.assertEqual(column(pull(2, merged=BEFORE)), "Released")
        self.assertIsNone(column(pull(2, merged=OLD)))
        self.assertEqual(column(pull(2, merged=OLD, repo="monloader")), "Ready for main")

    def test_orphan_closed(self):
        self.assertIsNone(column(pull(2, closed=AFTER)))
        self.assertEqual(column(pull(2, "reimplemented", closed=AFTER)), "Ready for main")


class Plan(unittest.TestCase):
    def test_add_move_archive(self):
        a, b, c, d, e = issue(1), issue(2, "accepted"), issue(3, "declined"), issue(4), issue(5, "duplicate")
        cards = [a, b, c, d, e]
        wanted = sweep.columns(cards, {}, NOW)
        board = {b["id"]: ("x", "Proposed", False), c["id"]: ("y", "Proposed", False),
                 d["id"]: ("z", "Proposed", False), e["id"]: ("w", "Proposed", True)}
        self.assertEqual(sweep.plan(cards, wanted, board),
                         [("add", a, "Proposed"), ("move", b, "Accepted"), ("archive", c, None)])

    def test_archived_card_wanted_again_is_added(self):
        a = issue(1)
        self.assertEqual(sweep.plan([a], {a["id"]: "Proposed"}, {a["id"]: ("x", "Proposed", True)}),
                         [("add", a, "Proposed")])

    def test_card_of_another_repo_is_left_alone(self):
        a = issue(1, repo="mondocs")
        self.assertEqual(sweep.plan([a], sweep.columns([a], {}, NOW), {a["id"]: ("x", None, False)}), [])


class Card(unittest.TestCase):
    def node(self, body, linked=()):
        repo = {"name": "monbooru", "owner": {"login": "monbooru"}}
        return {"id": "P", "number": 2, "pullState": "OPEN", "mergedAt": None, "closedAt": None, "body": body,
                "repository": repo, "labels": {"nodes": []},
                "closingIssuesReferences": {"nodes": [{"number": n, "repository": repo} for n in linked]}}

    def test_issue_line(self):
        self.assertEqual(sweep.card(self.node("What:\nsee #7\n\nIssue: #178\n"))["issues"], [178])
        self.assertEqual(sweep.card(self.node("Issue: https://github.com/monbooru/monbooru/issues/12 and #13"))["issues"], [12, 13])
        self.assertEqual(sweep.card(self.node("Issue:\n\nfixes #7"))["issues"], [])
        self.assertEqual(sweep.card(self.node(None))["issues"], [])

    def test_link_wins_over_the_line(self):
        self.assertEqual(sweep.card(self.node("Issue: #1", linked=[5]))["issues"], [5])


if __name__ == "__main__":
    unittest.main()
