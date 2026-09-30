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

monbooru checks the provider when you save and refuses it, with an
error saying why, when the library or the device isn't there.

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

The first GPU run on a new machine spends a few minutes compiling. The
result is cached under the data folder (`.nv-cache/` for CUDA,
`.openvino-cache/` for OpenVINO), so keep that folder on a persistent
volume and later starts are quick.

**Settings -> Auto-Tagger -> Parallel workers** (`tagger.parallel`,
default 4) is how many images are prepared and tagged at once. On a
GPU, raise it if the GPU sits idle waiting for images. DirectML tags
one image at a time whatever you set.

## Your own models

Other ONNX tagging models may work too. Give each one its own
subfolder in the models folder, holding:

- `model.onnx`, the weights;
- one label file: `tags.csv` (WD14 layout: `tag_id,name,category_id`),
  `tags.txt` (one label per line, all `general`), or a Camie-style
  metadata `.json`.

The new tagger shows up in **Settings -> Auto-Tagger** on the next
page load.

monbooru works out how to feed the model from the label file for
`.csv` (WD14-style) and `.txt` (JoyTag-style) models. For anything
else, including a Camie-style `.json`, add a `tagger.json` next to
`model.onnx` describing the model: `label_format` and
`category_scheme` at least, plus any of input size, channel order,
normalization, padding and output activation that differ from what
monbooru guessed. The files in the repository's
`internal/tagger/profile_default/` folder are working examples.

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

monbooru ships rules of its own for the catalog taggers
(`internal/tagger/dispatch_default/` in the repository), and your file
goes on top: a rule for the same label replaces the shipped one, a new
label is added. The **Export** tab of the Configure dialog shows the
merged result, ready to copy over the shipped file in a pull request
or to drop next to `model.onnx` on another install.

## Memory

A model stays loaded for 15 minutes after its last run, then unloads
to free RAM and VRAM. **Settings -> Auto-Tagger** has the delay
(`tagger.idle_release_after_minutes`); `0` unloads right after each
run. **Settings -> Maintenance -> Free memory** unloads it on the
spot.

Tagging runs in a separate `tagger-worker` process, so unloading gives
everything back to the system, GPU libraries included. If that
process gives you trouble, `MONBOORU_TAGGER_BACKEND=inproc` runs
tagging inside monbooru itself instead.

Tagging one image from its detail page always uses the CPU, even with
a GPU configured.

## Videos and archives

A video is tagged from five frames and an archive from its pages, and
a label has to show up on several of them to stick.
`tagger.aggregation.min_hit_fraction` (default `0.05`) sets what share
of the frames that is, never fewer than 2 or more than 10 frames. Set
it to `0` and one frame is enough.

## Environment variables

| Variable | What it does |
|---|---|
| `MONBOORU_TAGGER_EXECUTION_PROVIDER` | Overrides `tagger.execution_provider`. |
| `MONBOORU_TAGGER_BACKEND` | `inproc` runs tagging inside monbooru instead of a separate process. |
| `MONBOORU_TAGGER_WORKER_LOG` | Log level (`warn` / `info` / `debug`) for the tagger process only. |
| `MONBOORU_TAGGER_DIRECTML_DEVICE_ID` | Which GPU DirectML uses, by adapter number. Defaults to `0`, which on a laptop is often the integrated GPU rather than the fast one. |
| `ORT_LIB_PATH` | Full path to the ONNX Runtime library, when it isn't next to the program or on the system library path. |
| `CUDA_CACHE_PATH` | Where CUDA keeps its compiled cache. Defaults to `.nv-cache/` in the data folder. |
