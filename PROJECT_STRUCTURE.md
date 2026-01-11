# Project Structure

## 📁 Directory Layout

```
bib_checker/
│
├── 📄 README.md                    # Project homepage (EN/ZH)
├── 📄 LICENSE                      # MIT License
├── 📄 CONTRIBUTING.md              # Contribution guide
├── 📄 CHANGELOG.md                 # Version history
├── 📄 QUICKSTART.md                # 5-minute tutorial
├── 📄 FAQ.md                       # Common questions
├── 📄 USAGE_GUIDE.md               # Detailed documentation
│
├── ⚙️ requirements.txt             # Python dependencies
├── ⚙️ .gitignore                   # Git ignore rules
├── ⚙️ config.ini.example           # Configuration template
│
├── 🐍 main.py                      # Main entry point
├── 🐍 parser.py                    # BibTeX parser
├── 🐍 scholar_scraper.py           # Google Scholar scraper
├── 🐍 comparator.py                # Field comparison
├── 🐍 interactive_review.py        # Interactive UI
├── 🐍 file_updater.py              # File updater
├── 🐍 __init__.py                  # Package initialization
│
├── 🧪 test_setup.py                # Environment test
├── 🧪 test_title_matching.py       # Title matching test
└── 📝 sample.bib                   # Sample BibTeX file
```

## 📊 File Statistics

| Category | Files | Lines |
|----------|-------|-------|
| Documentation | 7 | ~1,800 |
| Source Code | 7 | ~2,000 |
| Tests | 2 | ~200 |
| Configuration | 3 | ~100 |
| **Total** | **19** | **~4,100** |

## 📚 Documentation Files

### README.md
- **Purpose**: Project homepage and overview
- **Language**: English + Chinese (bilingual)
- **Contains**: Features, quick start, installation

### QUICKSTART.md
- **Purpose**: Get started in 5 minutes
- **Audience**: New users
- **Contains**: Step-by-step tutorial

### USAGE_GUIDE.md
- **Purpose**: Comprehensive user manual
- **Audience**: All users
- **Contains**: Detailed usage, parameters, examples

### FAQ.md
- **Purpose**: Common questions and answers
- **Audience**: Troubleshooting users
- **Contains**: 27 Q&A covering installation to advanced usage

### CHANGELOG.md
- **Purpose**: Version history
- **Audience**: All users
- **Contains**: v1.0.0 and v1.1.0 changes

### CONTRIBUTING.md
- **Purpose**: Developer guide
- **Audience**: Contributors
- **Contains**: Setup, coding style, PR process

### LICENSE
- **Purpose**: Legal terms
- **Type**: MIT License
- **Year**: 2026

## 🐍 Source Code Modules

### main.py (256 lines)
- **Role**: Entry point and orchestration
- **Features**: CLI argument parsing, workflow coordination
- **Key Functions**: `main()`, `setup_logging()`

### parser.py (196 lines)
- **Role**: BibTeX file parsing and manipulation
- **Features**: Parse, update, save, backup
- **Key Classes**: `BibTeXParser`

### scholar_scraper.py (280 lines)
- **Role**: Google Scholar automation
- **Features**: Search, extract BibTeX, batch processing
- **Key Classes**: `ScholarScraper`

### comparator.py (358 lines)
- **Role**: Field comparison and validation
- **Features**: Title matching, field normalization, diff detection
- **Key Classes**: `FieldComparator`, `EntryComparison`

### interactive_review.py (281 lines)
- **Role**: User interface for review
- **Features**: Display diffs, interactive selection
- **Key Classes**: `InteractiveReviewer`

### file_updater.py (371 lines)
- **Role**: File updates and reporting
- **Features**: Backup, update, HTML report generation
- **Key Classes**: `FileUpdater`

### __init__.py (16 lines)
- **Role**: Package initialization
- **Exports**: Main classes for programmatic use

## 🧪 Test Files

### test_setup.py (114 lines)
- **Purpose**: Environment verification
- **Tests**: Dependencies, modules, ChromeDriver
- **Run**: `python test_setup.py`

### test_title_matching.py (120 lines)
- **Purpose**: Title matching algorithm validation
- **Tests**: 7 test cases covering various scenarios
- **Run**: `python test_title_matching.py`

## ⚙️ Configuration Files

### requirements.txt
```
bibtexparser>=1.4.0
selenium>=4.15.0
webdriver-manager>=4.0.0
colorama>=0.4.6
tabulate>=0.9.0
```

### .gitignore
- Python artifacts (__pycache__, *.pyc)
- Virtual environments
- IDE files
- Log files
- Backup files
- ChromeDriver

### config.ini.example
- Sample configuration template
- Users can copy to `config.ini` and customize
- Not currently used by code (future feature)

## 🎯 Key Features by Module

### Title Matching (v1.1.0)
- **Module**: `comparator.py`
- **Functions**: `normalize_title()`, `calculate_title_match_score()`
- **Logic**: Allows ≤1 word difference, ignores case/punctuation

### Google Scholar Integration
- **Module**: `scholar_scraper.py`
- **Features**: Auto-search, click Cite, extract BibTeX
- **Anti-bot**: Random delays, user-agent spoofing, CAPTCHA detection

### Interactive Review
- **Module**: `interactive_review.py`
- **Features**: Table display, color output, multiple selection modes
- **Options**: Accept all, reject all, select individually

### Safe Updates
- **Module**: `file_updater.py`
- **Features**: Auto-backup, JSON logs, HTML reports
- **Safety**: No changes without confirmation

## 🚀 Entry Points

### For Users
```bash
python main.py reference.bib
```

### For Developers
```python
from bib_checker import BibTeXParser, ScholarScraper, FieldComparator

# Use as library
parser = BibTeXParser('file.bib')
entries = parser.get_entries()
```

## 📦 Dependencies

### Production
- `bibtexparser`: BibTeX parsing
- `selenium`: Browser automation
- `webdriver-manager`: ChromeDriver management
- `colorama`: Colored terminal output
- `tabulate`: Table formatting

### Development
- Standard library only for tests
- No additional dev dependencies

## 🔄 Workflow

```
User runs main.py
    ↓
Parse BibTeX file (parser.py)
    ↓
Search on Scholar (scholar_scraper.py)
    ↓
Compare fields (comparator.py)
    ↓
Display differences (interactive_review.py)
    ↓
User confirms changes
    ↓
Update file (file_updater.py)
    ↓
Generate reports & logs
```

## 💡 Design Principles

1. **Modular**: Each module has a single responsibility
2. **Safe**: Always backup before changes
3. **Interactive**: User confirms all changes
4. **Documented**: Comprehensive docs for all levels
5. **Tested**: Core features have test coverage
6. **Bilingual**: English and Chinese support

## 🎨 Code Quality

- **Style**: PEP 8 compliant
- **Documentation**: Docstrings on all public functions
- **Error Handling**: Try-except blocks with logging
- **Type Hints**: Gradually adding (Python 3.7+)
- **Comments**: Explain complex logic

## 📈 Future Enhancements

See CONTRIBUTING.md for areas where contributions are welcome:
- Additional search engines
- GUI interface
- Parallel processing
- More output formats
- Plugin system

---

**Last Updated**: 2026-01-11  
**Version**: 1.1.0  
**Status**: Production Ready ✅
