---
title: Maintenance
weight: 110
---

monbooru looks after itself: the watcher keeps it in step with your
folders and a nightly run tidies up. The tools under
**Settings -> Maintenance** are for the times it can't know what
happened, like when you reorganized files with monbooru switched off
or restored a backup.

## Which tool when

**You moved or deleted files while monbooru wasn't running.** Press
**sync** in the top bar (or `Y`). Files that are gone are marked
missing rather than forgotten, so their tags survive if they come
back. When you know they won't, **Missing images** removes them for
good, and **Empty folders** lists the folders the move left behind so
you can clear them out.

**Thumbnails look wrong, or you restored a backup.** **Rebuild
thumbnails** makes them all again, manga pages included.

**You're turning on a feature for a library you already have.** New
files are handled as they arrive; these catch up the images you
already had:

- **Compute hashes** for finding [near-duplicates](relations/index.md);
- **Meta tags** for the [tags monbooru writes itself](tags/index.md#where-tags-come-from),
  and **Remove meta tags** to take them off again;
- **Re-extract metadata** when an update reads more from your files,
  such as [generation data](ai-metadata.md) or comic archive details.

**You want to start your tags over, or tidy up after an import.**
**Unused tags** deletes the tags no image carries. The ones you gave an
alias, an implication or a note stay unless you tick the box. **Reset
tags** deletes every tag, alias and implication in the gallery, the
ratings aside, so you can tag from scratch; export the gallery first if
you might want them back. To empty a single category instead, use
**Clean up** next to it on the Categories page.

**You want disk space or memory back.** **Vacuum database** compacts
the database file, and **Free memory** hands back the memory monbooru
is holding, auto-tagger models included.

To clean up duplicate files, use the relations tools; see
[Relations](relations/index.md#cleaning-up-duplicates).

## Nightly schedule

**Settings -> Schedule** runs a set of jobs every night, at 01:00 by
default. Syncing and cleaning up leftover thumbnails are on out of the
box. Auto-tagging, finding relation pairs and
[looking up unsourced images](lookup/index.md#looking-up-a-library-overnight)
are there to switch on. With several galleries, you can pick which
galleries each job runs on: your own photos might get the sync and
skip the lookups. **Run now** starts the same run straight away.

If you're running monbooru on a desktop, it may not be on at the scheduled time. Under
**Run time** you can have a missed run happen a few minutes after
monbooru starts or the machine wakes up, or drop the clock and run
once a day at startup instead. Desktop installs start with the
catch-up choice.

Something not working? See [Troubleshooting](../advanced/troubleshooting.md).
