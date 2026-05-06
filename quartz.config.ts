// quartz.config.ts

import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

const config: QuartzConfig = {
  configuration: {
    // --- 这里是你要修改的核心部分 ---
    pageTitle: "🧠 Cixia's digital-garden", // 网站左上角和浏览器标签页的标题
    enableSPA: true,
    enablePopovers: true,
    analytics: {
      provider: "plausible",
    },
    // 你的网站最终部署的地址
    baseUrl: "cixia-zhao.github.io/digital-garden", 
    // 忽略一些不需要发布的文件或文件夹
    ignorePatterns: ["private", "templates", ".obsidian"],
    // 默认主题设置
    defaultDateType: "created",
    theme: {
      typography: {
        header: "Schibsted Grotesk",
        body: "Source Sans Pro",
        code: "IBM Plex Mono",
      },
      colors: {
        // 这里可以定义明亮和暗黑模式的颜色，暂时可以不用动
        lightMode: { /* ... */ },
        darkMode: { /* ... */ },
      },
    },
  },
  plugins: {
    // 这是插件列表，决定了网站的功能，默认已经很强大了
    transformers: [ /* ... */ ],
    filters: [ /* ... */ ],
    emitters: [ /* ... */ ],
  },
}

export default config
