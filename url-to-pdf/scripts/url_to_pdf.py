#!/usr/bin/env python3
import argparse
import asyncio
from pathlib import Path

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright


def build_html(title, author, date, body_html):
    return f"""<!doctype html>
<html>
<head>
  <meta charset=\"utf-8\" />
  <title>{title}</title>
  <style>
    :root {{
      --text: #111;
      --muted: #555;
      --bg: #fff;
    }}
    html, body {{
      margin: 0;
      padding: 0;
      background: var(--bg);
      color: var(--text);
      font-family: \"Georgia\", \"Times New Roman\", serif;
      line-height: 1.6;
    }}
    .page {{
      max-width: 820px;
      margin: 48px auto 64px;
      padding: 0 24px;
    }}
    h1 {{
      font-size: 28px;
      margin: 0 0 12px 0;
    }}
    .meta {{
      color: var(--muted);
      font-size: 14px;
      margin-bottom: 24px;
    }}
    img {{
      max-width: 100%;
      height: auto;
    }}
    p {{
      margin: 0 0 16px 0;
    }}
    blockquote {{
      margin: 16px 0;
      padding-left: 16px;
      border-left: 3px solid #ddd;
      color: #444;
    }}
  </style>
</head>
<body>
  <div class=\"page\">
    <h1>{title}</h1>
    <div class=\"meta\">{author} {date}</div>
    <div class=\"content\">
      {body_html}
    </div>
  </div>
</body>
</html>
"""


def normalize_images(soup):
    for img in soup.find_all("img"):
        data_src = img.get("data-src")
        src = img.get("src")
        if data_src:
            img["src"] = data_src
        elif src:
            img["src"] = src
    return soup


def find_chrome_executable():
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
    ]
    for path in candidates:
        if Path(path).exists():
            return path
    return None


async def auto_scroll(page, max_scroll_ms, step_px, pause_ms):
    elapsed = 0
    last_height = await page.evaluate("document.body.scrollHeight")
    last_loaded = await page.evaluate(
        "Array.from(document.images).filter(i => i.complete && i.naturalWidth > 0).length"
    )
    while elapsed < max_scroll_ms:
        await page.evaluate(f"window.scrollBy(0, {step_px});")
        await page.wait_for_timeout(pause_ms)
        elapsed += pause_ms
        height = await page.evaluate("document.body.scrollHeight")
        loaded = await page.evaluate(
            "Array.from(document.images).filter(i => i.complete && i.naturalWidth > 0).length"
        )
        if height == last_height and loaded == last_loaded:
            break
        last_height = height
        last_loaded = loaded
    await page.evaluate("window.scrollTo(0, 0);")


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="页面 URL")
    parser.add_argument("--out", default="page.pdf", help="输出 PDF 路径")
    parser.add_argument("--timeout-ms", type=int, default=20000)
    parser.add_argument("--wait-selector", help="抓取前等待的选择器")
    parser.add_argument("--content-selector", help="仅正文模式的内容选择器")
    parser.add_argument("--title-selector", help="仅正文模式的标题选择器")
    parser.add_argument("--author-selector", help="仅正文模式的作者选择器")
    parser.add_argument("--date-selector", help="仅正文模式的日期选择器")
    parser.add_argument("--no-scroll", action="store_true", help="禁用自动滚动")
    parser.add_argument("--max-scroll-ms", type=int, default=12000, help="自动滚动最长时间")
    parser.add_argument("--scroll-step-px", type=int, default=800, help="滚动步长（像素）")
    parser.add_argument("--scroll-pause-ms", type=int, default=200, help="滚动间隔（毫秒）")
    parser.add_argument("--chrome-path", help="指定本地 Chrome/Chromium 可执行文件路径")
    parser.add_argument("--headed", action="store_true", help="使用有界面模式（非 headless）")
    args = parser.parse_args()

    out_path = Path(args.out).expanduser().resolve()

    async with async_playwright() as p:
        launch_kwargs = {"args": ["--disable-crashpad", "--no-sandbox"]}
        chrome_path = args.chrome_path or find_chrome_executable()
        if chrome_path:
            launch_kwargs["executable_path"] = chrome_path
        browser = await p.chromium.launch(headless=not args.headed, **launch_kwargs)
        page = await browser.new_page()
        await page.goto(args.url, wait_until="domcontentloaded", timeout=args.timeout_ms)

        if args.wait_selector:
            await page.wait_for_selector(args.wait_selector, timeout=args.timeout_ms)

        if not args.no_scroll:
            await page.wait_for_timeout(500)
            await auto_scroll(page, args.max_scroll_ms, args.scroll_step_px, args.scroll_pause_ms)
            await page.wait_for_load_state("networkidle")

        if args.content_selector:
            await page.wait_for_selector(args.content_selector, timeout=args.timeout_ms)
            title = ""
            author = ""
            date = ""
            if args.title_selector:
                title = (await page.text_content(args.title_selector)) or ""
            if args.author_selector:
                author = (await page.text_content(args.author_selector)) or ""
            if args.date_selector:
                date = (await page.text_content(args.date_selector)) or ""

            body_html = await page.inner_html(args.content_selector)
            soup = BeautifulSoup(body_html, "html.parser")
            for tag in soup.find_all(["script", "style"]):
                tag.decompose()
            soup = normalize_images(soup)
            html = build_html(title.strip(), author.strip(), date.strip(), str(soup))
            content_page = await browser.new_page()
            await content_page.set_content(html, wait_until="networkidle")
            pdf_bytes = await content_page.pdf(
                format="A4",
                print_background=True,
                margin={"top": "20mm", "bottom": "20mm", "left": "16mm", "right": "16mm"},
            )
            await content_page.close()
        else:
            pdf_bytes = await page.pdf(
                format="A4",
                print_background=True,
                margin={"top": "10mm", "bottom": "10mm", "left": "10mm", "right": "10mm"},
            )

        await browser.close()

    out_path.write_bytes(pdf_bytes)
    print(f"PDF 已保存: {out_path}")


if __name__ == "__main__":
    asyncio.run(main())
