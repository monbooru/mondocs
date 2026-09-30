---
title: Install
weight: 10
---

monbooru comes three ways: a Docker image, a portable folder you
unpack anywhere, or a normal installed app. They all run the same
program and end up in the same place, a web page at
`http://localhost:8455`.

## Docker

1. Grab [`docker/docker-compose.yml`](https://github.com/monbooru/monbooru/blob/main/docker/docker-compose.yml)
   from the monbooru repository and edit the volume paths so they
   point at your folders.
2. `docker compose up -d`
3. Open `http://localhost:8455`.

| Mount | What goes there |
|---|---|
| `/gallery` | your images |
| `/data` | the database and thumbnails |
| `/config` | `monbooru.toml`, themes and plugins |
| `/models` | auto-tagger models |

Keep `/data` on a persistent volume: it holds everything monbooru
knows about your files.

The container runs as user `1000:1000`, the usual first user on a
Linux machine. Change `user:` in the compose file to your own uid:gid
so the files monbooru writes belong to you.

The compose file also starts [monloader](../addons/monloader/_index.md),
the optional companion for downloading and reverse lookup. Delete its
block if you don't want it.

## Portable

Download a **portable** build for your system from the
[releases page](https://github.com/monbooru/monbooru/releases),
unpack it and run the program. A browser opens on a short setup page.

A portable folder keeps everything inside itself:

```
monbooru/            the folder you unpacked
  monbooru           the program (monbooru.exe on Windows)
  monbooru.toml      settings
  data/              database, thumbnails, logs
  gallery/           your images
```

Move the folder or copy it to a USB stick and it keeps working. Delete
it and monbooru is gone. To upgrade, replace the program file (and the
bundled tools, if you took the bundled download) and leave the rest
alone.

Each build comes in two flavours:

- **lite** is just the program. Video, AVIF and JPEG XL thumbnails
  need ffmpeg installed on your system, and auto-tagging needs ONNX
  Runtime.
- **bundled** adds both, so everything works out of the box.

## Installed

If you'd rather have monbooru in your applications menu and
uninstall it the normal way, take one of these instead. Each opens the
same setup page on first run.

- Windows: the installer.
- Linux: an AppImage, or a Flatpak.
- Arch Linux: `monbooru` in the AUR. Install `onnxruntime` and
  `ffmpeg` alongside it for auto-tagging and video thumbnails.

Every release also has a `SHA256SUMS` file if you want to check your
download.

### Where an installed copy keeps your files

| | Linux | Windows |
|---|---|---|
| Settings, plugins, themes | `~/.config/monbooru` | `%AppData%\monbooru` |
| Database and thumbnails | `~/.local/share/monbooru` | `%LocalAppData%\monbooru` |
| Log file | `logs` in the database folder | same |
| Your images | wherever you pointed setup | same |

A Flatpak keeps the first three under
`~/.var/app/io.github.monbooru.Monbooru/` instead.

To run monbooru as a service on a server, see
[Configuration](../advanced/configuration.md#running-it-on-a-server).

## Next

[First steps](first-steps/index.md) walks you through adding and
tagging your first images.
