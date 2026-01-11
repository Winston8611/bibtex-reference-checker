# Contributing to BibTeX Reference Checker

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Ways to Contribute

### 🐛 Report Bugs

Found a bug? Please open an issue with:
- **Clear title**: Brief description of the problem
- **Steps to reproduce**: How to trigger the bug
- **Expected vs actual behavior**: What should happen vs what happens
- **Environment**: Python version, OS, browser version
- **Log file**: Attach `bib_checker.log` if available

### 💡 Suggest Features

Have an idea? Open an issue with:
- **Feature description**: What you'd like to see
- **Use case**: Why this would be useful
- **Possible implementation**: Your thoughts on how to implement it (optional)

### 📝 Improve Documentation

Documentation improvements are always welcome:
- Fix typos or unclear explanations
- Add examples
- Translate to other languages
- Improve README or guides

### 🔧 Submit Code

Want to contribute code? Great!

## Development Setup

1. **Fork and clone**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/bib_checker.git
   cd bib_checker
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run tests**:
   ```bash
   python test_setup.py
   python test_title_matching.py
   ```

## Code Style

- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and small
- Add comments for complex logic

## Making Changes

1. **Create a branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Write clear, focused commits
   - Test your changes thoroughly

3. **Test**:
   ```bash
   # Run existing tests
   python test_setup.py
   python test_title_matching.py
   
   # Test with sample file
   python main.py sample.bib --limit 3
   ```

4. **Commit**:
   ```bash
   git add .
   git commit -m "Add: brief description of changes"
   ```

   Commit message prefixes:
   - `Add:` for new features
   - `Fix:` for bug fixes
   - `Update:` for improvements
   - `Doc:` for documentation
   - `Refactor:` for code restructuring

5. **Push and create PR**:
   ```bash
   git push origin feature/your-feature-name
   ```
   
   Then open a Pull Request on GitHub with:
   - Clear description of changes
   - Related issue number (if applicable)
   - Screenshots (if UI changes)

## Areas for Contribution

Looking for where to start? Consider:

### Easy
- Improve error messages
- Add more test cases
- Update documentation
- Fix typos

### Medium
- Add configuration file support
- Improve progress reporting
- Add more output formats (CSV, Excel)
- Enhance title matching algorithm

### Advanced
- Add support for other search engines (CrossRef, Semantic Scholar)
- Implement parallel processing
- Create GUI interface
- Add plugin system

## Code Review Process

1. Maintainers will review your PR
2. They may suggest changes or improvements
3. Make requested changes
4. Once approved, your PR will be merged!

## Testing Guidelines

When adding new features:
- Add test cases in `test_*.py` files
- Ensure all existing tests still pass
- Test edge cases
- Document test scenarios

## Documentation Guidelines

When updating docs:
- Keep language clear and concise
- Provide examples where helpful
- Update CHANGELOG.md for user-facing changes
- Ensure Chinese and English docs match (if applicable)

## Questions?

Not sure about something? Feel free to:
- Open an issue asking for clarification
- Reach out to maintainers
- Check existing issues and PRs for similar questions

## Code of Conduct

- Be respectful and constructive
- Welcome newcomers
- Focus on what's best for the project
- Give credit where it's due

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing!** Every contribution, no matter how small, makes this project better. 🎉
