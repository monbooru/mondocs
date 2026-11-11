---
title: Tags
weight: 20
---

A tag is a short label for one thing about a picture: `red_hair`,
`beach`, `hakurei_reimu`, `2003`. Give each image a few and you can
combine them in a search to narrow thousands of images down to the
handful you want.

## Adding tags

Type tags into the tag box on an image's page, separated by spaces. A
tag can't contain a space, so a multi-word tag uses underscores, or
quotes that do it for you: `"john doe"` becomes `john_doe`. Names are
lowercase and can use almost any character except spaces, the double
quote and `*`, so `girls'_frontline`, `fate/grand_order` and
`東方project` all work.

To tag many images at once, tick them in the gallery and press
**Add** in the batch bar's tags group. **Remove** next to it takes
tags off again, by name or by where they came from.

In an image's tag list, click a tag to search for it, or the `?` in
front of it to open [the tag's own page](#notes-and-links).

## Categories

Every tag sits in a category, which says what kind of thing it names
and gives it a colour: `general` for what's in the picture,
`character`, `artist`, `copyright` for the series or franchise, `meta`
for things about the file, plus `medium`, `person`, `year`, `species`
and `rating`. Put the category in front when you type:
`artist:"john doe" blue_eyes 1girl` adds `john_doe` as an artist and
the other two as general tags.

The **Categories** page lets you recolour categories, add your own and
change their order: drag a row to move its group of tags up or down on
the image page and in the gallery sidebar.

To fold spellings together or keep a name out for good, see
[Cleaning up tags](../tag-cleanup/index.md).

## Ratings and the SFW ceiling

A rating says how safe an image is to have on screen, from `general`
through `sensitive` and `questionable` to `explicit`. An image has one
rating. Adding another replaces it, and yours always wins over an
auto-tagger's.

The rating buttons in the footer set the **SFW ceiling**: click
`sfw` and everything rated above `general` disappears from the gallery,
related images and anything else you browse. Batch actions on "the
whole search" respect it too, so they never touch an image you can't
see. Click `explicit` to turn it off again. Each browser remembers its
own ceiling.

## Where tags come from

A tag can come from several places: you, an auto-tagger, a booru that
monloader pulled from, the Hydrus Public Tag Repository, or monbooru
itself. monbooru keeps track of each one separately, and an image's tag
list shows it next to the tag:

- `87%`: only an auto-tagger put the tag there, and that's how sure it
  was.
- `x3`: three sources agree on it.
- Struck through and marked `stale`: the source no longer lists the
  tag. It stays until you remove it, and **[remove all]** under the
  list clears every stale tag at once.

The **group by: [category] / [source]** switch above the list regroups
it by source, so you can see what each one added. Removing a tag in
that view only removes that source's copy: if another source also has
the tag, it stays.

You can search on all of this: `tagged:user` finds images you tagged
yourself, `tagged:danbooru` the ones danbooru tagged,
`autotagged:false` the ones no auto-tagger has seen, and `stale:any`
the ones with stale tags.

### Tags monbooru adds by itself

Some things can be read straight from the file, so monbooru tags them
as images arrive: the size (`highres`, `lowres`), the shape
(`wide_image`, `tall_image`), what it is (`video`, `animated`) and a
few more. They go in `meta` and use Danbooru's names.

They don't count as tagging: `tagged:false` still finds an image
nobody has tagged. Turn them off with **Automatically generate meta
tags from the file** under **Settings -> General**. **Settings ->
Maintenance** adds them to the images you already have or takes them
all off.

## Notes and links

A tag's own page holds a note about what the tag means to you and a
list of links (an artist's pages, a series' official site), along with
the tag's aliases and implications. The note takes the same
[formatting](../provenance/index.md#formatting) as image notes, so it
can point at other tags with `[tag]...[/tag]`.
