---
title: Manga and comic archives
weight: 35
---

A CBZ or ZIP archive full of images is treated as one item: one
thumbnail in the grid (its first page), one set of tags, one rating.
**Open in reader** on its page reads it, and the reader remembers
where you stopped.

If the archive carries a `ComicInfo.xml`, the series, author and other
details it holds show on the archive's page.

The [auto-tagger](../auto-tagger/index.md#videos-and-archives) reads
every page and merges what it finds into one set of tags for the whole
book.

## Extracting a page

To keep one page as an image of its own, press **Extract** in the
reader (or `e`). The page is saved as a new file in your upload folder
and opens so you can tag it.

## Turning an archive into a collection

Sometimes an archive would be better as separate images: you want to
tag each page on its own, drop the credits page, or keep just a few
variants. **Generate collection** on the archive's page unpacks it:
every page becomes its own image, in a folder named after the archive,
filed in order into a [collection](../collections/index.md) you name.
Each page is linked back to the archive, so you can always find where
it came from.

The archive itself stays as it was, and its tags aren't copied onto
the pages.

To go the other way and pack a collection into an archive, see
[Collections](../collections/index.md#turning-a-collection-into-an-archive).
