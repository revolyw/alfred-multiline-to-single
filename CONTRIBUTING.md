# Contributing

感谢考虑为本项目做贡献！

Please also see the English notes below. By participating, you agree to follow
our [Code of Conduct](CODE_OF_CONDUCT.md).

## 开发环境

- macOS
- [Alfred](https://www.alfredapp.com/) 4+（需 Powerpack）
- Python 3.9+

```bash
git clone https://github.com/revolyw/alfred-multiline-to-single.git
cd alfred-multiline-to-single
python3 -m unittest discover -s tests -v
./package.sh
```

## 如何贡献

1. Fork 本仓库并创建分支（`feature/…` 或 `fix/…`）
2. 为行为变更补充或更新测试
3. 确保 `python3 -m unittest discover -s tests -v` 通过
4. 如修改了 workflow 运行时代码，执行 `./package.sh` 重新打包
5. 提交 Pull Request，描述动机、变更与测试方式

## 问题反馈

- Bug：请使用 [Bug report](https://github.com/revolyw/alfred-multiline-to-single/issues/new?template=bug_report.yml)
- 功能建议：请使用 [Feature request](https://github.com/revolyw/alfred-multiline-to-single/issues/new?template=feature_request.yml)

提 issue 时尽量包含：Alfred 版本、macOS 版本、复现步骤、期望与实际结果。

## 提交信息

建议使用清晰的祈使句，例如：

- `fix: escape backslashes before wrap chars`
- `docs: clarify hotkey setup in README`
- `test: cover empty clipboard fallback`

## English

1. Fork and create a topic branch
2. Add/update tests for behavior changes
3. Run `python3 -m unittest discover -s tests -v`
4. Rebuild with `./package.sh` if runtime files change
5. Open a PR describing why, what, and how you tested
