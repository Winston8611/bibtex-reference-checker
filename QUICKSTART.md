# Quick Start Guide

Get started with BibTeX Reference Checker in 5 minutes.

## Step 1: Install Dependencies (1 min)

```bash
cd bib_checker
pip install -r requirements.txt
```

ChromeDriver will be downloaded automatically on first run.

## Step 2: Test Installation (1 min)

```bash
python test_setup.py
```

All checks should show ✓.

## Step 3: Try Sample File (2 min)

```bash
# Test with sample file (limit to 3 entries)
python main.py sample.bib --limit 3
```

## Step 4: Check Your File

```bash
# Test with first 10 entries
python main.py /path/to/your/reference.bib --limit 10

# If everything looks good, run full check
python main.py /path/to/your/reference.bib --headless --delay 3-5
```

## Step 5: Review and Confirm

The program will display differences found. You can:
- **[A]** Accept all corrections
- **[N]** Reject all
- **[S]** Select individually
- **[V]** View detailed information

## Important Notes

⚠️ **Always test first** with `--limit 10`  
⚠️ **Use reasonable delays** (3-5 seconds recommended)  
⚠️ **CAPTCHA handling**: Program pauses; solve manually  
⚠️ **Automatic backup**: Original file backed up as `.backup`

## Common Commands

| Purpose | Command |
|---------|---------|
| Basic check | `python main.py file.bib` |
| Headless mode | `python main.py file.bib --headless` |
| Test mode | `python main.py file.bib --limit 10` |
| Generate report | `python main.py file.bib --output report.html` |
| Slow mode (safe) | `python main.py file.bib --delay 3-6` |

## Troubleshooting

**Problem**: Installation fails  
**Solution**: Try `pip install --upgrade pip` first

**Problem**: ChromeDriver error  
**Solution**: Will auto-download on first run

**Problem**: Can't find entries  
**Solution**: Check if title has special characters

## Next Steps

- Read [USAGE_GUIDE.md](USAGE_GUIDE.md) for detailed documentation
- Check [FAQ.md](FAQ.md) for common questions
- Run with your actual BibTeX file

## Expected Behavior

### Normal Match
```
✓ Title matches → Compare fields → Show differences → User confirms
```

### Title Mismatch (v1.1.0)
```
⚠️ Title doesn't match (>1 word different)
→ Mark as "needs manual review"
→ Skip automatic correction
→ Show in separate warning section
```

## Performance

- **Speed**: ~3-5 seconds per entry (depends on delay setting)
- **100 entries**: ~30-60 minutes (headless mode)
- **Recommendation**: Process large files in batches

---

**Need help?** Check [FAQ.md](FAQ.md) or open an issue on GitHub.
