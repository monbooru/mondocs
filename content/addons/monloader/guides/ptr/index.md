---
title: Hydrus PTR
weight: 50
---

The [Hydrus Public Tag Repository](https://hydrusnetwork.github.io/hydrus/PTR.html)
(PTR) is a huge shared database of tags, built by Hydrus users over
many years: billions of tags for files identified by their hash.
monloader can keep a local copy and use it to tag your images from the
file alone, including files that were deleted from the boorus or never
posted there. It's off until you turn it on.

## What it costs

The PTR can't be asked about a single file (on purpose, so its server
never learns what files you have). Using it means downloading the
whole thing once and keeping it up to date:

- **Disk**: the local copy needs more than 70 GB, on a volume of its
  own. Put it on an SSD; building it on a spinning disk can take
  weeks.
- **Time**: the first sync takes days. You can pause and resume it
  whenever you like.
- **After that**: one small update a day or so.

The copy can be deleted and downloaded again at any time; it's all
public data. To skip most of the first sync, start from a snapshot
(below).

## Turning it on

![The PTR page before enabling](ptr-disabled.png)

1. Give the copy a place to live. A desktop install already has a
   `ptr` folder next to its data; on Docker, mount a volume at `/ptr`
   (the compose file has a commented example). The **data path** in
   **Settings -> ptr** can point anywhere with enough room; on the
   Flatpak, grant access to a folder outside its sandbox first with.
2. Open **PTR** in the top bar, check the free space, and click
   **enable ptr sync**.

Unticking **enable sync and answer sha256 lookups** in **Settings ->
ptr** turns it off and keeps the copy; **delete ptr data** frees the
disk.

![The PTR page once the index has caught up](ptr-synced.png)

## Starting from a snapshot

A snapshot is a ready-made copy you can download instead of syncing
from scratch. monloader then only fetches the days since it was made.

1. Download the latest `ptr-snapshot-<date>.sqlite.zst` (about 22 GB)
   from the [Hydrus PTR tag mappings dataset](https://huggingface.co/datasets/Leqwin/hydrus-ptr-tag-mappings)
   on Hugging Face. Its `SHA256SUMS` file lets you check the download.
2. Unpack it with `zstd -d ptr-snapshot-<date>.sqlite.zst`. It grows to
   about 68 GB.
3. With monloader stopped, put it in the PTR folder as `ptr.sqlite`
   (on Docker, owned by uid 1000: `chown 1000:1000 ptr.sqlite`).
4. Start monloader and enable the PTR. It catches up the missing days
   and is ready.

## Using it

The PTR answers only once the copy has caught up: a half-built copy
would give a few of a file's tags as if they were all of them. After
that, **pause** on the PTR page stops the downloads.

From then on, monbooru can use it to
[look up images](../../../../guides/lookup/index.md) and to find
aliases and implications for your tags. Tags come back in monbooru's
form: hydrus namespaces become categories (`creator:` is artist,
`series:` is copyright...), and bookkeeping namespaces like `title:`
or `filename:` are left out.

## Contributing back

With a personal PTR account, you can also give back the tags you
curate yourself, from monbooru (see
[Contributing to the PTR](../../../../guides/ptr-contributions/index.md)).

Create the account from the **account** card on the PTR page. It's
anonymous, and volunteers (janitors) review what you send. The account
is its key: lose the key and you lose the account, so use the card's
button to reveal it and keep a copy somewhere safe. The
**contributions** card keeps a record of what you sent, and anything
that failed on the way can be retried from there.
