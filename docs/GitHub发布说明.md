# GitHub 发布操作

本成果提供本地 Git 仓库和可上传的项目文件。远程发布状态见成果清单，发布后再填写实际仓库地址。

在 GitHub 创建一个空仓库，例如 `python-pytest-portfolio`，不要在网站初始化 README，因为本地已经有 README 与提交历史。复制仓库的 HTTPS 地址。

在项目根目录打开 PowerShell：

```powershell
git status
git log --oneline -3
# 把下面变量内容替换为你刚创建仓库的实际 HTTPS 地址。
$repoUrl = 'https://github.com/YOUR_ACCOUNT/python-pytest-portfolio.git'
git remote add origin $repoUrl
git push -u origin main
```

推送完成后，打开仓库首页核对 README 是否显示，源码和测试目录是否存在，证据图片是否能打开。仓库简介可写：`Python 与 pytest 测试作品，覆盖输入校验、购物车金额、参数化、fixture 与异常断言。`

还可以下载仓库或重新克隆，照 README 创建虚拟环境、安装依赖并运行测试。不要只检查网页上的文件名，要确认实际能够运行。

项目压缩包已排除虚拟环境、Git 内部目录、缓存和本地验证副本。使用 Git 推送时会保留本地提交历史；通过网页上传压缩包解压后的文件时不会自动保留这段历史。
