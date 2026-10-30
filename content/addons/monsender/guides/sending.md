---
title: Sending
weight: 10
---

There are three ways to send something to monloader: the toolbar
button, the keyboard shortcut, and the right-click menu.

## Tagged or untagged: what arrives

What you send decides what arrives in monbooru:

- A **post page** on a booru monloader knows (or a pool, a tag search,
  an artist page) comes in with its tags, rating and source. The popup
  labels these "booru - tags will be included".
- A **direct image file** (an address ending in `.jpg` on some image
  server) is just downloaded, so it comes in without tags or rating.
  When you send one from the right-click menu or a page scan, the page
  you were on is recorded as its source, so you can find your way
  back.

When you have the choice, send the post page. Which sites monloader
knows is covered in [Sites and credentials](../../monloader/guides/sites/index.md).

## The toolbar button

**send page** works on any web page, labelled or not: monloader makes
the final call, and a page it can't handle comes back as "not a
supported site".

The result shows in the popup within a few seconds. If monloader takes
longer than the wait set in [settings](../settings/index.md), the
popup says "queued" and the job carries on in the queue below.

## The keyboard shortcut

Ctrl+Shift+L sends the current page without opening the popup. A badge
on the toolbar icon shows how it went, and opening the popup clears
it.

## Right-click an image or video

Right-click an image or video and pick **Send to monloader**. The
extension sends the best thing it can:

1. the post the image links to, if it's on a known site (so in a
   thumbnail grid you get the tagged post, not the thumbnail);
2. otherwise the page you're on, if it's a known site;
3. otherwise the file itself, untagged, in the largest size the page
   offers.

When it sent the page but you pointed at one image, say on a post
holding a finished piece plus sketches, a note appears next to the
image for a few seconds: "sent the post page [only this image]". Click
**only this image** to swap the post for just that file. To pick
several images from a page, [scan it](scanning/index.md).

## Following what you sent

The bottom of the popup shows monloader's recent jobs, with a marker
on the ones this browser sent. It's monloader's whole queue, so it
also shows the lookups monbooru asks for. Each row counts monloader's
outcomes in short words (new, dup, skip, fail...), explained on
[Downloading](../../monloader/guides/downloading/index.md#per-item-outcomes).
Hover a failed row to see why.

Each job can be retried. When a job skipped posts monloader had
downloaded before, **[force download]** fetches them anyway, the way
to get back something you deleted in monbooru. A tag search that hit
monloader's limit offers **[continue]** for the next batch and
**[fetch all]** for the rest.

The pause button holds monloader's whole queue: the download in
progress finishes, and nothing new starts until you resume. It's the
same pause as on monloader's own pages.
