---
title: Building from source
weight: 50
---

monbooru is a Go program. From a checkout of the
[repository](https://github.com/monbooru/monbooru):

```bash
# without the auto-tagger
go build -o monbooru ./cmd/monbooru

# with the auto-tagger (needs cgo and the ONNX Runtime library)
CGO_ENABLED=1 go build -tags tagger -o monbooru ./cmd/monbooru

# with the Linux tray icon (needs GTK 3 and libayatana-appindicator)
CGO_ENABLED=1 go build -tags tray -o monbooru ./cmd/monbooru

./monbooru -config /path/to/monbooru.toml
```

With no config file, the first run writes `monbooru.toml` in the
working directory (or wherever `-config` points), with its data and
gallery folders next to it. Edit the paths there if you want them
somewhere else; the keys are on [Configuration](configuration.md).

A `-tags tagger` build needs the ONNX Runtime library at run time:
`libonnxruntime.so` on the library path, or `ORT_LIB_PATH` pointing
at it. See [Auto-tagger: GPU and models](auto-tagger.md). Video, AVIF
and JPEG XL thumbnails and the animated previews need `ffmpeg` and
`ffprobe`, on the `PATH` or next to the program.

`main` is one snapshot per release and what a clone builds. Work and
pull requests go to `dev`;
[CONTRIBUTING](https://github.com/monbooru/monbooru/blob/main/CONTRIBUTING.md)
has the details.
