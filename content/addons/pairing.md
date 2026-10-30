---
title: Pairing
weight: 20
---

The apps talk to each other through their APIs, and each needs a key
to get in. Pairing sets those keys up for you, so you never copy one
between settings pages: one app asks, you approve in the other, and
they exchange keys that allow only what each needs.

There are two links:

- **monloader and monbooru.** In monloader, **Settings -> Pairing ->
  Connect to monbooru** sends the request, and you approve it in
  monbooru under **Settings -> Plugins**. monloader can then add
  images and tags to monbooru and update them (it can't delete any),
  and monbooru can ask monloader for lookups.
- **monsender and monloader.** In the extension's options, **connect
  to monloader** sends the request, and you approve it in monloader
  under **Settings -> Pairing**. The extension can then add URLs to
  monloader's queue.

[Plugins](plugins.md) pair with monbooru the same way and show up in
the same list.

## Good to know

- You approve a pairing once and it stays. Removing it on either side
  withdraws the keys on both.
- A request waits a few minutes for you to approve it, and doesn't
  survive a restart of the app it's waiting on. If it runs out, just
  connect again.
- If a link stops working, press **Reconnect** in monloader and
  approve the new request; the old pairing keeps working until you
  do. For the extension, remove its old pairing in monloader first,
  then click **connect to monloader** again.

Step by step: [monloader pairing](monloader/getting-started/pairing/index.md),
[monsender setup](monsender/getting-started/setup/index.md). For
scripts of your own, see [API and plugins](../advanced/api.md) and
[monloader's API](monloader/development.md).
