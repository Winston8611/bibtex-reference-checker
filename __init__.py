"""
BibTeX参考文献检查器包
"""

__version__ = '1.0.0'
__author__ = 'BibTeX Checker Team'

from .parser import BibTeXParser, parse_bibtex_string
from .scholar_scraper import ScholarScraper
from .comparator import FieldComparator, EntryComparison, DifferenceType
from .file_updater import FileUpdater
from .interactive_review import InteractiveReviewer

__all__ = [
    'BibTeXParser',
    'parse_bibtex_string',
    'ScholarScraper',
    'FieldComparator',
    'EntryComparison',
    'DifferenceType',
    'FileUpdater',
    'InteractiveReviewer',
]
