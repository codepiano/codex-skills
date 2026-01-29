#!/usr/bin/env python3
import argparse
from pathlib import Path

import requests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="微信公众号文章 URL")
    parser.add_argument(
        "--out",
        default="wechat-article.html",
        help="输出 HTML 路径",
    )
    parser.add_argument("--timeout", type=int, default=20)
    args = parser.parse_args()

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
    resp = requests.get(args.url, headers=headers, timeout=args.timeout)
    resp.raise_for_status()

    out_path = Path(args.out).expanduser().resolve()
    out_path.write_text(resp.text, encoding="utf-8")
    print(f"HTML 已保存: {out_path}")


if __name__ == "__main__":
    main()
