---
name: wechat-to-notebooklm
description: 获取微信公众号文章链接，提取正文内容并生成保留图片和排版的 PDF，通过 tmc/nlm CLI 上传到 NotebookLM。适用于“公众号文章转 PDF”“保存微信公众号到 NLM/NotebookLM”“把公众号文章放进 NotebookLM”“选择 notebook 并上传”等场景。
---

# 微信公众号 → NotebookLM

## 快速开始

```bash
python3 scripts/wechat_to_notebooklm.py --url "<WECHAT_URL>"
```

常用选项：

```bash
python3 scripts/wechat_to_notebooklm.py --url "<WECHAT_URL>" --notebook-id "<ID>"
python3 scripts/wechat_to_notebooklm.py --url "<WECHAT_URL>" --new-title "My Notebook"
python3 scripts/wechat_to_notebooklm.py --list-only
python3 scripts/wechat_to_notebooklm.py --url "<WECHAT_URL>" --pdf-path "/path/to/article.pdf"
python3 scripts/wechat_to_notebooklm.py --url "<WECHAT_URL>" --out "/path/to/custom.pdf"
python3 scripts/wechat_to_notebooklm.py --url "<WECHAT_URL>" --nlm-timeout 120
```

## 依赖安装（headless 浏览器）

```bash
python3 -m pip install playwright beautifulsoup4
python3 -m playwright install chromium
```

或使用内置安装脚本：

```bash
./scripts/setup.sh
```

## 安装与认证（nlm CLI）

Go 版本（推荐，支持上传 PDF）：

```bash
go install github.com/tmc/nlm@latest
```

认证（默认会打开浏览器登录）：

```bash
nlm auth
```

查看认证状态：

```bash
nlm auth status
```

## NotebookLM MCP 集成（已移除）

该 skill 已移除 notebooklm-mcp 相关流程，仅使用 Go 版 `nlm` CLI（支持上传 PDF）。

## 工作流

1. 输入微信公众号文章 URL。
2. 运行 `scripts/wechat_to_pdf.py` 生成内容型 PDF（保留图片）。
3. 运行 `scripts/wechat_to_notebooklm.py` 列表并上传。
4. 如果无法列出 notebook，手动输入 notebook id。

## 备注

- `wechat_to_pdf.py` 默认自动滚动以加载懒加载图片；可用 `--no-scroll` 关闭。
- 可用 `--max-scroll-ms`、`--scroll-step-px`、`--scroll-pause-ms` 调整滚动策略。
- `wechat_to_pdf.py` 默认超时提升到 60s，可用 `--timeout-ms` 调整。
- `wechat_to_pdf.py` 默认使用文章标题作为 PDF 文件名；可用 `--out` 覆盖。
- `wechat_to_notebooklm.py` 的 `--nlm-timeout` 可调整 `nlm` CLI 超时。
- 如果无法下载 Playwright 浏览器，可用已安装的 Chrome：`--chrome-path "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"`。
- `nlm` CLI 推荐使用 Go 版本 https://github.com/tmc/nlm（支持上传 PDF）。
- 若链接需要登录/验证，可能无法直接抓取。
- 若只需要“URL → PDF”，请使用独立的 `url-to-pdf` skill。
