## GitHub SSH 配置

* 服务器使用独立密钥：`/home/codexdev/.ssh/id_ed25519_github_digital_garden`。
* 公钥已添加到 GitHub 账户；私钥只保留在服务器，绝不复制到平板、手机或聊天中。
* GitHub 仓库使用 SSH 地址，例如：`git@github.com:cixia-zhao/digital-garden.git`。
* 验证连接：`ssh -T git@github.com`；推送前先执行 `git status`。
