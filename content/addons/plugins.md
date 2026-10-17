---
title: Plugins
weight: 100
---

A plugin is a small program that pairs with monbooru the way monloader
does and adds a few buttons to its interface: say, a **crop** button
on an image's page, or a **rotate** button for a batch of selected
images. Anyone can write one, in any language.

A plugin works on your library through monbooru's API, and it can
show its own pages. Those pages open inside monbooru and can do
anything you can do there, so only pair plugins you trust.

## The two kinds of button

A **relay** button sends the plugin the image you're looking at, or
everything you selected, and shows you the plugin's answer. If the
plugin changed the files, the page reloads so you see the result.

An **open** button shows one of the plugin's own pages in a pop-in
over monbooru, for anything that needs a real interface: a crop tool,
an artist database, a tag editor of your own design. When you're done,
it closes and the page reloads.

A plugin can say which files it handles. One that only edits pictures
won't show its buttons on videos or comic archives, and leaves them
out of a batch, telling you how many it skipped.

## Installing one

A plugin that comes as a folder is installed by dropping the folder
into `plugins/`, next to `monbooru.toml`. It shows up under
**Settings -> Plugins** switched off, and nothing runs until you
enable it; monbooru shows you the exact command first. A plugin that
runs on its own (in Docker, say) pairs the way monloader does and
lands in the same list.

## Where to find them

The [monbooru-plugins registry](https://github.com/monbooru/monbooru-plugins)
lists plugins and themes people have published. Being listed there is
not a review: every entry links its source so you can read it, and
bugs go to the plugin's own tracker.

To write your own, see [Writing a plugin](../advanced/api.md#writing-a-plugin).
