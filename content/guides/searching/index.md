---
title: Searching
weight: 10
---

Finding things again is what tags are for. Type a tag in the search
bar and you get every image that has it. Type two, `red_hair beach`,
and you get only the images that have both. Every extra term narrows
the results down.

## The basics

| Search | Finds |
|---|---|
| `red_hair beach` | images with both tags |
| `red_hair -sketch` | `red_hair`, but not `sketch` |
| `cat OR dog` | images with either tag |
| `red*` | any tag starting with "red": `red_hair`, `red_eyes`... |
| `*hair*` | any tag with "hair" in it |
| `"re:zero"` | a tag with a colon in its name; quotes keep it a tag |

Case doesn't matter. The search box suggests tags as you type, each
with the number of images you'd get by adding it.

Tags live in categories (`character`, `artist`, `copyright` and so on,
see [Tags](../tags/index.md)). Put the category in front to be
specific: `character:saber` finds the character, not the general tag.
`cat:artist` finds any image with an artist tag at all.

Ratings search like tags: `rating:general` finds the images rated
general. Adding `-rating:explicit` is a quick way to keep a search
safe.

## Filters

Anything written as `key:value` with a known key is a filter, which
searches something other than tags: the file, where it came from,
when you added it. Filters combine with tags and each other like any
other term.

Numbers can be compared (`width:>=1920`, `duration:<30`) or given as
a range (`width:1000..2000`, `pages:100..`). Dates work the same, in
your own timezone: `date:2024-03-15` is that day, `date:2024-01..2024-06`
the first half of the year.

A few you're likely to use:

| Search | Finds |
|---|---|
| `inbox:true` | images you haven't reviewed yet |
| `fav:true` | your favorites |
| `tagged:false` | images nobody has tagged |
| `autotagged:false` | images no auto-tagger has seen |
| `tagcount:<5` | images with fewer than five tags |
| `folder:2024/trip` | a folder and everything under it |
| `name:vacation` | files with "vacation" in their name |
| `type:animated` | videos and animated GIFs |
| `width:>=3840 ratio:>1` | large landscape images, wallpapers maybe |
| `date:>2024-06-01` | images added since June 2024 |
| `source:none` | images with no known source |
| `ai:any model:sdxl` | AI images made with an SDXL model |
| `relation:duplicate` | images you marked as duplicates |

Files that have gone missing from disk are left out of every search.
Add `missing:true` to see them.

## Images with similar tags

`similar:1042` finds images that share tags with image 1042, closest
first. It catches what a pixel comparison can't: a redraw, a recolour,
another picture from the same set. Each result is badged with its
score as a percentage, and `similar:1042~0.7` keeps only the ones at
70% or better. The **[more like this]** link on an image's page runs
this search for you.

## Everything else: the system: list

There are many more filters: file hashes, how an image arrived,
generation settings, relation types, lookup states and so on. Rather
than listing them here, monbooru lists them where you need them: type
`system:` in the search bar and a dropdown shows every filter with a
hint for each. Pick one and it shows the values it takes.

![The system: dropdown in the search bar](search-system.png)

The [AI metadata](../ai-metadata.md) page covers the filters for
generation data, including searching inside ComfyUI workflows.

## Sorting and saving

Results can be sorted by date added (newest first, the default), file
size, or collection order. Random order (`R`) shuffles them, and the
shuffle stays put as you turn pages.

To keep a search around, run it and press **Save search** beside the
search bar. Saved searches show in the sidebar, one list per gallery.
