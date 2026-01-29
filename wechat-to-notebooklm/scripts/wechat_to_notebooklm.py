#!/usr/bin/env python3
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

# 如果 nlm CLI 的命令/参数有变化，请更新这里。
# tmc/nlm (Go 版): https://github.com/tmc/nlm
NLM_LIST_CMD = ["nlm", "list"]
NLM_CREATE_CMD = ["nlm", "create", "{title}"]
NLM_ADD_FILE_CMD = ["nlm", "add", "{notebook}", "{file}"]


def run(cmd, timeout):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(cmd, returncode=124, stdout="", stderr=f"Command timed out after {timeout}s")


def list_notebooks(timeout):
    result = run(NLM_LIST_CMD, timeout=timeout)
    if result.returncode != 0:
        return None, result.stderr.strip() or result.stdout.strip()
    # CLI 输出为可读文本，直接返回
    return result.stdout.strip(), None


def prompt_notebook_id(listing_text):
    if listing_text:
        print("可用的 notebooks:")
        print(listing_text)
    return input("输入 notebook id（或直接回车创建新 notebook）: ").strip()


def create_notebook(title, timeout):
    cmd = [c.format(title=title) for c in NLM_CREATE_CMD]
    result = run(cmd, timeout=timeout)
    if result.returncode != 0:
        print(result.stderr.strip() or result.stdout.strip())
        return None
    output = (result.stdout or "").strip()
    # Expected format: "Created notebook: <id>" or "notebook <id>"
    match = re.search(r"[0-9a-fA-F-]{36}", output)
    if match:
        return match.group(0)
    return output


def add_to_notebook(notebook_id, pdf_path, timeout):
    cmd = [c.format(notebook=notebook_id, file=pdf_path) for c in NLM_ADD_FILE_CMD]
    result = run(cmd, timeout=timeout)
    if result.returncode == 0:
        print(result.stdout.strip())
        return True
    print(result.stderr.strip() or result.stdout.strip())
    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="微信公众号文章 URL")
    parser.add_argument("--out", help="输出 PDF 路径（默认使用文章标题）")
    parser.add_argument("--notebook-id", help="上传到指定 notebook id")
    parser.add_argument("--new-title", help="先创建 notebook（标题）再上传")
    parser.add_argument("--list-only", action="store_true", help="仅列出 notebooks 并退出")
    parser.add_argument("--chrome-path", help="指定本地 Chrome/Chromium 可执行文件路径")
    parser.add_argument("--headed", action="store_true", help="使用有界面模式（非 headless）")
    parser.add_argument("--pdf-path", help="已有 PDF 路径（跳过生成）")
    parser.add_argument("--nlm-timeout", type=int, default=60, help="nlm CLI 超时（秒）")
    args = parser.parse_args()

    # Step 1: generate PDF (unless provided)
    if args.pdf_path:
        pdf_path = Path(args.pdf_path).expanduser().resolve()
    else:
        script_dir = Path(__file__).resolve().parent
        pdf_script = script_dir / "wechat_to_pdf.py"
        pdf_cmd = [sys.executable, str(pdf_script), "--url", args.url]
        pdf_path = None
        if args.out:
            pdf_path = Path(args.out).expanduser().resolve()
            pdf_cmd.extend(["--out", str(pdf_path)])
        if args.chrome_path:
            pdf_cmd.extend(["--chrome-path", args.chrome_path])
        if args.headed:
            pdf_cmd.append("--headed")
        result = subprocess.run(pdf_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(result.stderr.strip() or result.stdout.strip())
            sys.exit(result.returncode)
        if not pdf_path:
            output = (result.stdout or "") + "\n" + (result.stderr or "")
            match = re.search(r"^OUTPUT_PATH:\s*(.+)$", output, re.MULTILINE)
            if not match:
                print("未能解析生成的 PDF 路径。请使用 --out 指定输出路径。")
                sys.exit(1)
            pdf_path = Path(match.group(1)).expanduser().resolve()

    # Step 2: list notebooks or create/upload
    listing, err = list_notebooks(args.nlm_timeout)
    if listing is None:
        print("无法列出 notebooks，错误/输出如下:")
        print(err)
        listing = ""

    if args.list_only:
        if listing:
            print(listing)
        return

    notebook_id = args.notebook_id
    if args.new_title and notebook_id:
        print("请只提供 --notebook-id 或 --new-title 其中一个。")
        sys.exit(1)

    if args.new_title:
        created = create_notebook(args.new_title, args.nlm_timeout)
        if not created:
            print("创建 notebook 失败。若认证过期，请运行: nlm auth")
            sys.exit(1)
        notebook_id = created
        print(f"已创建 notebook: {notebook_id}")

    if not notebook_id:
        notebook_id = prompt_notebook_id(listing)
        if not notebook_id:
            title = input("输入新 notebook 标题: ").strip()
            if not title:
                print("未提供 notebook id 或标题，已终止。")
                sys.exit(1)
            created = create_notebook(title, args.nlm_timeout)
            if not created:
                print("创建 notebook 失败。若认证过期，请运行: nlm auth")
                sys.exit(1)
            notebook_id = created
            print(f"已创建 notebook: {notebook_id}")

    if not add_to_notebook(notebook_id, str(pdf_path), args.nlm_timeout):
        print("上传失败。若认证过期，请运行: nlm auth")
        sys.exit(1)


if __name__ == "__main__":
    main()
