---
title: Wikilinks
---

Wikilinks were pioneered by earlier internet wikis to make it easier to write links across pages without needing to write Markdown or HTML links each time.

Quartz supports Wikilinks by default and these links are resolved by Quartz using the [CrawlLinks](CrawlLinks.md) plugin. See the [Obsidian Help page on Internal Links](https://help.obsidian.md/Linking+notes+and+files/Internal+links) for more information on Wikilink syntax.

This is enabled as a part of [Obsidian compatibility](Obsidian%20compatibility.md) and can be configured and enabled/disabled from that plugin.

## Syntax

- `[Path to file](Path%20to%20file)`: produces a link to `Path to file.md` (or `Path-to-file.md`) with the text `Path to file`
- `[ Here's the title override](Path%20to%20file%20)`: produces a link to `Path to file.md` with the text `Here's the title override`
- `[](Path%20to%20file#Anchor)`: produces a link to the anchor `Anchor` in the file `Path to file.md`
- `[](Path%20to%20file#^block-ref)`: produces a link to the specific block `block-ref` in the file `Path to file.md`

### Embeds

- `![Path to image](Path%20to%20image)`: embeds an image into the page
- `![100x145](Path%20to%20image)`: embeds an image into the page with dimensions 100px by 145px
- `![Path to file](Path%20to%20file)`: transclude an entire page
- `![](Path%20to%20file#Anchor)`: transclude everything under the header `Anchor`
- `![](Path%20to%20file#^b15695)`: transclude block with ID `^b15695`
