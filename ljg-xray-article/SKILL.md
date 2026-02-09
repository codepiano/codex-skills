---
name: ljg-xray-article
description: 用“四层漏斗”方法透视文章并提炼可迁移的智慧晶核，支持文章 URL 或粘贴全文输入，输出结构化分析（智慧公式、论证拓扑、迁移矩阵、行动清单）。适用于“文章 X 光分析”“提炼方法论”“认知升级/迁移应用”等场景。
---

# 智慧 X 光机（Codex 版）

将文章从信息层面升级到认知结构层面，输出可迁移、可执行的智慧结论。

## 上游仓库

- Source: `https://github.com/lijigang/ljg-skill-xray-article`
- 更新同步示例：`git clone --depth=1 https://github.com/lijigang/ljg-skill-xray-article.git`

## 何时使用

当用户希望你对文章做深度分析，而不仅是摘要时使用本 skill。典型请求：
- “帮我 X 光分析这篇文章”
- “提炼这篇文章的方法论/智慧公式”
- “给出跨领域迁移和行动建议”

## 输入支持

- 文章全文（用户直接粘贴）
- 文章 URL（你负责抓取正文）

## 执行流程

### 1) 获取文章内容

- 若输入是 URL：优先获取正文内容，再提取标题、作者、来源。
- 若输入是粘贴文本：直接使用文本并识别标题（若可推断）。
- 若正文缺失或噪声过多：先告知并请求补充文本。

### 2) 四层分析（核心流程）

按以下四层顺序输出，不跳层：

1. `LAYER 1: SURFACE SCAN`
- 主题域
- 核心论点（一句话）
- 论据支撑（3-5 个）

2. `LAYER 2: DEEP PENETRATION`
- 问题意识
- 思维模型
- 隐含假设
- 反常识点

3. `LAYER 3: CORE LOCALIZATION`
- 智慧公式（形式化表达，如 `结果 = 输入 × 机制 + 条件`）
- 适用边界（成立/失效）
- 迁移潜力（3 个明显不同领域）

4. `LAYER 4: WISDOM TOPOLOGY`
- 智慧连接（对应理论/概念）
- 认知跃迁（Before -> After）
- 行动启示（3 条具体建议）

### 3) 论证拓扑图（ASCII）

用纯 ASCII 字符绘制逻辑结构图。仅使用基础符号（如 `+ - | > < / \\ * = .`），不要使用 Unicode 图形符号。

### 4) 生成输出文档

默认输出 Markdown；若用户明确要求可输出 Org-mode。内容必须包含：
- `WISDOM CORE`
- `LAYER 1-4`
- `ARGUMENT TOPOLOGY`（ASCII）
- `TRANSFER MATRIX`
- `COGNITIVE UPGRADE`
- `ACTION PROTOCOL`

### 5) 文件落地（用户要求保存时）

当用户要求“保存到本地”时：
- 生成时间戳（例如 `date +%Y%m%dT%H%M%S`）
- 文件名：`{timestamp}--xray-{slug}__read.md`（或 `__read.org`）
- 目录：`~/Documents/notes/`
- 创建目录并写入文件；需要时再打开文件。

## 质量标准

- 文字精炼、可执行，避免空泛判断。
- 智慧公式应简洁、可迁移、可指导行动。
- 迁移矩阵中的 3 个领域必须与原文领域明显不同。
- 行动建议要可立即执行（含对象/步骤/约束）。

## 参考资料（按需加载）

- 在提炼“智慧公式”、边界条件、迁移矩阵时，先读取：
  - `references/methodology.md`
- 该文件定义了四层漏斗、公式模板、迁移评估标准；不要把其内容原样复述给用户，而要用于指导分析质量。
