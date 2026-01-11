# BibTeX Reference Checker - 使用指南

## 快速开始

### 1. 安装依赖

```bash
cd bib_checker
pip install -r requirements.txt
```

首次运行时，程序会自动下载ChromeDriver。

### 2. 基本使用

```bash
python main.py /path/to/your/reference.bib
```

## 命令行选项

### 完整语法

```bash
python main.py <bibfile> [选项]
```

### 可用选项

| 选项 | 说明 | 示例 |
|------|------|------|
| `--headless` | 使用无头浏览器模式（不显示浏览器窗口） | `python main.py ref.bib --headless` |
| `--delay MIN-MAX` | 设置搜索延迟范围（秒） | `python main.py ref.bib --delay 2-5` |
| `--output PATH` | 生成HTML格式的差异报告 | `python main.py ref.bib --output report.html` |
| `--verbose` 或 `-v` | 显示详细日志 | `python main.py ref.bib -v` |
| `--limit N` | 限制检查的文献数量（用于测试） | `python main.py ref.bib --limit 10` |

### 使用示例

#### 1. 标准模式（显示浏览器）
```bash
python main.py reference.bib
```

#### 2. 无头模式（推荐用于服务器或后台运行）
```bash
python main.py reference.bib --headless
```

#### 3. 自定义延迟避免触发反爬虫
```bash
python main.py reference.bib --delay 3-6
```

#### 4. 生成HTML报告
```bash
python main.py reference.bib --output report.html
```

#### 5. 组合选项
```bash
python main.py reference.bib --headless --delay 2-5 --output report.html
```

#### 6. 测试模式（只检查前10条）
```bash
python main.py reference.bib --limit 10
```

## 工作流程

### 步骤1: 解析BibTeX文件
程序读取并解析您的`.bib`文件，提取所有参考文献条目。

### 步骤2: Google Scholar搜索
对每条文献，程序会：
- 使用标题在Google Scholar搜索
- 找到最相关的结果
- 点击"Cite"按钮
- 获取BibTeX格式数据

**注意**: 此步骤可能需要较长时间，取决于文献数量和网络状况。

### 步骤3: 比对字段
程序比较原始数据和Scholar返回的数据，检测以下字段的差异：
- `author` (作者)
- `journal` / `booktitle` (期刊/会议)
- `volume` (卷)
- `number` (期)
- `pages` (页码)
- `year` (年份)
- `publisher` (出版社)
- `doi` (数字对象标识符)
- 其他元数据字段

**排除字段**:
- `ID` (引用键，如`coello2005solving`) - 保持不变
- `title` (标题) - 用于搜索，不修改

### 步骤4: 交互式审查
程序以表格形式展示所有差异，您可以：

#### 选项A: 全部修正
自动选择所有有差异的文献进行修正。

#### 选项N: 全部不修正
不修改任何内容，直接退出。

#### 选项S: 单独选择
逐条查看每个文献的差异，手动选择是否修正：
```
[1/12] coello2005solving
标题: Solving multiobjective optimization problems using an artificial immune system
  ✗ pages: 163-190 → 163--190
  ⚠ doi: (无) → 10.1007/s10710-005-2988-5

修正此条目？ (Y/N/Q):
```

#### 选项V: 查看详细信息
查看所有差异的完整详细信息。

### 步骤5: 更新文件
确认后，程序会：
1. **创建备份**: 原文件备份为 `.backup`
2. **更新字段**: 根据您的选择更新相应字段
3. **保存文件**: 覆盖原始文件
4. **生成日志**: 创建 `.update_log.json` 记录所有修改

## 输出文件

### 1. 备份文件
- **文件名**: `<原文件名>.backup`
- **内容**: 原始BibTeX文件的完整备份
- **用途**: 如需恢复，可手动替换

### 2. 更新日志
- **文件名**: `<原文件名>.update_log.json`
- **格式**: JSON
- **内容**: 记录每个修改的详细信息

示例:
```json
[
  {
    "citation_key": "coello2005solving",
    "title": "Solving multiobjective optimization problems...",
    "timestamp": "2024-01-10T15:30:45",
    "updated_fields": {
      "pages": {
        "original": "163-190",
        "new": "163--190"
      }
    }
  }
]
```

### 3. HTML报告（可选）
- **生成方式**: 使用 `--output` 参数
- **内容**: 美观的网页格式差异报告
- **用途**: 便于分享和存档

## 常见问题

### Q1: 遇到验证码怎么办？
**答**: 程序会自动检测验证码并暂停，提示您手动完成验证。完成后按Enter继续。

### Q2: 搜索速度太慢？
**答**: 
- 使用 `--limit N` 参数限制检查数量
- 减小延迟范围（注意：可能触发反爬虫）
- 使用 `--headless` 模式提升性能

### Q3: 如果程序中断了怎么办？
**答**: 程序会保存临时日志到 `bib_checker.log`。重新运行即可，已创建的备份文件不会被覆盖（会添加时间戳）。

### Q4: 某些文献找不到怎么办？
**答**: 
- Scholar搜索失败的文献会被跳过
- 检查日志文件查看详细原因
- 可能是标题格式问题或文献较新/较旧

### Q5: 如何撤销修改？
**答**: 使用备份文件恢复：
```bash
cp reference.bib.backup reference.bib
```

### Q6: 作者名格式不一致怎么办？
**答**: 程序会进行智能规范化比较，忽略：
- 大小写差异
- 空格差异
- 标点符号差异

但仍建议手动检查关键文献。

## 高级技巧

### 1. 批量处理多个文件
创建Shell脚本：
```bash
#!/bin/bash
for file in *.bib; do
    echo "Processing $file..."
    python main.py "$file" --headless --delay 3-5
done
```

### 2. 定期验证
将检查器加入定期任务（cron）：
```bash
0 2 * * 0 python /path/to/main.py /path/to/reference.bib --headless
```

### 3. 自定义忽略字段
编辑 `comparator.py` 中的 `EXCLUDED_FIELDS` 列表。

### 4. 查看详细日志
```bash
python main.py reference.bib -v 2>&1 | tee output.log
```

## 性能建议

1. **首次运行**: 使用小数据集测试（`--limit 5`）
2. **大文件**: 使用无头模式（`--headless`）
3. **避免封禁**: 设置较长延迟（`--delay 3-6`）
4. **网络不稳定**: 使用详细日志模式（`-v`）

## 技术限制

- **Google Scholar限制**: 频繁访问可能触发验证码或临时封禁
- **搜索准确性**: 依赖Scholar搜索结果的相关性
- **特殊字符**: LaTeX特殊字符可能需要手动调整
- **中文文献**: 可能需要额外配置

## 故障排除

### ChromeDriver错误
```bash
# 手动更新ChromeDriver
pip install --upgrade webdriver-manager
```

### 解析错误
```bash
# 检查BibTeX文件格式
python -c "import bibtexparser; bibtexparser.load(open('reference.bib'))"
```

### 网络问题
```bash
# 测试连接
curl -I https://scholar.google.com
```

## 贡献与反馈

如发现问题或有改进建议，请检查日志文件 `bib_checker.log` 并报告详细错误信息。

## 版本信息

- **版本**: 1.0.0
- **Python要求**: 3.7+
- **主要依赖**: selenium, bibtexparser, colorama, tabulate
