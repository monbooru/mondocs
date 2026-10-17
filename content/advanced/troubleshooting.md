---
title: Troubleshooting
weight: 60
---

## A "degraded mode" banner

monbooru can't read the gallery folder. What's already indexed stays
browsable, but syncing and the watcher are off. Fix the path or its
permissions and restart.

## "Library too old to upgrade directly"

monbooru may upgrades a gallery's database from the last two minor
releases. A gallery last opened by something older stops the start
with this message, and names a release that still upgrades it: run
that release once against the same folders, then start the current
one again. Nothing is changed in the meantime.

## Thumbnails are missing

Run **Settings -> Maintenance -> Rebuild thumbnails**. Videos,
animated GIFs, AVIF and JPEG XL need ffmpeg, which comes with the
Docker image and the bundled downloads. If you installed your own,
restart monbooru so it finds it (JPEG XL needs a build with libjxl).

The bundled ffmpeg is a small build that only covers the formats
monbooru supports. If one of your videos uses a codec it refuses and
you have a full ffmpeg installed, delete `ffmpeg` and `ffprobe` from
the monbooru folder and it uses yours instead.

## New files don't show up

Check that they're inside the gallery folder, under the size limit
in **Settings -> General**, and in a supported format, then press the
sync button. A file the watcher missed is always picked up by a sync.

## The watcher stops with "no space left on device"

That's Linux's limit on watched folders (`inotify_add_watch` in the
log). Raise `fs.inotify.max_user_watches` on the host, not inside the
container, and restart. If the log says "too many open files"
instead, raise `fs.inotify.max_user_instances`. Or turn the watcher
off in **Settings -> General** and sync by hand.

## Moving or deleting a file fails with a permission error

monbooru takes ownership of new files as it indexes them so it can
move or delete them later. A file that still belongs to another user
has to be made writable for the user monbooru runs as. On Docker,
taking ownership needs the `CHOWN` and `DAC_OVERRIDE` capabilities;
see [Docker details](configuration.md#docker-details).

## Locked out of the login

After a few wrong passwords the login makes you wait before trying
again. The wait is short and resets after a few quiet minutes, and
restarting monbooru clears it.

## The API answers 503 api_disabled

No API token exists yet. Create one under
**Settings -> Authentication**; see [API and plugins](api.md).
