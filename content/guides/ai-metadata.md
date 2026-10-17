---
title: AI metadata
weight: 40
---

Stable Diffusion tools like A1111, Forge and ComfyUI save how an image
was made inside the file: the prompt, the model, the seed, sometimes
the whole workflow. monbooru reads all of it as images arrive, shows
it on the image's page, and lets you search on it.

It reads PNG, JPEG and WebP files. AVIF and JPEG XL files aren't read.

## What you see

An image's page gets a **Generation data** block: prompt, negative
prompt, model, sampler, seed and the rest, with the raw parameters or
the full ComfyUI workflow underneath.

At the top of the block is the **generation hash**, a short
fingerprint of the recipe (prompt, model, sampler, steps, CFG, but not
the seed). Every image made from the same recipe shares it, so
clicking it lists all your re-rolls of that prompt together.

A PNG that only carries ComfyUI's editor graph, without the API
version of the workflow, gives up its nodes but no prompt, seed or
model.

## Searching

| Search | Finds |
|---|---|
| `ai:any` | any image with generation data (`ai:a1111`, `ai:comfyui`, `ai:none` also work) |
| `prompt:catgirl` | images whose prompt contains "catgirl" |
| `model:sdxl` | images made with a model whose name contains "sdxl" |
| `sampler:dpm` | images made with a matching sampler |
| `seed:12345` | images with that exact seed |
| `generated:abcd1234abcd` | images sharing that generation hash |

They combine like any other search: `ai:comfyui model:sdxl prompt:cat`
finds the ComfyUI images of cats made with an SDXL model.

## Searching inside a ComfyUI workflow

`prompt:`, `model:` and `sampler:` only see the handful of values
monbooru picks out of a workflow, from the nodes it knows. A custom
node it doesn't know can be taught to it, see
[Configuration](../advanced/configuration.md#comfyui-nodes).
`comfyui:` searches the whole thing: every node the workflow uses and
every value set on it, custom nodes included.

| Search | Finds |
|---|---|
| `comfyui:IPAdapterAdvanced` | workflows that use that node |
| `comfyui:lora_name=my_lora.safetensors` | a node input set to that value |
| `comfyui:lora_name=*detail*` | the same with a wildcard |
| `comfyui:steps=20..30` | a number in a range |
| `comfyui:"title=Base pass"` | a node by its title; quote values with spaces |

The easiest way in is the Generation data block itself: every node
name and value there is a link that runs the search finding it. Typing
`comfyui:` in the search bar also suggests the nodes and values your
own images use.

A search term matches anywhere in the workflow, so
`comfyui:KSampler comfyui:steps=28` finds workflows that have both,
not necessarily on the same node.
