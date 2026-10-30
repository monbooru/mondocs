---
title: Themes
weight: 20
---

Four themes come with monbooru: `dark` (the default), `light`,
`legacy-dark` and `legacy-light`. You pick between them under
**Settings -> Plugins**, and the choice applies at once, no restart
needed. You can share your own in the
[monbooru-plugins registry](https://github.com/monbooru/monbooru-plugins).
A theme folder works in monloader too, picked under its
**Settings -> Themes**.

## Making your own

A theme is a folder in `themes/`, next to `monbooru.toml`, holding a
`theme.css` and, if you want, a logo, a tab icon and drawings:

```
/config/themes/mytheme/theme.css
/config/themes/mytheme/logo.png          # optional, replaces the topbar logo
/config/themes/mytheme/favicon.png       # optional, replaces the tab icon
/config/themes/mytheme/mascot-lost.png   # optional, the 404 page and a search with no match
/config/themes/mytheme/mascot-sleep.png  # optional, an empty gallery, inbox or queue
/config/themes/mytheme/mascot-panic.png  # optional, a gallery that can't be read
```

The other drawings are `mascot-hello.png` (the first-run setup page),
`mascot-sparkle.png` (monloader's home page and its setup page), and
`mascot-sparkle-head.png` (beside a running job). The registry's
`dark` and `light` folders carry every one of them. A theme without a
drawing shows none there.

It shows up in the picker straight away. On first start monbooru
copies its light theme to `themes/light/` as an example to start
from. Copy it under a new name rather than editing it in place: a
theme of your own is never touched by an update.

## The variables

Every colour and the font come from one `:root` block, so a theme is
that block and nothing else. Here's a light one:

```css
:root {
  color-scheme: light;     /* scrollbars, dropdowns and autofill follow it */
  --bg:         #f4f1ee;   /* the page */
  --bg-surface: #e6e0da;   /* top bar, sidebar, panels, dialogs */
  --bg-input:   #ffffff;   /* text fields */
  --border:     #c8bfb6;   /* every rule and outline */
  --fg:         #1c1a19;   /* text */
  --fg-dim:     #6b625c;   /* secondary text */
  --accent:     #9d2235;   /* the selected image, pressed buttons, fills; never text */
  --on-accent:  #f4f1ee;   /* the text on an accent fill */
  --link:       #8a1f30;   /* links, keyboard focus and every coloured text */
  --danger:     #9d2235;   /* delete buttons */
  --on-danger:  #ffffff;   /* the text on them */
  --success:    #2f7a4d;
  --warning:    #8a6a10;
  --error:      #b02a37;
  --monloader:  #2f5d8a;   /* the monloader actions */
  --peer:       var(--monloader);
  --tagger:     #1f6f63;   /* the auto-tagger */
  --plugin:     #7a3fa0;   /* plugin buttons */
  --fav:        #c0392b;   /* favorites */
  --remove:     #a03a44;   /* tag remove buttons */
  --alternate:  #4f45a0;   /* the Variant button in a relations session */
  --scrim:      #ffffff;   /* badges over images */
  --backdrop:   rgb(28 26 25 / 45%);  /* behind an open dialog */
  --shadow-block: rgb(28 26 25 / 30%);  /* the hard shadow under a dialog and a message */
  --media-bg:   #ffffff;   /* behind an image that doesn't fill its frame */
  --font-mono:  "IBM Plex Mono", monospace;
}
```

Each top menu entry can take a colour of its own:

```css
:root {
  --nav-images:      #b12937;
  --nav-inbox:       #8f4c1b;
  --nav-categories:  #755a0d;
  --nav-tags:        #226c3a;
  --nav-collections: #136a64;
  --nav-relations:   #1e6393;
  --nav-settings:    #813cb5;
}
```

Tag category colours are set on the Categories page, but a theme can
recolour the ones monbooru ships with. Each variable is named after
the colour it replaces, so a category you recoloured yourself keeps
your colour:

```css
:root {
  --cat-3d90e3: #2b5ea4;   /* general   */
  --cat-00aa00: #226c3a;   /* character */
  --cat-cc0000: #b12937;   /* artist    */
  --cat-aa00aa: #883aac;   /* copyright */
  --cat-ffaa00: #7a580e;   /* meta      */
  --cat-996666: #82505b;   /* rating    */
  --cat-7d4fbf: #6945c4;   /* medium    */
  --cat-b85c9e: #983a7d;   /* person    */
  --cat-4a8fa8: #2b657b;   /* year      */
  --cat-ed5d1f: #944923;   /* species   */
}
```

The name in the top bar and on the login screen has four variables:

```css
:root {
  --wordmark-font:     bold 16px var(--font-mono);  /* a CSS font shorthand */
  --wordmark-case:     uppercase;
  --wordmark-tracking: 2px;
  --wordmark-accent:   currentColor;   /* the part after "mon" */
}
```

Each page names its app, so a block like this one
applies to monloader only:

```css
:root[data-app="monloader"] {
  --accent:   #3f51b5;
  --link:     #303f9f;
  --monbooru: #a3243b;
}
```

These variable names are kept stable between releases. Anything else
in monbooru's stylesheet can change, so a theme that overrides more
than the variables may need fixing after an update.

## Name and colour outside the page

Two settings under `[server]` in `monbooru.toml` go with a theme:

- `theme_color` is the colour of the splash screen and the mobile
  address bar when monbooru is installed as an app. Set it to your
  `--bg`.
- `name` replaces "monbooru" in the top bar, the page titles and the
  login screen.
