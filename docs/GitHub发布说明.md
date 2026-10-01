# GitHub 发布操作

项目已上传到 https://github.com/TaoTao-319/python-pytest-step08 ，本地 `main` 分支已跟踪 `origin/main`。下面保留初次发布的步骤，便于理解 Git 操作；当前仓库已经完成这些操作。

在 GitHub 创建一个空仓库，例如 `python-pytest-portfolio`，不要在网站初始化 README，因为本地已经有 README 与提交历史。复制仓库的 HTTPS 地址。

在项目根目录打开 PowerShell：

```powershell
git status
git log --oneline -3
# 把下面变量内容替换为你刚创建仓库的实际 HTTPS 地址。
$repoUrl = 'https://github.com/TaoTao-319/python-pytest-step08.git'
git remote add origin $repoUrl
git push -u origin main
```

推送完成后，打开仓库首页核对 README 是否显示，源码和测试目录是否存在，证据图片是否能打开。仓库简介可写：`Python 与 pytest 测试作品，覆盖输入校验、购物车金额、参数化、fixture 与异常断言。`

还可以下载仓库或重新克隆，照 README 创建虚拟环境、安装依赖并运行测试。不要只检查网页上的文件名，要确认实际能够运行。

项目压缩包已排除虚拟环境、Git 内部目录、缓存和本地验证副本。使用 Git 推送时会保留本地提交历史；通过网页上传压缩包解压后的文件时不会自动保留这段历史。

## 后续更新

修改文件后，在项目根目录执行：

```powershell
git status
git add .
git commit -m "Describe the project changes"
git push
```

提交说明应替换为本次修改的实际内容。已经设置过远程仓库，不需要再次运行 `git remote add origin`。
