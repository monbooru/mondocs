---
title: Install
weight: 10
---

monloader needs a monbooru to send downloads to, and nothing else. It
comes the same three ways as monbooru.

## Docker

monbooru's `docker/docker-compose.yml` already has a monloader
service on the same network, so there's nothing to wire up:

```bash
docker compose up -d monloader
```

Open `http://localhost:8456`. The compose file only publishes the port
on the machine itself; change its `ports:` line to reach monloader
from elsewhere on your network.

| Mount | What goes there |
|---|---|
| `/config` | `monloader.toml`, gallery-dl's config, cookies, and your site profiles |
| `/ptr` | optional: the Hydrus PTR copy, only if you turn it on (about 80 GB, see [Hydrus PTR](../guides/ptr/index.md)) |

## Portable

Download a **portable** build from the
[releases page](https://github.com/monbooru/monloader/releases),
unpack it and run it. Everything it keeps goes in a `data` folder next
to the program. The **lite** build expects gallery-dl to be installed
already; the **bundled** one brings its own.

## Installed

On Windows there's an installer; on Linux, an AppImage, an AUR package
and a Flatpak. They keep their files here:

| | Linux (AppImage, AUR) | Windows |
|---|---|---|
| Settings and site profiles | `~/.config/monloader` | `%AppData%\monloader` |
| Queue, cookies and gallery-dl's files | `~/.local/share/monloader` | `%LocalAppData%\monloader` |
| Log file | `logs` in that same folder | same |
| PTR copy | `ptr` in that same folder | same |

A Flatpak keeps all of it under
`~/.var/app/io.github.monbooru.Monloader/` instead.

## First run

The portable and installed builds open a browser on a short setup page
the first time they start. Under **Connect to monbooru**, check the
**monbooru API URL**; the default fits a monbooru on the same computer.
If monbooru is already running, tick **Pair with monbooru** and
approve the request in monbooru under **Settings -> Plugins**. Under
**Who can open monloader?**, pick **Other devices on the LAN too** if
monsender will send from a browser on another device; **Only this
computer** keeps monloader to this machine.

## Next

[Pair it with monbooru](pairing/index.md), pick the gallery downloads
go to, then paste a URL into the add bar on the home page. The
[downloading guide](../guides/downloading/index.md) explains what
happens next.
