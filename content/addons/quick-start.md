---
title: Quick start
weight: 10
---

This page adds monloader (downloads and lookups) and the monsender
browser extension to a monbooru you already run. It assumes the
Docker setup from [Install](../getting-started/install.md); if you use
the desktop downloads instead, install monloader the same way from its
[install page](monloader/getting-started/install.md) and continue from
step 2.

## 1. Start monloader

monbooru's `docker/docker-compose.yml` already has a monloader
service, on the same network. Start it:

```bash
docker compose up -d monloader
```

Then open `http://localhost:8456`.

## 2. Pair monloader with monbooru

1. In monloader, go to **Settings**. Under **monbooru**, the default
   api url `http://monbooru:8455` is right for the shared compose
   network.
2. Under **pairing**, click **connect to monbooru**.
3. In monbooru, open **Settings -> Plugins** and approve the request.
4. Back in monloader, pick the **default gallery** downloads go to, and
   save.

To try it, paste the URL of a booru post into monloader's add bar. A
moment later the image is in monbooru, with its tags.

## 3. Add the browser extension

1. [Install monsender](monsender/getting-started/install.md) in
   Firefox or Chrome.
2. In the extension's options, set the monloader URL, the address your
   browser reaches it at: `http://localhost:8456` on the same machine,
   or your server's address, like `http://192.168.1.20:8456`.
3. Click **connect to monloader**, then approve the request in
   monloader under **Settings -> pairing**.

Now open a post on a booru and press the extension's toolbar button
(or Ctrl+Shift+L). The page goes to monloader, downloads, and shows up
in monbooru.

## Where next

- [Which sites monloader supports](monloader/guides/sites/index.md)
- [Sending pages from the browser](monsender/guides/sending.md)
- [Looking up images you already have](../guides/lookup/index.md)
