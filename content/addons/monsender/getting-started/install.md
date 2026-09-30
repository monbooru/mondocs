---
title: Install
weight: 10
---

monsender runs in Firefox and Chrome. It needs a running monloader to
send to; if you don't have one yet, start with the
[quick start](../../quick-start.md).

## Firefox

Install it from
[Mozilla Add-ons](https://addons.mozilla.org/en-US/firefox/addon/monsender/).
Firefox keeps it up to date.

## Chrome

There's no Chrome Web Store listing. Instead, each release has a Chrome
build:

1. Download `monsender-chrome-<version>.zip` from the
   [releases page](https://github.com/monbooru/monsender/releases) and
   unzip it somewhere it can stay.
2. Open `chrome://extensions` and switch on **Developer mode** (top
   right).
3. Click **Load unpacked** and pick the unzipped folder.

To update, unzip the next release over the same folder and press the
reload arrow on the extension's card.

## What it's allowed to do

The extension only asks to read the page you use it on, store its
settings, and add an entry to the right-click menu. It can't see your
history, your downloads or your other tabs.

Next: [set it up](setup/index.md).
