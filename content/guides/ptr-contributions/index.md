---
title: Contributing to the PTR
weight: 100
---

The Hydrus Public Tag Repository (PTR) is a huge tag database shared by
Hydrus users, where anyone can add tags and volunteers (janitors)
review the disputed ones. monloader can keep a copy of it for lookups
(see the [PTR guide](../../addons/monloader/guides/ptr/index.md)).
Once you have a PTR account, monbooru also lets you give back: add
tags your images have that the PTR lacks, and ask for wrong ones to be
removed.

Everything goes through monloader. You need its PTR copy fully synced,
and a contribution account created on monloader's PTR page.

## From an image

An image's page has a **Public Tag Repository** panel under the tag
box. It says how many of the image's tags the PTR doesn't have yet,
and how many tags the PTR has that your image doesn't. **Pull tags**
brings the second kind in; **contribute...** sends the first kind out.

The contribute dialog has two lists:

- **add**: tags the PTR doesn't have for this file yet. Some go up
  under the PTR's own spelling (an `artist:` tag is a `creator:` tag
  there), and the row says so. A row marked "not a PTR tag" would
  create a brand new tag on the PTR, so check first that the PTR
  doesn't already know it under another name.
- **petition removal**: tags the PTR has for this file that your image
  doesn't. Your image lacking a tag doesn't make it wrong, so only
  tick one that is actually wrong for the picture, and give a reason.

**send to PTR** sends it under your account and shows what went
through. Added tags apply right away. Petitions go to the janitors
with your reason, and can't be taken back once sent.

## From a tag

A tag's own page has the same panel, for its aliases and implications
instead of its images.

The PTR may know your tag under another name: you called a character
`samus_aran_(metroid)`, the PTR files her as `character:samus aran`.
If one of your aliases matches, the panel uses that name
automatically. If none does, **[look up as...]** lets you pick the
PTR's spelling from a list of names close to yours, and shows what a
pull would bring. You can then keep your own spelling and add the
PTR's as aliases, or switch your images over to the PTR's name and
keep yours as the alias. Either way, the two are linked from then on.

Its **contribute...** dialog works like the image one: **suggest**
sends aliases and implications you declared that the PTR doesn't have,
and **petition removal** asks for wrong ones to go. Both need a short
reason for the janitors. The dialog only sends what your own tags
declare, so set things up in monbooru first, then contribute.

## Afterwards

monloader keeps the history of everything you sent: what was applied,
what a janitor approved or turned down, what's still waiting. Open
its PTR page to see it; each row links back to the image or tag. Tags
you added can be taken back from there. Suggestions and petitions
can't, which is why the dialogs ask before sending.
