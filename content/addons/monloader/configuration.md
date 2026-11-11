---
title: Configuration
weight: 80
---

monloader keeps its settings in `monloader.toml` (`/config/monloader.toml`
in Docker) and writes it with defaults on first start. The Settings
page edits almost all of it. The override tables and a few server keys
are only in the file.

## monloader.toml

```toml
setup_done = false                       # first-run setup page, desktop installs only

[server]
bind_address = "0.0.0.0:8456"
base_url     = "http://localhost:8456"   # shown on the API docs page; set it to a domain you reach monloader by
name         = ""                        # rename the UI; empty = monloader
theme        = ""                        # dark, light, legacy-dark, legacy-light or a theme in themes/, see Look below; empty = dark

[monbooru]
api_url         = "http://monbooru:8455" # where monloader reaches monbooru
api_token       = ""                     # written by pairing
web_url         = ""                     # monbooru's address as your browser sees
                                         # it, for links; empty = no links
default_gallery = ""                     # empty = monbooru's active gallery
paused          = false                  # set by the footer light's pause

[downloader]
concurrency            = 1               # downloads at once; applies on restart
max_items_per_job      = 200             # posts per job for a tag search
default_folder         = ""              # monbooru subfolder for downloads; blank = monbooru's "Where received files go"
success_retention_days = 3               # clear succeeded jobs after this many days; 0 = never
history_retention_days = 14              # clear every other finished job after this many days; 0 = never

[tags]
drop_categories = []                     # monbooru categories left out of every push
blacklist       = []                     # a post matching any of these rules is skipped before download

[gallerydl]
binary_path   = "gallery-dl"
config_path   = "/config/gallery-dl.json"          # written by monloader
archive_path  = "/config/gallery-dl-archive.sqlite" # remembers what was downloaded
cookies_dir   = "/config/cookies"
sleep_request = 1.0                      # seconds between requests to a site
raw_config    = ""                       # extra gallery-dl config, see below
supportedsites_path = ""                 # site table override; empty = the built-in one

[auth]
enable_password       = false            # see Password below
password_hash         = ""
session_lifetime_days = 7
# named API tokens live under [[auth.tokens]]; create them in Settings -> Authentication

[log]
level = "warn"                           # warn / info / debug

[ptr]                                    # see Hydrus PTR
enabled      = false
paused       = false                     # set by the PTR page's pause and resume
data_path    = "/ptr"                    # a running sync takes it on restart
address      = "https://ptr.hydrus.network:45871"
access_key   = ""                        # empty = the public read-only key
fetch_sleep  = 1.0                       # seconds between update downloads
min_free_gb  = 90                        # free space needed to start syncing
commit_sleep = 1.0                       # seconds between contribution uploads

[lookup]                                 # see Reverse lookup
min_similarity         = 80              # percent
scheduled_daily_budget = 25              # images a day for monbooru's nightly run

[lookup.iqdb]
order = 2                                # position in the lookup chain
# url = "https://..."                    # only if the service moves

[lookup.saucenao]
order   = 3
api_key = ""
# url = "https://..."                    # only if the service moves

[desktop]
tray = true                              # tray icon, desktop builds only

[[sites]]                                # one block per site you configured
name         = "gelbooru"                # gallery-dl's name for the site
api_key      = ""
user_id      = ""
username     = ""
password     = ""
gallery      = ""                        # monbooru gallery; empty = default_gallery
label        = ""                        # source label; empty = the site name
cookies      = ""                        # path to a cookies file; the paste box writes one into cookies_dir
user_agent   = ""                        # text or +firefox, +chrome, +gallery-dl; empty = the default
options      = ""                        # extra gallery-dl options, as JSON
blacklist    = []                        # adds to [tags] blacklist for this site
lookup_order = 4                         # position in the lookup chain; 0 = not asked
```

Sites edited on the profile tab are saved next to the config as
`profiles/<site>.json`; see [development](development.md#site-profiles).

## Override tables

Three more tables, for corrections the profiles don't cover. An
override wins over any profile and applies from the next download:

```toml
# send one site's tag category somewhere else
[[tag_overrides]]
site = "e621"
from = "species"
to   = "general"

# read one site's rating value differently
[[rating_overrides]]
site = "somebooru"
from = "x"
to   = "explicit"

# the source label for a host no site covers (also in Settings)
[[host_labels]]
host  = "static.example.org"
label = "example"
```

`site` is gallery-dl's name for the site, the same as `[[sites]] name`.

## Environment variables

Each of these overrides its key in the file on every start, so a
Settings change to an env-set key lasts until the next restart; change
it in the compose file instead.

| Variable | Overrides |
|---|---|
| `MONLOADER_SERVER_BIND_ADDRESS` | `server.bind_address` |
| `MONLOADER_SERVER_BASE_URL` | `server.base_url` |
| `MONLOADER_MONBOORU_API_URL` | `monbooru.api_url` |
| `MONLOADER_MONBOORU_API_TOKEN` | `monbooru.api_token` |
| `MONLOADER_MONBOORU_WEB_URL` | `monbooru.web_url` |
| `MONLOADER_MONBOORU_DEFAULT_GALLERY` | `monbooru.default_gallery` |
| `MONLOADER_DOWNLOADER_CONCURRENCY` | `downloader.concurrency` |
| `MONLOADER_DOWNLOADER_MAX_ITEMS_PER_JOB` | `downloader.max_items_per_job` |
| `MONLOADER_DOWNLOADER_DEFAULT_FOLDER` | `downloader.default_folder` |
| `MONLOADER_DOWNLOADER_SUCCESS_RETENTION_DAYS` | `downloader.success_retention_days` |
| `MONLOADER_DOWNLOADER_HISTORY_RETENTION_DAYS` | `downloader.history_retention_days` |
| `MONLOADER_GALLERYDL_BINARY_PATH` | `gallerydl.binary_path` |
| `MONLOADER_GALLERYDL_CONFIG_PATH` | `gallerydl.config_path` |
| `MONLOADER_GALLERYDL_ARCHIVE_PATH` | `gallerydl.archive_path` |
| `MONLOADER_GALLERYDL_COOKIES_DIR` | `gallerydl.cookies_dir` |
| `MONLOADER_GALLERYDL_SUPPORTEDSITES_PATH` | `gallerydl.supportedsites_path` |
| `MONLOADER_GALLERYDL_SLEEP_REQUEST` | `gallerydl.sleep_request` |
| `MONLOADER_AUTH_ENABLE_PASSWORD` | `auth.enable_password` |
| `MONLOADER_AUTH_PASSWORD_HASH` | `auth.password_hash` |
| `MONLOADER_LOG_LEVEL` | `log.level` |
| `MONLOADER_PTR_ENABLED` | `ptr.enabled` |
| `MONLOADER_PTR_DATA_PATH` | `ptr.data_path` |
| `MONLOADER_PTR_ADDRESS` | `ptr.address` |
| `MONLOADER_PTR_ACCESS_KEY` | `ptr.access_key` |
| `MONLOADER_PTR_FETCH_SLEEP` | `ptr.fetch_sleep` |
| `MONLOADER_PTR_MIN_FREE_GB` | `ptr.min_free_gb` |
| `MONLOADER_PTR_COMMIT_SLEEP` | `ptr.commit_sleep` |
| `MONLOADER_LOOKUP_MIN_SIMILARITY` | `lookup.min_similarity` |
| `MONLOADER_LOOKUP_SAUCENAO_API_KEY` | `lookup.saucenao.api_key` |
| `MONLOADER_LOOKUP_IQDB_URL` | `lookup.iqdb.url` |
| `MONLOADER_LOOKUP_SAUCENAO_URL` | `lookup.saucenao.url` |

`TZ` sets the timezone for displayed times (UTC by default).
`MONLOADER_CONTAINER`, set by the official image, makes a brand-new
config use the container defaults shown above. Without it,
`bind_address` starts as `127.0.0.1:8456`, `api_url` as
`http://127.0.0.1:8455`, and the paths sit beside the config file, or
in the folders listed on [Install](getting-started/install.md) for the
desktop builds.

## Pairing by hand

To manage the monbooru token yourself instead of pairing, put a
monbooru API token with read and write permissions in
`monbooru.api_token` or `MONLOADER_MONBOORU_API_TOKEN`. There's no
field for it in the Settings page.

## gallery-dl

**Settings -> Advanced** can install any gallery-dl release without
waiting for a monloader update, and go back to the bundled version in
one click. The installed copy is kept with monloader's own files, so
it survives updates.

The same section has a box for raw gallery-dl configuration: a JSON
object merged into the `gallery-dl.json` monloader writes, with your
keys winning. It's the way to set any gallery-dl option monloader has
no field for. Per-site options go in the site's own dialog instead
(see [Sites and credentials](guides/sites/index.md)).

Downloads pass through a scratch folder and are deleted from it once
monbooru has them. In Docker it doesn't need a volume; mount a `tmpfs`
at `/work` if you'd like it in RAM.

## Password

The web UI has no password by default. Turn one on under **Settings ->
Authentication**, or hash one and put it in the file:

```bash
./monloader -hash-password 'your-password'
# or with Docker:
docker exec -it monloader monloader -hash-password 'your-password'
```

Put the result in `auth.password_hash` and set
`auth.enable_password = true`. A login lasts `session_lifetime_days`.

## Look

`name` under `[server]` changes the name in the top bar and page
titles. monloader takes the same theme folders as monbooru: put one in
`themes/`, next to `monloader.toml`, and pick it under
**Settings -> Themes** (`theme` holds the choice). A theme's logo, tab
icon and drawings come with it. See
[Themes](../../advanced/themes.md).

## Log levels

- `warn` (the default): warnings, errors and failed logins.
- `info`: adds a line per request, the startup banner, logins and settings changes.
- `debug`: adds the queue polling and health checks.
