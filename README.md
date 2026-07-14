# Alfred Multiline → Single

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Alfred](https://img.shields.io/badge/Alfred-4%2B%20Powerpack-purple.svg)](https://www.alfredapp.com/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![CI](https://github.com/revolyw/alfred-multiline-to-single/actions/workflows/ci.yml/badge.svg)](https://github.com/revolyw/alfred-multiline-to-single/actions/workflows/ci.yml)
[![GitHub release](https://img.shields.io/github/v/release/revolyw/alfred-multiline-to-single?include_prereleases)](https://github.com/revolyw/alfred-multiline-to-single/releases)

[English](README.en.md) · 简体中文

将**多行文本**转成**单行文本**的 Alfred Workflow。输入后可用 ↑↓ 选择包裹符与分隔符模式，回车复制结果。

## 功能

- 默认读取**剪贴板**中的多行文本（也支持关键词参数 / 选中文本热键）
- 上下选择转换模式：

  | 模式 | 示例输出 |
  | --- | --- |
  | 单引号 + 逗号 | `'apple','banana','cherry'` |
  | 双引号 + 逗号 | `"apple","banana","cherry"` |
  | 单引号 + 逗号空格 | `'apple', 'banana', 'cherry'` |
  | 双引号 + 逗号空格 | `"apple", "banana", "cherry"` |

- 自动跳过空白行，并对包裹符与反斜杠做转义
- 结果复制到剪贴板，并弹出系统通知

## 要求

- macOS
- [Alfred](https://www.alfredapp.com/) 4+ 并启用 Powerpack
- Python 3.9+（macOS 自带/`python3` 可用即可）

## 安装

### 方式一：Release（推荐）

1. 打开 [Releases](https://github.com/revolyw/alfred-multiline-to-single/releases)
2. 下载 `Multiline.to.Single.alfredworkflow`
3. 双击导入 Alfred

### 方式二：从源码打包

```bash
git clone https://github.com/revolyw/alfred-multiline-to-single.git
cd alfred-multiline-to-single
./package.sh
open "Multiline to Single.alfredworkflow"
```

## 使用

1. 复制多行文本，例如：

   ```text
   apple
   banana
   cherry
   ```

2. 调出 Alfred，输入关键词 `m2s`
3. 用 ↑↓ 选择模式，回车复制结果

### 热键（可选）

在 Alfred → Preferences → Workflows → **Multiline to Single** 中为 Hotkey 节点绑定快捷键。热键参数为「Selection in macOS」，选中文本后即可触发。

### 配置

Alfred → Workflows → **Multiline to Single** → `[x]`：

- **Keyword**：触发关键词（默认 `m2s`）
- **Default mode**：结果列表置顶的模式
- **UI language**：界面语言（English / 中文）

## 社区 / Gallery

- Alfred 论坛帖：[Multiline to Single](https://www.alfredforum.com/topic/23902-multiline-to-single-join-lines-with-quotes-separators/)
- 发帖底稿：[`docs/FORUM_POST.md`](docs/FORUM_POST.md)

## 开发

```bash
# 运行测试
python3 -m unittest discover -s tests -v

# 本地试跑 Script Filter（无参数时读剪贴板）
python3 filter.py
python3 filter.py $'a\nb'

# 打包 .alfredworkflow
./package.sh
```

项目结构：

```text
├── filter.py          # Script Filter 入口
├── info.plist         # Alfred workflow 定义
├── icon.png           # 256×256 图标
├── package.sh         # 打包脚本
├── docs/FORUM_POST.md # Alfred 论坛英文帖草稿
├── tests/             # 单元测试
└── .github/           # Issue / PR 模板与 CI
```

## 贡献

欢迎 Issue 与 PR。请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 与 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。

## 安全

安全问题请按 [SECURITY.md](SECURITY.md) 私下报告，不要公开发布 exploit。

## 变更记录

见 [CHANGELOG.md](CHANGELOG.md)。

## 许可证

本项目基于 [MIT License](LICENSE) 开源。
