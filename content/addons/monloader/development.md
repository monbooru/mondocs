---
title: API and development
weight: 90
---

## API tokens

monloader's API lives under `/api/v1/`. It stays off until you create
a token under **Settings -> Authentication**. Each token has a name,
can be revoked on its own, and its secret is shown once. Its
permissions are `read` (see the queue, jobs and sites) and `write` (add
URLs, manage jobs); a call it isn't allowed to make gets
`403 insufficient_scope`. Tokens made by [pairing](../pairing.md) are
managed by removing the pairing.

```bash
curl -H "Authorization: Bearer <token>" \
     -X POST http://localhost:8456/api/v1/queue \
     -d '{"url":"https://danbooru.donmai.us/posts/123"}'
```

The full reference comes with the app: `/api/v1/docs` (also linked in
the footer) and `/api/v1/openapi.json`. Both, and `/health`, work
without a token.

## Error codes

A failed item carries one of these codes, which scripts and monsender
can rely on:

| Code | Meaning |
|---|---|
| `unsupported_url` | gallery-dl doesn't know the URL, and it isn't a direct link to a file monbooru takes |
| `auth_required` | the site wants credentials |
| `blocked` | a Cloudflare or captcha wall |
| `rate_limited` | the site said to slow down |
| `network_unreachable` | the site's host couldn't be found or reached |
| `download_failed` | gallery-dl failed for another reason |
| `mapping_failed` | the post had no usable file |
| `file_too_large` | monbooru refused the file for its size |
| `monbooru_unreachable` | monbooru didn't answer |
| `monbooru_rejected` | monbooru answered with an error |
| `hash_mismatch` | the file fetched doesn't match the one expected |
| `hash_not_found` | no source in the lookup chain has the file |
| `ptr_unavailable` | a PTR lookup while the PTR is off |
| `ptr_syncing` | a PTR lookup while the PTR is still syncing |
| `ptr_account_required` | a PTR contribution without a working account |
| `ptr_banned` | the PTR account is banned |
| `already_exists` | an upgrade's file is already in the gallery as another image |
| `wrong_type` | an upgrade aimed at an archive or a video |
| `canceled` | the job was canceled mid-way |

What the outcomes mean is on [Downloading](guides/downloading/index.md#per-item-outcomes).

## Building from source

monloader is plain Go, with no cgo:

```bash
make build      # injects the version from VERSION.md
# or:
go build -o monloader ./cmd/monloader

./monloader -config /path/to/monloader.toml
```

A plain `go build` reports its version as `dev`. It needs gallery-dl
to download anything: put it on the `PATH` or set
`gallerydl.binary_path`. Without it the UI still runs and downloads
fail until it's there.

Command-line flags:

- `-config <path>`: the config file (default `./monloader.toml`).
- `-hash-password <password>`: print a password hash and exit.
- `-desktop`: the desktop profile (OS folders or a portable folder, a
  log file, a browser at startup, the setup page); every download has
  it on.
- `-no-browser`: with `-desktop`, don't open a browser.
- `-version`: print the version and exit.
- `healthcheck`: probe the local `/health` endpoint and exit non-zero
  when it doesn't answer.

## Site profiles

How monloader reads a site is data, not code: each known site has a
profile, a small JSON file. The profile tab of a site's dialog
([Metadata mapping](guides/mapping/index.md#editing-a-sites-profile))
writes yours to `profiles/<site>.json` next to the config, on top of
the shipped one. The shipped profiles are the same files, in
`internal/mapping/profiles/`, so contributing a fix or a new site is a
pull request adding your file there. The **export** tab of the site's
dialog gives you the file, without your credentials.

| Field | Purpose |
|---|---|
| `family` | `danbooru`, `e621`, `moebooru`, `gelbooru_v02`, `philomena` or `generic`: how ratings and tag categories are read |
| `kind` | `booru` (the default), `manga` (galleries become one cbz), or `other` |
| `post_url_template` | the post page, with `{id}` |
| `md5_search_template` | the hash search URL, with `{md5}`; makes the site usable for lookups |
| `auth` | `none`, `api_optional`, `api_required`, `username_password`, `cookies` or `oauth` |
| `hosts` | other hosts that belong to the site (file CDNs, mirrors) |
| `example` | a sample URL for the site's test button |
| `category_overrides` | tag category remaps |
| `rating_overrides` | rating value remaps |
| `default_rating` | the rating when the site gives none |
| `needs_tags` | for a generic site: ask gallery-dl for per-category tags (one more request per post) |
| `has_notes` | for a generic site: ask gallery-dl for note boxes |
| `options` | gallery-dl options for the site; shared, so never secrets |
| `tag_rules` | per-tag fixes: `""` drops the tag, a name renames it, `category:name` moves it |
