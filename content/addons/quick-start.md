---
title: Quick start
weight: 10
---

This page adds monloader (downloads and lookups) and the monsender
browser extension to a monbooru you already run. It assumes the
Docker setup from [Install](../getting-started/install.md); with the
desktop downloads, install monloader from its
[install page](monloader/getting-started/install.md) instead, whose
setup page offers to pair it with monbooru, then continue from step 2
or 3.

## 1. Open monloader

monbooru's `docker/docker-compose.yml` has a monloader service on the
same network, so the `docker compose up -d` from Install already
started it. Open `http://localhost:8456`.

## 2. Pair monloader with monbooru

In monloader's **Settings**, click **Connect to monbooru** under
**Pairing**, then approve the request in monbooru under
**Settings -> Plugins**. Downloads go to monbooru's active gallery
unless you pick another **Default gallery** in monloader.
[Pairing with monbooru](monloader/getting-started/pairing/index.md)
has the steps with pictures.

To try it, paste the URL of a booru post into monloader's add bar. A
moment later the image is in monbooru, with its tags.

## 3. Add the browser extension

[Install monsender](monsender/getting-started/install.md) in Firefox
or Chrome. In its options, set the URL to `http://localhost:8456`,
click **connect to monloader**, and approve the request in monloader
under **Settings -> Pairing**.
[Setup](monsender/getting-started/setup/index.md) has the details.

The compose file only publishes monloader's port on the machine
itself. To send from a browser on another device, change its `ports:`
line and use your server's address instead.

Now open a post on a booru, click the extension's toolbar button and
press **send page** in its popup (Ctrl+Shift+L sends straight away).
The page goes to monloader, downloads, and shows up in monbooru.

## Where next

- [Which sites monloader supports](monloader/guides/sites/index.md)
- [Sending pages from the browser](monsender/guides/sending.md)
- [Looking up images you already have](../guides/lookup/index.md)
