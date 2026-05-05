---
title: RoamFlavoredMarkdown
tags:
  - plugin/transformer
---

This plugin provides support for [Roam Research](https://roamresearch.com) compatibility. See [Roam Research compatibility](Roam%20Research%20Compatibility.md) for more information.

> [!note]
> For information on how to add, remove or configure plugins, see the [](Configuration.md#Plugins|Configuration) page.

This plugin accepts the following configuration options:

- `orComponent`: If `true` (default), converts Roam `{{ or:ONE|TWO|THREE }}` shortcodes into HTML Dropdown options.
- `TODOComponent`: If `true` (default), converts Roam `{{[TODO](TODO)}}` shortcodes into HTML check boxes.
- `DONEComponent`: If `true` (default), converts Roam `{{[DONE](DONE)}}` shortcodes into checked HTML check boxes.
- `videoComponent`: If `true` (default), converts Roam `{{[video](video):URL}}` shortcodes into embeded HTML video.
- `audioComponent`: If `true` (default), converts Roam `{{[audio](audio):URL}}` shortcodes into embeded HTML audio.
- `pdfComponent`: If `true` (default), converts Roam `{{[pdf](pdf):URL}}` shortcodes into embeded HTML PDF viewer.
- `blockquoteComponent`: If `true` (default), converts Roam `{{[>](>)}}` shortcodes into Quartz blockquotes.

## API

- Category: Transformer
- Function name: `Plugin.RoamFlavoredMarkdown()`.
- Source: [`quartz/plugins/transformers/roam.ts`](https://github.com/jackyzha0/quartz/blob/v4/quartz/plugins/transformers/roam.ts).
