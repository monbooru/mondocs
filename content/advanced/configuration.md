---
title: Configuration
weight: 10
---

monbooru keeps its settings in one file, `monbooru.toml`, and writes
it with defaults the first time it starts. Where it lives depends on
how you installed:

- Docker: `/config/monbooru.toml`.
- Portable folder: next to the program.
- Installed copy: the settings folder listed in
  [Install](../getting-started/install.md#where-an-installed-copy-keeps-your-files).
- Anything else (a build you ran yourself): the working directory, or
  wherever `-config` points.

Almost everything in it can be changed from the Settings page, which
writes the file back for you. A few things can only be changed here,
followed by a restart: the paths, the bind address and where each
gallery lives on disk. A save from the Settings page rewrites the
whole file, so comments and your own ordering don't survive it.

## monbooru.toml

The sample below shows the Docker defaults. Other installs seed their
own paths.

```toml
default_gallery = "default"      # the gallery loaded on startup
setup_done      = false          # first-run setup page, desktop installs only

[[galleries]]                    # one block per gallery
name         = "default"
gallery_path = "/gallery"        # the folder holding your images

[server]
bind_address  = "127.0.0.1:8455"          # the containers set 0.0.0.0:8455 instead
base_url      = "http://localhost:8455"   # used for links back to monbooru and CORS
cors_origins  = []               # other pages allowed to call the API; "*" for any
name          = ""               # rename the UI; empty = monbooru
theme         = ""               # see Themes
theme_color   = ""               # see Themes
monloader_url = ""               # monloader's address as your browser sees it,
                                 # for the footer link; empty = no link

[monloader]
api_url = ""                     # the monloader address monbooru calls;
                                 # empty = the one learned at pairing
# api_token and paused are written by pairing and the footer light

[paths]
data_path  = "/data"             # databases, thumbnails, caches
model_path = "/models"           # auto-tagger models, one subfolder each

[gallery]
watch_enabled         = true     # watch gallery folders for changes
max_file_size_mb      = 2048     # larger files are skipped; 0 = no limit
default_upload_folder = ""       # where received files land; empty = gallery root
default_upload_name   = ""       # what they are renamed to; empty = keep the name
rename_on_ingest      = false    # apply the two above to files found on disk too
auto_meta_tags        = true     # tag new files with what they are (highres, video...)
ignore                = ["@eaDir", "#recycle", "#snapshot", "@Recycle", ".@__thumb",
                         "$RECYCLE.BIN", ".Trash-*", ".Trashes", ".zfs", ".snapshots",
                         ".stversions", ".thumbnails", "._*"]   # never indexed

[tagger]
execution_provider         = "cpu"   # see Auto-tagger: GPU and models
parallel                   = 4       # images tagged in parallel
idle_release_after_minutes = 15      # unload idle models; 0 = right after each run

[tagger.aggregation]
min_hit_fraction = 0.05          # see Auto-tagger: GPU and models

[[tagger.taggers]]               # one block per tagger, managed from
name                 = "wd-swinv2"   # Settings -> Auto-Tagger
enabled              = true
confidence_threshold = 0.40
category_thresholds  = { character = 0.85 }  # optional threshold per category
per_category_top_k   = { general = 25 }      # optional cap on tags per category; 0 = no cap
disabled_categories  = ["meta"]              # optional, categories it never tags
galleries            = ["default"]           # optional; missing = every gallery, [] = none
model_file           = "model.onnx"          # optional; default model.onnx
tags_file            = "tags.csv"            # optional; default tags.csv (or tags.txt)

[auth]
enable_password       = false    # see Password below
password_hash         = ""
session_lifetime_days = 7
# [[auth.tokens]] blocks are managed by Settings -> Authentication

# [[plugin]] blocks are written by pairing and by Settings -> Plugins

[ui]
page_size     = 40               # images per gallery page
thumbnail_fit = "natural"        # "natural" (real shape) or "square" (cropped)

[log]
level = "warn"                   # warn / info / debug

[schedule]                       # the nightly run, see Maintenance
time                = "01:00"    # 24h, in the TZ timezone
mode                = "at_time"  # at_time / at_time_catchup / on_start / off
sync_gallery        = true
remove_orphans      = true
run_auto_taggers    = false
find_relation_pairs = false
lookup_ptr          = false
lookup_booru        = false

[schedule.galleries]             # optional: limit an action to some galleries
lookup_booru        = ["anime"]  # unlisted actions run on every gallery; [] = none

[relations]
default_distance      = 4        # how alike two pictures must be to pair (0-12)
default_session_order = "smallest_distance_first"  # or largest_file_first / random
incremental_on_ingest = true     # check each new image for near-duplicates; saving
                                 # Settings -> Relations turns this back on
tag_pairs             = true     # also pair images that share rare tags
tag_pair_threshold    = 0.85     # how strong that tag match must be (0.7-1)

[desktop]
tray = true                      # tray icon, desktop builds only
```

## Environment variables

Each of these overrides its key in the file. The file keeps its own value, and Settings shows the key greyed out with the variable's name.

| Variable | Overrides |
|---|---|
| `MONBOORU_SERVER_BIND_ADDRESS` | `server.bind_address` |
| `MONBOORU_SERVER_BASE_URL` | `server.base_url` |
| `MONBOORU_SERVER_CORS_ORIGINS` | `server.cors_origins` (comma-separated) |
| `MONBOORU_SERVER_MONLOADER_URL` | `server.monloader_url` |
| `MONBOORU_MONLOADER_API_URL` | `monloader.api_url` |
| `MONBOORU_MONLOADER_API_TOKEN` | `monloader.api_token` |
| `MONBOORU_PATHS_DATA_PATH` | `paths.data_path` |
| `MONBOORU_PATHS_MODEL_PATH` | `paths.model_path` |
| `MONBOORU_GALLERY_WATCH_ENABLED` | `gallery.watch_enabled` |
| `MONBOORU_GALLERY_MAX_FILE_SIZE_MB` | `gallery.max_file_size_mb` |
| `MONBOORU_GALLERY_AUTO_META_TAGS` | `gallery.auto_meta_tags` |
| `MONBOORU_TAGGER_EXECUTION_PROVIDER` | `tagger.execution_provider` |
| `MONBOORU_AUTH_ENABLE_PASSWORD` | `auth.enable_password` |
| `MONBOORU_AUTH_PASSWORD_HASH` | `auth.password_hash` |
| `MONBOORU_AUTH_SESSION_LIFETIME_DAYS` | `auth.session_lifetime_days` |
| `MONBOORU_LOG_LEVEL` | `log.level` |

Two more aren't tied to a key:

- `TZ` is the timezone for displayed times and the nightly schedule,
  for example `Europe/Paris`. It defaults to UTC.
- `MONBOORU_CONTAINER` is set by the official images. It only decides
  where a brand-new config puts its folders: the `/data`, `/models`
  and `/gallery` mounts with it, next to the config file without it.
  Set it if you build your own image around those paths.

The auto-tagger's own variables are on
[Auto-tagger: GPU and models](auto-tagger.md).

## Log levels

- `warn` (the default): warnings, errors and failed logins.
- `info`: adds a line per request, startup messages, logins and
  settings changes.
- `debug`: adds everything else, thumbnails and status polls included.

## Password

There's no login by default, which is fine on a home network. To add
one, turn it on under **Settings -> Authentication**, or set
`auth.enable_password = true` and a `password_hash` in the file. To
make the hash:

```bash
./monbooru -hash-password 'your-password'
# or with Docker:
docker exec -it monbooru monbooru -hash-password 'your-password'
```

A login lasts `session_lifetime_days` (7 by default) or until monbooru
restarts. Changing the password logs out every other browser.

## Running it on a server

The docker container is the best option for servers; its compose file
publishes the port on the machine itself only, so change its `ports:`
line for other machines to reach it. If you want to run a binary, there's no separate server download: take a portable archive, and
before starting it as a service,

- write a `monbooru.toml` next to the program with the settings you
  want, at least `bind_address` under `[server]` if other machines
  need to reach it (a file you wrote skips the setup page);
- add `-no-browser` to the launch line.

Everything monbooru makes still lands in that folder, so backing up
is copying one directory. Paths you point elsewhere are stored as
full paths; paths inside the folder stay relative, so the folder can
still move.

An empty `monbooru.toml` next to the program is what makes a copy
portable. The AppImage behaves like an installed app because a single
file has nowhere to carry one; put an empty `monbooru.toml` next to
the `.AppImage` and it keeps everything beside it instead.

## Docker details

The bundled compose file runs monbooru as `user: "1000:1000"`, drops
every container capability and adds back only `CHOWN` and
`DAC_OVERRIDE`. monbooru uses those two to take ownership of new
files so it can move or delete them later. If every file in your
gallery is already owned by the user the container runs as, you can
drop them too. Files behind a symlinked folder are never taken over;
make them writable by that user yourself if you want monbooru to move
or delete them.

The image has a healthcheck built in (`monbooru healthcheck`, which
probes `/health`), so `docker ps` shows the container as healthy once
it's up. Point your own monitoring at `GET /health` if you like.

## ComfyUI nodes

monbooru fills an image's prompt, model, sampler, seed and the rest
from the ComfyUI nodes it knows: KSampler, the checkpoint loaders, the
LoRA loaders and a few more. A workflow built from other nodes keeps
those fields empty. To teach monbooru a node, put a
`comfyui_nodes.json` next to `monbooru.toml` naming, for each node
type, the input that holds each field:

```json
{
  "version": 1,
  "nodes": {
    "RandomNoise": {"seed": "noise_seed"},
    "Efficient Loader": {"model": "ckpt_name", "lora": "lora_name"}
  }
}
```

The fields are `prompt`, `seed`, `steps`, `cfg`, `sampler`,
`scheduler`, `model`, `lora`, and `positive` (the sampler input that
points at the prompt node). An entry replaces monbooru's own for the
same node type. New images pick the file up as they arrive; run
**Settings -> Maintenance -> Re-extract metadata** for the ones
already in the gallery.

## Command-line flags

- `-config <path>`: the config file to use.
- `-hash-password <password>`: print a password hash and exit.
- `-desktop`: the desktop profile (OS folders or a portable folder, a
  log file, a browser at startup, the setup page). Every download has
  it on; `-desktop=false` turns it off.
- `-no-browser`: with `-desktop`, don't open a browser at startup.
- `-version`: print the version and exit.
- `healthcheck`: probe the local `/health` endpoint and exit 0 when
  monbooru answers.
