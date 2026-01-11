# BibTeX Reference Checker

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Version](https://img.shields.io/badge/version-1.1.0-brightgreen.svg)
![Status](https://img.shields.io/badge/status-stable-success.svg)

[English](#english) | [中文](#中文)

---

## English

Automatically verify and correct BibTeX references using Google Scholar.

### ✨ Features

- **Automated Verification**: Search and validate references via Google Scholar
- **Smart Title Matching**: Detect incorrect search results (v1.1.0)
- **Batch Comparison**: Check authors, volume, issue, pages, and more
- **Interactive Review**: Table-based diff display with manual confirmation
- **Safe & Reliable**: Automatic backup, preserves citation keys
- **Report Generation**: JSON logs and HTML reports

### 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Test environment
python test_setup.py

# Run checker
python main.py reference.bib
```

### 📖 Usage

```bash
# Basic usage
python main.py reference.bib

# Headless mode (recommended)
python main.py reference.bib --headless --delay 3-5

# Generate HTML report
python main.py reference.bib --output report.html

# Test with limited entries
python main.py reference.bib --limit 10
```

### 🆕 What's New in v1.1.0

**Smart Title Matching**: Prevents using incorrect search results
- Automatically validates title similarity between original and Scholar results
- Marks entries with >1 word difference as "title mismatch"
- Excludes mismatched entries from auto-correction
- Case differences use Scholar's version

See [CHANGELOG.md](CHANGELOG.md) for details.

### 📚 Documentation

- [QUICKSTART.md](QUICKSTART.md) - 5-minute tutorial
- [USAGE_GUIDE.md](USAGE_GUIDE.md) - Detailed usage guide
- [FAQ.md](FAQ.md) - Common questions & answers
- [CHANGELOG.md](CHANGELOG.md) - Version history

### ⚙️ Requirements

- Python 3.7+
- Chrome browser
- Internet access to Google Scholar

### ⚠️ Important Notes

- **Test first**: Use `--limit 10` to test on a small dataset
- **Reasonable delays**: Use 3-5 second delays to avoid rate limiting
- **CAPTCHA handling**: Program pauses when detected; solve manually
- **Manual review**: Always verify important references

### 📝 License

This project is open source. See [LICENSE](LICENSE) for details.

### 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

### 📧 Contact

For questions or issues, please open an issue on GitHub.

---

## 中文

通过 Google Scholar 自动验证和修正 BibTeX 参考文献。

### ✨ 功能特性

- **自动验证**: 通过 Google Scholar 搜索并验证参考文献
- **智能标题匹配**: 自动检测错误的搜索结果 (v1.1.0)
- **批量比对**: 检查作者、卷期号、页码等字段差异
- **交互式审查**: 表格展示差异，人工确认修正
- **安全可靠**: 自动备份，保留原始引用键
- **报告生成**: JSON 日志和 HTML 美观报告

### 🚀 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 测试环境
python test_setup.py

# 运行检查
python main.py reference.bib
```

### 📖 使用方法

```bash
# 基本用法
python main.py reference.bib

# 无头模式（推荐）
python main.py reference.bib --headless --delay 3-5

# 生成HTML报告
python main.py reference.bib --output report.html

# 测试模式（只检查前10条）
python main.py reference.bib --limit 10
```

### 🆕 v1.1.0 新功能

**智能标题匹配**: 避免使用错误的文献数据
- 自动验证搜索结果标题与原标题的相似度
- 超过1个单词差异会被标记为"标题不匹配"
- 标题不匹配的文献不会被自动修正
- 大小写差异使用 Scholar 的版本

详见 [CHANGELOG.md](CHANGELOG.md)。

### 📚 文档

- [QUICKSTART.md](QUICKSTART.md) - 5分钟快速上手
- [USAGE_GUIDE.md](USAGE_GUIDE.md) - 详细使用指南
- [FAQ.md](FAQ.md) - 常见问题解答
- [CHANGELOG.md](CHANGELOG.md) - 版本更新历史

### ⚙️ 系统要求

- Python 3.7+
- Chrome 浏览器
- 能访问 Google Scholar

### ⚠️ 重要提示

- **先测试**: 使用 `--limit 10` 先测试小数据集
- **合理延迟**: 使用 3-5 秒延迟避免被封禁
- **验证码处理**: 遇到验证码需手动完成
- **人工复核**: 重要文献建议人工核对

### 📝 许可证

本项目开源，详见 [LICENSE](LICENSE)。

### 🤝 贡献

欢迎贡献！您可以：
- 报告 Bug
- 提出新功能建议
- 提交 Pull Request

### 📧 联系方式

如有问题，请在 GitHub 上提交 Issue。
