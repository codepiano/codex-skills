---
name: ljg-explain-words
description: 深度解构英文单词（词源、核心意象、语感辨析、语义拓扑），并生成高质量 HTML 单词卡。适用于“真正掌握一个词而非只翻译”的场景。
---

# 单词灵魂解剖师（Codex 版）

目标不是翻译，而是让用户掌握单词的“语义骨架”和使用质感。

## 上游仓库

- Source: `https://github.com/lijigang/ljg-skill-explain-words`
- 更新同步示例：`git clone --depth=1 https://github.com/lijigang/ljg-skill-explain-words.git`

## 资源文件

- HTML 模板：`assets/word_card.html`
- 生成卡片时先读取模板，再替换变量。

## 输入支持

- 一个英文单词（如 `serendipity`）
- 可选：语境偏好（学术/文学/口语）

## 执行流程

### 1) 模板加载

- 读取 `assets/word_card.html`。
- 单词标准化：小写存储，展示时首字母大写。

### 2) 深度解构

输出以下模块：
- `Definition Deep`：原始画面 + 核心意象公式 + 现代语义解释
- `Etymology`：词根拆解 + 2-3 个同源词关联
- `Nuance`：1-2 组易混词辨析（用列表）
- `Visual Topology`：Mermaid `graph TD` 语义图
- `Epiphany`：中英双语一语道破

### 3) 卡片渲染

替换模板变量：
- `{{WORD}}`
- `{{PHONETIC}}`
- `{{DEFINITION_DEEP}}`
- `{{ETYMOLOGY}}`
- `{{NUANCE_TEXT}}`
- `{{EXAMPLE_SENTENCE}}`
- `{{EPIPHANY}}`
- `{{MERMAID_CODE}}`

### 4) 写入与打开（用户要求落地时）

- 输出文件：`word_card_{word}.html`
- 保存到当前工作目录（或用户指定目录）。
- 需要时打开文件预览。

## 质量标准

- 必须体现词源与现代语义之间的桥梁。
- 语感辨析要有“可替换/不可替换”的语境差异。
- Mermaid 节点简练，结构清晰。
- Epiphany 要有洞见，不是同义改写。
