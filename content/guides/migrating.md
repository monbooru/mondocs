---
title: Migrating
weight: 90
---

Coming from another app? monbooru's import (**Settings -> Galleries ->
Import**) reads an export from the apps below and brings over your
images and their tags. App-specific extras don't come along; each
section says what stays behind.

Once you have the export, drop it into the import dialog and pick
**Merge** or **Replace**; [Galleries](galleries/index.md#import)
explains the two.

## Hydrus Network

1. In Hydrus, select the files you want, then right-click ->
   **share** -> **export** -> **files**.
2. In the export dialog, add a **.txt** sidecar with the **all known
   tags / display tags** preset. Each file then gets a
   `<filename>.txt` next to it, one tag per line.
3. Export into a folder, and zip that folder.
4. Drop the zip into monbooru's import dialog.

Files keep their names and folders. Hydrus names files after their
SHA-256, and on a Merge that's what matches them to images you already
have.

Namespaced tags land in the matching category:

| Hydrus namespace | monbooru category |
|---|---|
| `character:` | `character` |
| `creator:` | `artist` |
| `copyright:`, `series:`, `studio:` | `copyright` |
| `meta:`, `medium:`, `person:`, `year:` | the category of the same name |
| any namespace matching one of your categories | that category |
| no namespace | `general` |
| any other namespace (`title:`, `filename:`...) | `general`, without the namespace |

**Not brought over:** URLs, rating services, notes and file
relationships.

## Blombooru

1. In Blombooru's admin panel, go to **Backup** -> **Download full
   backup**. You get a `.zip` with every media file and its tags.
2. Drop that zip into monbooru's import dialog.

Files keep their names, and tags land by category:

| Blombooru category id | monbooru category |
|---|---|
| 0 | general |
| 1 | artist |
| 3 | copyright |
| 4 | character |
| 5 | meta |
| anything else | general |

On a Merge, images are matched to the ones you already have by their
SHA-256, when Blombooru stored one (older entries only have an MD5).

**Not brought over:** albums, ratings, parent/child relations and
custom metadata.
