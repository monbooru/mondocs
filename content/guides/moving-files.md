---
title: Moving and renaming files
weight: 75
---

You can reorganize your files without leaving monbooru. Moves and
renames happen to the real files on disk, so what you see in your file
manager matches what you see in monbooru.

**Rename / move** on an image's page (or `m`) opens with the image's
current folder and name: change either or both. Clear the folder for
the top of the gallery; clear the name to keep the current one.
Missing folders are created, and the file extension stays as it is.

The gallery's batch bar has the same thing for a selection or a whole
search. There, a plain name numbers the files from one base,
`trip01.png`, `trip02.png` and so on, in the order they're shown, so
sort the gallery the way you want them counted first. When several
files would end up with the same name, they're numbered apart.

## Naming with tokens

Instead of a fixed name, either field can take a template made of
tokens: `{date}-{name}` puts the date a file was added in front of its
name, and `{name}-{hash:8}` ends it with the first characters of the
file's hash. The dialog lists the tokens as buttons: hover one to see
what it becomes, click it to add it.

The folder field can hold slashes, so `archive/{year}/{type}` files
each image under its year and kind, and `{folder}/{year}` sorts within
the folders you already have. In the batch bar the folder field
starts out as `{folder}`, so a batch rename leaves files in their
folders unless you change it.

## Naming files as they arrive

**Settings -> General -> Where received files go** decides where
uploads and files sent by other apps land, and what they're called.
Both halves take the same tokens: `inbox/{year}-{month}` and
`{name}-{hash:8}` file and name every incoming file. Files
[monloader](../addons/monloader/_index.md) sends can also use
`{source}` and `{post_id}`: `{source}-{post_id}` names a download
`danbooru-4821993.jpg`.

Files you drop into the gallery folder yourself are left where you put
them, unless you tick **Apply to files found on disk too**. Either
way, this only applies to new files: nothing already in your library
is moved behind your back. To rename and file those images too, use
**Settings -> Maintenance -> Apply destination**. With the folder left
blank, every image keeps its folder and only its name changes.

To move images to another gallery, see
[Transfer](galleries/index.md#transfer).
