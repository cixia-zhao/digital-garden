---
title: Welcome to Quartz 4
---

Quartz is a fast, batteries-included static-site generator that transforms Markdown content into fully functional websites. Thousands of students, developers, and teachers are [already using Quartz](showcase.md) to publish personal notes, websites, and [digital gardens](https://jzhao.xyz/posts/networked-thought) to the web.

## 🪴 Get Started

Quartz requires **at least [Node](https://nodejs.org/) v22** and `npm` v10.9.2 to function correctly. Ensure you have this installed on your machine before continuing.

Then, in your terminal of choice, enter the following commands line by line:

```shell
git clone https://github.com/jackyzha0/quartz.git
cd quartz
npm i
npx quartz create
```

This will guide you through initializing your Quartz with content. Once you've done so, see how to:

1. [Writing content](authoring%20content.md) in Quartz
2. [Configure](configuration.md) Quartz's behaviour
3. Change Quartz's [layout](layout.md)
4. [Build and preview](build.md) Quartz
5. Sync your changes with [GitHub](setting%20up%20your%20GitHub%20repository.md)
6. [Host](hosting.md) Quartz online

If you prefer instructions in a video format you can try following Nicole van der Hoeven's
[video guide on how to set up Quartz!](https://www.youtube.com/watch?v=6s6DT1yN4dw&t=227s)

## 🔧 Features

- [Obsidian compatibility](Obsidian%20compatibility.md), [full-text search](full-text%20search.md), [graph view](graph%20view.md), [wikilinks, transclusions](wikilinks.md), [backlinks](backlinks.md), [Latex](features/Latex.md), [syntax highlighting](syntax%20highlighting.md), [popover previews](popover%20previews.md), [Docker Support](Docker%20Support.md), [internationalization](i18n.md), [comments](comments.md) and [many more](./features/) right out of the box
- Hot-reload on configuration edits and incremental rebuilds for content edits
- Simple JSX layouts and [page components](creating%20components.md)
- [Ridiculously fast page loads](SPA%20Routing.md) and tiny bundle sizes
- Fully-customizable parsing, filtering, and page generation through [plugins](making%20plugins.md)

For a comprehensive list of features, visit the [features page](./features/). You can read more about the _why_ behind these features on the [philosophy](philosophy.md) page and a technical overview on the [architecture](architecture.md) page.

### 🚧 Troubleshooting + Updating

Having trouble with Quartz? Try searching for your issue using the search feature. If you haven't already, [upgrade](upgrading.md) to the newest version of Quartz to see if this fixes your issue.

If you're still having trouble, feel free to [submit an issue](https://github.com/jackyzha0/quartz/issues) if you feel you found a bug or ask for help in our [Discord Community](https://discord.gg/cRFFHYye7t).
