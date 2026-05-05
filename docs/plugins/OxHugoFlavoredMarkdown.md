---
title: OxHugoFlavoredMarkdown
tags:
  - plugin/transformer
---

This plugin provides support for [ox-hugo](https://github.com/kaushalmodi/ox-hugo) compatibility. See [OxHugo compatibility](OxHugo%20compatibility.md) for more information.

> [!note]
> For information on how to add, remove or configure plugins, see the [](configuration.md#Plugins|Configuration) page.

This plugin accepts the following configuration options:

- `wikilinks`: If `true` (default), converts Hugo `{{ relref }}` shortcodes to Quartz [wikilinks](wikilinks.md).
- `removePredefinedAnchor`: If `true` (default), strips predefined anchors from headings.
- `removeHugoShortcode`: If `true` (default), removes Hugo shortcode syntax (`{{}}`) from the content.
- `replaceFigureWithMdImg`: If `true` (default), replaces `<figure/>` with `![]()`.
- `replaceOrgLatex`: If `true` (default), converts Org-mode [Latex](features/Latex.md) fragments to Quartz-compatible LaTeX wrapped in `$` (for inline) and `$$` (for block equations).

> [!warning]
> While you can use this together with [ObsidianFlavoredMarkdown](ObsidianFlavoredMarkdown.md), it's not recommended because it might mutate the file in unexpected ways. Use with caution.
>
> If you use `toml` frontmatter, make sure to configure the [Frontmatter](Frontmatter.md) plugin accordingly. See [OxHugo compatibility](OxHugo%20compatibility.md) for an example.

## API

- Category: Transformer
- Function name: `Plugin.OxHugoFlavoredMarkdown()`.
- Source: [`quartz/plugins/transformers/oxhugofm.ts`](https://github.com/jackyzha0/quartz/blob/v4/quartz/plugins/transformers/oxhugofm.ts).
