---
name: url-to-pdf
description: 将网页 URL 转为 PDF，使用 headless 浏览器并支持自动滚动以加载懒加载资源。适用于“保存网页为 PDF / 保留排版和图片 / 从指定选择器生成正文 PDF”等需求。
---

# URL 转 PDF

## 快速开始

```bash
python3 scripts/url_to_pdf.py --url "<URL>" --out /tmp/page.pdf
```

仅正文（提取指定选择器并重新排版）：

```bash
python3 scripts/url_to_pdf.py --url "<URL>" --out /tmp/page.pdf --content-selector "#js_content"
```

## 依赖安装

```bash
python3 -m pip install playwright beautifulsoup4
python3 -m playwright install chromium
```

或使用内置安装脚本：

```bash
./scripts/setup.sh
```

## 备注

- 默认开启自动滚动加载懒加载图片；可用 `--no-scroll` 关闭。
- 页面异步渲染时可用 `--wait-selector` 等待特定元素出现。
- 如 Playwright 无法下载浏览器，可使用已安装的 Chrome：`--chrome-path "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"`。
