---
title: Troubleshooting
weight: 90
---

## The connection dot

The popup and the options page show a dot for the link to monloader:

- **green (connected)**: all good.
- **red (unreachable)**: nothing answers at the URL in
  [settings](settings/index.md). Check that monloader is running, and
  open the URL in a tab to make sure your browser can reach it.
- **amber (token rejected)** or **amber (not paired yet)**: monloader
  answers but doesn't accept the extension. That happens before the
  first pairing, after you change the URL, after the pairing was
  removed, or after monloader was reinstalled. Click **connect to
  monloader** in the options and approve the request in monloader
  under **Settings -> Pairing**.
- **amber (setup not finished)**: monloader answers but its first-run
  setup isn't done. Finish the setup page in monloader.

## An image is missing from a scan

The chooser only lists what monbooru can store (see [What the chooser
lists](guides/scanning/index.md#what-the-chooser-lists)), so an SVG
logo, a HEIC photo or an MKV clip is left out. Small images are left
out too; see **min image size** in [settings](settings/index.md).

A page the browser doesn't let extensions read, like the add-on store,
a browser settings page or the PDF viewer, says "this page cannot be
scanned".
