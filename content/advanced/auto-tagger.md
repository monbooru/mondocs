---
title: "Auto-tagger: GPU and models"
weight: 30
---

The [auto-tagger guide](../guides/auto-tagger/index.md) covers
installing and running taggers. This page is about making them faster
with a GPU, bringing your own models, and the settings that only live
in files.

## Running on a GPU

Tagging runs on the CPU by default. To use a GPU, pick an execution
provider under **Settings -> Auto-Tagger** (or set
`tagger.execution_provider`):

| Provider | For |
|---|---|
| `cuda` | NVIDIA |
| `tensorrt` | NVIDIA, with TensorRT |
| `directml` | any Direct3D 12 GPU on Windows |
| `openvino` | Intel GPUs |
| `coreml`, `coremlv2` | Apple hardware |

The Windows downloads already carry a runtime built with DirectML, so
`directml` works with nothing else to install. Every other provider
needs an ONNX Runtime built for it: take one from the
[ONNX Runtime releases](https://github.com/microsoft/onnxruntime/releases)
(1.21 or newer) and either put it next to the program in place of the
`onnxruntime.dll` or `libonnxruntime.so` that came with it, or point
`ORT_LIB_PATH` at it. The libraries the provider itself needs go in
the same folder. CUDA also wants CUDA 12 and cuDNN 9 installed.

On Docker, the default image is CPU-only. Use the `-cuda` image tag
for NVIDIA or `-openvino` for Intel, and pass the GPU into the
container the usual way; the compose file has a commented example for
each. An Intel GPU also needs `/dev/dri` passed in and the container
added to the host's render group. Both tags are amd64 only.

The first GPU run compiles the model and caches the result under the
data folder (`.nv-cache/` for CUDA, `.openvino-cache/` for OpenVINO),
so keep that folder on a persistent volume.

**Settings -> Auto-Tagger -> Parallel workers** (`tagger.parallel`,
default 4) is how many images are prepared and tagged at once. On a
GPU, raise it if the GPU sits idle waiting for images. DirectML
tags one image at a time whatever you set.

## More models

The [monbooru-plugins](https://github.com/monbooru/monbooru-plugins)
registry lists every tagger monbooru supports in `TAGGERS.md`, each
one a folder under `taggers/`. To add one, copy its folder into the
models folder: it shows up in **Settings -> Auto-Tagger** with an
**Install** button that shows the commands to fetch the weights, which
the folder does not hold.

A registry folder holds a `model.json` (the description, the default
thresholds and the files to download), and when the model needs them
a `profile_default.json` and a `dispatch_default.json`. Leave those
two alone, a newer copy of the folder replaces them. Your own changes
go in `tagger.json` and `dispatch.json` beside them.

## Your own models

Other ONNX tagging models may work too. Give each one its own
subfolder in the models folder, holding the `.onnx` weights (and the
`.onnx.data` file next to them, when the model ships one) and one
label file:

- `tags.csv`: a header row, then `index,name,category` per row. The
  category is a WD14 category number (`0` general, `4` character, ...)
  or a category name.
- `tags.txt`: one label per line, all `general`.
- a `.json` label file, described by the `tagger.json` below.

The new tagger shows up in **Settings -> Auto-Tagger** on the next
page load.

monbooru works out how to feed `.csv` (WD14-style) and `.txt`
(JoyTag-style) models on its own. For anything else, add a
`tagger.json` next to the model saying how its authors feed it. Every
field is optional and only restates what differs from that guess:

| Field | Values |
|---|---|
| `input_size` | the square side in pixels; leave it out to read it from the model |
| `layout` | `nhwc` or `nchw` |
| `channels` | `rgb` or `bgr` |
| `normalize` | `none`, `div255`, `imagenet`, `clip`, or `mean_std` with `norm_scale`, `norm_mean` and `norm_std`: each pixel becomes `(value / norm_scale - norm_mean) / norm_std` |
| `pad` | `white_square`, `mean_color_aspect` or `fill` with `fill_color` as `[r, g, b]` |
| `activation` | `logits` when the model's scores still need a sigmoid, `sigmoid_in_model` when they don't |
| `label_format` | `csv`, `txt` or `json` |
| `label_json` | where a `.json` label file keeps its labels: `shape` is `index_map` (`{"0": "tag", ...}`), `list` (`["tag", ...]`) or `blocks` (`[{"name": category, "offset": n, "tags": [...]}]`), `path` the dotted way to it, and `category_path` the dotted way to a tag-to-category object |
| `category_scheme` | `wd14_numeric`, `name_string` (the label file names the categories) or `single_general` |
| `category_map` | renames the label file's categories, `{"style": "artist"}` |
| `output_index` | which of the model's outputs holds the scores, when it has several |

Here's the one for PixAI's tagger. Its runner pads to a black square,
maps pixels to `-1..1`, applies a sigmoid, and keeps its labels in
`tags.json` as one block per category, the `style` block being
artists:

```json
{
  "version": 1,
  "profile": {
    "layout": "nchw", "channels": "rgb",
    "normalize": "mean_std", "norm_scale": 255,
    "norm_mean": [0.5, 0.5, 0.5], "norm_std": [0.5, 0.5, 0.5],
    "pad": "fill", "fill_color": [0, 0, 0],
    "activation": "logits",
    "label_format": "json",
    "label_json": {"shape": "blocks", "path": "categories"},
    "category_scheme": "name_string",
    "category_map": {"style": "artist"}
  }
}
```

Its ratings are labelled `rating:g`, `rating:s`, `rating:q` and
`rating:e`, so it also needs four
[label rules](#label-rules-dispatchjson) that rename them to
`general`, `sensitive`, `questionable` and `explicit`. The
`profile_default.json` files in the registry's folders are more
examples.

## Label rules (dispatch.json)

The mappings tab of a tagger's **Configure** dialog is the easy way to
change where a label goes. It saves your rules as `dispatch.json` next
to the model, and you can also write or share that file by hand:

```json
{
  "version": 1,
  "rules": [
    { "source": "monochrome",       "category": "medium" },
    { "source": "ugly_label",       "category": ""       },
    { "source": "twitter_username", "category": "meta", "name": "twitter" }
  ]
}
```

- `source` is the label the model emits.
- `category` is where it goes. An empty string drops the label.
- `name`, if set, renames the tag. A rule into `rating` has to end on
  one of the four ratings.

monbooru ships rules of its own for the suggested taggers, taken from
their registry folders, and any other model from the registry brings
its own as `dispatch_default.json`. Your file goes on top: a rule for
the same label replaces the shipped one, a new label is added.

## Memory

A model stays loaded for 15 minutes after its last run, then unloads
to free RAM and VRAM. **Settings -> Auto-Tagger** has the delay
(`tagger.idle_release_after_minutes`); `0` unloads right after each
run. **Settings -> Maintenance -> Free memory** unloads it on the
spot.

## Videos and archives

A video is tagged from five frames and an archive from its pages, and
a label has to show up on several of them to stick.
`tagger.aggregation.min_hit_fraction` (default `0.05`) sets what share
of the frames that is. Set it to `0` and one frame is enough.

## Environment variables

| Variable | What it does |
|---|---|
| `MONBOORU_TAGGER_WORKER_LOG` | Log level (`warn` / `info` / `debug`) for the tagger process only. Unset, it follows monbooru's own level. |
| `MONBOORU_TAGGER_DIRECTML_DEVICE_ID` | Which GPU DirectML uses, by adapter number. Defaults to `0`. |
| `ORT_LIB_PATH` | Full path to the ONNX Runtime library, when it isn't next to the program or on the system library path. |
| `CUDA_CACHE_PATH` | Where CUDA keeps its compiled cache. Defaults to `.nv-cache/` in the data folder. |
