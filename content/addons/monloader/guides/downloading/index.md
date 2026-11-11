---
title: Downloading
weight: 10
---

Paste a URL into the add bar and press Enter: a single post, a pool, a
tag search, an artist page, a manga, or a direct link to an image.
Anything gallery-dl understands works. You can also send pages
straight from your browser with the
[monsender extension](../../../monsender/guides/sending.md).

![The queue with a re-submitted post, a capped tag search, and a pool](queue.webp)

Each URL becomes a job on the queue. monloader works out which posts
it covers, downloads each one, [translates its tags](../mapping/index.md)
for monbooru and sends it to your gallery. Once monbooru has the file,
monloader deletes its own copy; it keeps nothing.

## Per-item outcomes

Every post in a job ends with one of these:

| Outcome | Means |
|---|---|
| `created` | a new image in monbooru |
| `duplicate` | monbooru already had this file; any new tags were added to it |
| `enriched` | a lookup or refresh added tags to an image monbooru already had |
| `matched` | a PTR lookup found the image's tags, and monbooru applied them |
| `replaced` | an [upgrade](../../../../guides/lookup/index.md#running-lookups-from-monbooru) swapped in a better file |
| already fetched (`skipped_archive`) | downloaded before, so not again |
| file type not supported (`skipped_unsupported`) | a file type monbooru doesn't take (audio, a document...) |
| blacklisted (`skipped_blacklist`) | it matched one of your blacklist rules, named beside it |
| `failed` | something went wrong; the row says what |

A failed item says why in plain words, and hovering it shows the error
code; the codes are listed in
[API and development](../../development.md#error-codes).

If a search comes back shorter than the site shows, the missing posts
probably need a login: [add yours](../sites/index.md).

## Skipping posts by tag

You can skip posts that contain certain tags. List their tags under
**Blacklist** in **Settings -> Rules**, one rule per line:
`guro` skips any post carrying that tag, `furry -rating:general` skips furry
posts unless they're rated general, and
`*_(cosplay)` uses a wildcard. A list for just one site should go on the site's
**tags** tab.

## Big searches

A tag search or an artist page can run to thousands of posts, so a job
takes at most 200 of them by default (**Settings -> Downloads**). To
change it on the fly, use the menu beside the add bar; it remembers your
last pick. A job that hit its limit offers **Get next N** for the next
batch and **Get all** for the rest. Pools and manga are exempt: you
asked for the whole thing, so you get all of it.

## Watching a search

Watch a tag search or an artist page and monloader checks it again on a
schedule, so new posts keep landing in monbooru without you pasting the
URL again. Click **Watch** on a finished search in the queue, or paste
the URL on the **Watched** page and pick how often to check it.

## Retrying

- **Retry** shows on a job that didn't finish cleanly and runs it
  again, fetching every post again.
- **Force download** fetches everything again, skipped posts included:
  the way to get back a post whose image you deleted in monbooru.
- Sending a **single post** again always fetches it again, and
  monbooru adds any new tags to the image it has. That's how to
  refresh one post.

Stopping or restarting monloader cancels the jobs that hadn't
finished. They stay in the list so you can retry them, and one that was
mid-download comes back marked **interrupted**, one click away from
being queued again. Finished jobs clear themselves after a few days;
the delays are in **Settings -> Downloads**.

When a download fails and you want to know why, the `[debug]` next to a
finished item fetches that post again with gallery-dl's debug log on,
and shows you the log. Nothing is sent to monbooru.

## Pause and resume

**[pause]** in the top bar (also in the monsender popup) holds all
downloads: the one in progress finishes, then nothing new starts until
you resume. Use it to line up a batch before letting it run.

## Pools and manga

- A **booru pool** comes in as a
  [collection](../../../../guides/collections/index.md): each page is
  its own image with its own tags, in order.
- A **manga or comic** is bundled into one `.cbz` archive, which
  monbooru opens in its reader. If any page fails to download, the job
  fails rather than sending half a book.
- A **manga title** with chapters becomes one archive per chapter.

## Tagging by hash

Paste a file's md5 into the add bar and monloader imports the post
that has that file; see [Reverse lookup](../lookup/index.md).
