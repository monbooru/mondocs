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
| `/ptr` | optional: the Hydrus PTR copy, only if you turn it on (tens of GB, see [Hydrus PTR](../guides/ptr/index.md)) |

## Portable

Download a **portable** build from the
[releases page](https://github.com/monbooru/monloader/releases),
unpack it and run it. Everything it writes goes in a `data` folder next
to the program. The **lite** build expects gallery-dl to be installed
already; the **bundled** one brings its own.

## Installed

On Windows there's an installer; on Linux, an AppImage and a Flatpak.
They keep their files here:

| | Linux | Windows |
|---|---|---|
| Settings and site profiles | `~/.config/monloader` | `%AppData%\monloader` |
| Queue, cookies and gallery-dl's files | `~/.local/share/monloader` | `%LocalAppData%\monloader` |
| Log file | `logs` in that same folder | same |
| PTR copy | `ptr` in that same folder | same |

A Flatpak keeps all of it under
`~/.var/app/io.github.monbooru.Monloader/` instead.

## Next

[Pair it with monbooru](pairing/index.md), pick the gallery downloads
go to, then paste a URL into the add bar on the home page. The
[downloading guide](../guides/downloading/index.md) explains what
happens next.
