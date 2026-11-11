---
title: Troubleshooting
weight: 60
---

The problems people run into most, by what you see on screen or in the
log.

## A "degraded mode" banner

monbooru can't read the gallery folder. What's already indexed stays
browsable, but syncing and the watcher are off. Fix the path or its
permissions and restart.

## "Library too old to upgrade directly"

The gallery was last opened by a monbooru too old for this one to
upgrade. The message names a release that still can: run that release
once against the same folders, then start the current one again.

## Thumbnails are missing

Run **Settings -> Maintenance -> Rebuild thumbnails**. Videos, AVIF,
JPEG XL and the animated preview of a GIF need ffmpeg, which comes
with the Docker image and the bundled downloads. If you installed your
own, restart monbooru so it finds it (JPEG XL needs a build with
libjxl).

The bundled ffmpeg is a small build that only covers the formats
monbooru supports. If one of your videos uses a codec it refuses and
you have a full ffmpeg installed, delete `ffmpeg` and `ffprobe` from
the monbooru folder and it uses yours instead.

## New files don't show up

Check that they're inside the gallery folder, under the size limit
in **Settings -> General**, and in a supported format, then press the
sync button. A file the watcher missed is always picked up by a sync.

## The watcher stops with "no space left on device"

That's Linux's limit on watched folders (`inotify limit hit` in the
log). Raise `fs.inotify.max_user_watches` on the host, not inside the
container, and restart. If raising it changes nothing, raise
`fs.inotify.max_user_instances` too. Or turn the watcher off in
**Settings -> General** and sync by hand.

## Moving or deleting a file fails with a permission error

The file belongs to another user. Make it writable for the user
monbooru runs as. On Docker, check that the `CHOWN` and `DAC_OVERRIDE`
capabilities are still there; see
[Docker details](configuration.md#docker-details).

## Locked out of the login

After a few wrong passwords the login makes you wait before trying
again. Wait a few minutes, or restart monbooru.

## The API answers 503 api_disabled

No API token exists yet. Create one under
**Settings -> Authentication**; see [API and plugins](api.md).
