---
title: API and plugins
weight: 40
---

monbooru has a REST API under `/api/v1/`, which is what monloader,
plugins and your own scripts use. The full endpoint reference comes
with the app and always matches the version you run:

- `/api/v1/docs` for the HTML reference (also linked in the footer),
- `/api/v1/openapi.json` for the OpenAPI spec.

This page covers what that reference doesn't: tokens, calling it from
a browser, and writing a plugin.

## Tokens

The API stays off until you create a token under
**Settings -> Authentication**. Each token has a name, can be revoked
on its own, and carries the permissions you give it:

- `read`: every `GET` (search, fetch, tags...)
- `write`: `POST` and `PATCH` (upload, edit, tag, relate...)
- `delete`: `DELETE`

The secret is shown once, when you create it. Send it as a bearer
token:

```bash
curl -H "Authorization: Bearer <token>" \
     "http://localhost:8455/api/v1/images/search?q=1girl"
```

The errors you're most likely to meet: `401 unauthorized` for a
missing or wrong token, `403 insufficient_scope` when the token lacks
the permission, and `503 api_disabled` when no token exists yet.

Requests go to the active gallery. Add `?gallery=<name>` or an
`X-Monbooru-Gallery` header to talk to another one.

Tokens for monloader and plugins are made by
[pairing](../addons/pairing.md) rather than by hand.

## Calling it from a web page

A page monbooru serves can call the API right away. A page served from
anywhere else, like your own tool on another port or a browser
extension, is blocked by the browser until you add its address to
`server.cors_origins` in [the config file](configuration.md), for
example `http://192.168.1.50:5173`. `*` allows any page. Scripts, curl
and monloader aren't browsers and don't need this. `/api/v1/docs`
shows the addresses currently allowed.

## Writing a plugin

A [plugin](../addons/plugins.md) is an HTTP service that pairs with
monbooru and gets a few buttons in its interface. It can be written in
anything. It needs at most three things:

- `GET /health` answering 200. monbooru checks it before approving the
  pairing and to decide whether to show your buttons. Answer
  `{"version": "..."}` and your version shows on the settings row.
- If you declared relay buttons, a handler for the relay `POST`. It
  receives `{payload, monbooru, gallery, slot, button, image_ids}`
  with your token as a bearer header, and answers
  `{"ok": true, "message": "...", "refresh": true}`. monbooru waits up
  to 10 seconds for the answer.
- If you declared open buttons, the pages they point at. monbooru
  serves them through itself under `/plugins/<name>/`, so use relative
  links inside them.

Buttons go in one of two slots, `detail-actions` (an image's page) or
`batch-bar` (under the gallery's batch bar, relay only). A button's
`path` can use `{image_id}`, `{gallery}` and `{back_url}`. Give a
button `media` when it doesn't handle everything: any of `image`,
`archive` and `animated`, comma-separated. monbooru then hides it on
other files and leaves them out of a batch.

Everything else goes through the REST API with the token you're
issued. Pairing is a few calls: `POST /api/v1/pair/request` with your
name, address, the permissions you need and your buttons, then poll
`/api/v1/pair/status` until the user approves, and keep the token it
returns. Ask for `read` and `write`, and for `delete` only if your
plugin really deletes images. Changing your buttons in a later release
means offering again: the user approves a request marked **re-pair**.

To ship it as a folder people drop into `plugins/`, add a
`plugin.toml` with the launch line, `command = "./yourplugin"` (and
`command_windows` if Windows needs another one). monbooru starts it
with the folder as working directory and `MONBOORU_URL` in its
environment, and stops it by closing its stdin, so exit when stdin
closes. monbooru installs nothing, so ship a self-contained program.

What monbooru keeps stable for plugins: the `/api/v1` API, the pairing
exchange, the relay message, the button slots and variables, the
`/plugins/<name>/` mount, and the theme variables. Templates,
`/internal/` URLs and the database are not part of that and can
change in any release.

[`examples/simple-edit`](https://github.com/monbooru/monbooru-plugins/tree/main/examples/simple-edit)
in the plugins registry is a working plugin to copy: it pairs, rotates
images from a relay button, and serves a crop page behind an open
button.
