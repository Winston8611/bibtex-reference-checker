# Frequently Asked Questions (FAQ)

## Installation & Setup

### Q1: What are the system requirements?
**A**: 
- Python 3.7 or higher
- Chrome browser installed
- Internet access to Google Scholar
- Supported OS: macOS, Linux, Windows

### Q2: How do I install dependencies?
**A**: 
```bash
pip install -r requirements.txt
```

If you're in China, use a mirror:
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q3: ChromeDriver installation fails?
**A**: 
The program auto-downloads ChromeDriver on first run. If it fails:
1. Check your internet connection
2. Try using a VPN
3. Or download manually from https://chromedriver.chromium.org/

## Usage

### Q4: How do I test if it's working?
**A**: 
```bash
python test_setup.py
python main.py sample.bib --limit 3
```

### Q5: Why is it so slow?
**A**: 
- Use `--headless` mode for faster performance
- Reduce delay (carefully): `--delay 1-2`
- Process in batches: `--limit 50`

**Note**: Delays prevent rate limiting by Google Scholar.

### Q6: What happens when I see a CAPTCHA?
**A**: 
1. Program automatically pauses
2. Solve the CAPTCHA manually in the browser
3. Press Enter to continue

**Prevention**: Use longer delays (`--delay 3-6`)

### Q7: Some references not found?
**A**: 
Possible reasons:
1. **Title formatting**: Contains special LaTeX characters
2. **Not indexed**: Too new or too old for Scholar
3. **Title mismatch**: Search result differs by >1 word

Check the log file: `bib_checker.log`

### Q8: What is "title mismatch"?
**A**: 
Starting from v1.1.0, the program validates search results:

**Allowed differences** (will process):
- Case differences → Uses Scholar's case
- Punctuation differences
- ≤1 word difference (e.g., missing "The")

**Not allowed** (marked for manual review):
- >1 word difference
- Different articles

This prevents using data from wrong papers.

### Q9: How do I undo changes?
**A**: 
```bash
cp reference.bib.backup reference.bib
```

### Q10: Can I process multiple files?
**A**: 
Yes, create a shell script:

```bash
#!/bin/bash
for file in *.bib; do
    python main.py "$file" --headless --delay 3-5
done
```

## Safety & Data

### Q11: Is my original file safe?
**A**: 
Yes! The program:
- Creates `.backup` before any changes
- Requires user confirmation
- Logs all changes to `.update_log.json`

### Q12: Which fields are compared?
**A**: 
Compared: author, journal, volume, number, pages, year, publisher, doi, etc.  
**Not changed**: citation key (e.g., `smith2020paper`), title

### Q13: How to handle title mismatch warnings?
**A**: 
1. Check if original title is correct
2. Manually search on Google Scholar
3. If Scholar data is correct, update manually
4. If original is correct, keep it unchanged

## Performance

### Q14: How long for 100 references?
**A**: 
- Standard mode: 30-60 minutes
- Headless mode: 20-40 minutes
- With 3-second delays: ~5 minutes search time

Actual time depends on network speed and Scholar response.

### Q15: Can it run in parallel?
**A**: 
Not currently. Running multiple instances may trigger Scholar's anti-bot measures.

## Errors

### Q16: "ConnectionError" or network errors
**A**: 
1. Check internet connection
2. Test: `curl -I https://scholar.google.com`
3. Try VPN if Scholar is blocked
4. Increase delays

### Q17: "TimeoutException"
**A**: 
Network is slow. Increase delays or retry later.

### Q18: BibTeX parsing errors
**A**: 
1. Validate your .bib file format
2. Use online tool: http://bibtex.online
3. Check the specific entry mentioned in error

### Q19: Program crashes mid-run
**A**: 
1. Check `bib_checker.log` for details
2. Backup file is already created
3. Re-run the program (won't duplicate backups)

## Features

### Q20: Does it support Chinese references?
**A**: 
Yes, but:
- Scholar coverage of Chinese journals may be limited
- Some Chinese journal names may not match
- Recommend manual verification for important Chinese references

### Q21: What about preprints (arXiv)?
**A**: 
If indexed by Scholar, they can be found. Note:
- May find published version instead of preprint
- Check version consistency

### Q22: Supported entry types?
**A**: 
All standard BibTeX types:
- @article, @inproceedings, @book, @inbook
- @phdthesis, @mastersthesis, @techreport
- And more

## Advanced

### Q23: How to customize excluded fields?
**A**: 
Edit `comparator.py`, modify `EXCLUDED_FIELDS` list:
```python
EXCLUDED_FIELDS = ['ID', 'ENTRYTYPE', 'title', 'note']
```

### Q24: Can I adjust title matching strictness?
**A**: 
Edit `comparator.py`, in `calculate_title_match_score()`:
```python
is_match = diff_count <= 1  # Change to 0 (stricter) or 2 (looser)
```

### Q25: How to generate reports for others?
**A**: 
```bash
python main.py reference.bib --output report.html
```

Share the generated HTML file.

## Contributing

### Q26: How to report bugs?
**A**: 
Open an issue on GitHub with:
1. Error log (`bib_checker.log`)
2. Command you used
3. Python and OS version
4. Screenshots if applicable

### Q27: Can I contribute code?
**A**: 
Yes! Areas for improvement:
- Support other search engines (CrossRef, Semantic Scholar)
- GUI interface
- Parallel processing
- More output formats

## Still Need Help?

1. Check [USAGE_GUIDE.md](USAGE_GUIDE.md) for detailed documentation
2. Review `bib_checker.log` for error details
3. Run test: `python test_setup.py`
4. Open an issue on GitHub

---

**Can't find your question?** Open an issue on GitHub and we'll add it here!
