---
title: Pairing
weight: 20
---

The apps talk to each other through their APIs, and each needs a key
to get in. Pairing sets those keys up for you, so you never copy one
between settings pages: one app asks, you approve in the other, and
they exchange keys that allow only what each needs.

There are two links:

- monloader and monbooru: monloader asks, you approve in monbooru.
  monloader can then add images and tags to monbooru and update them
  (it can't delete any), and monbooru can ask monloader for lookups.
  [Step by step](monloader/getting-started/pairing/index.md).
- monsender and monloader: the extension asks, you approve in
  monloader. The extension can then add URLs to monloader's queue.
  [Step by step](monsender/getting-started/setup/index.md).

[Plugins](plugins.md) pair with monbooru the same way and show up in
the same list.

## Good to know

- You approve a pairing once and it stays. Removing it on either side
  withdraws the keys on both.
- A request waits a few minutes for your approval. If it runs out,
  connect again.
- If a link stops working, press **Pair again** in monloader and
  approve the new request; the old pairing keeps working until you
  do. For the extension, click **connect to monloader** again. If
  monloader still lists the old pairing under **Settings -> Pairing**,
  remove it there first.

For scripts of your own, see [API and plugins](../advanced/api.md) and
[monloader's API](monloader/development.md).
