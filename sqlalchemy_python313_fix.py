"""
SQLAlchemy Python 3.13 Compatibility Fix
========================================
Workaround for Python 3.13 typing strictness issue with SQLAlchemy.
This must be imported BEFORE any SQLAlchemy imports.

Note: Python 3.13 has stricter typing checks. For production use, 
consider Python 3.11 or 3.12 until libraries fully support 3.13.
"""

import sys
import os

# Python 3.13 compatibility fix for SQLAlchemy
if sys.version_info >= (3, 13):
    # Patch SQLAlchemy's internal TypingOnly check
    # This needs to happen before SQLAlchemy imports
    
    # Method 1: Patch typing module to be less strict for SQLAlchemy
    import typing
    
    # Store original
    _original_init_subclass = typing.Generic.__init_subclass__
    
    # Create a wrapper that catches AssertionError
    def _make_patched_init_subclass():
        def patched(cls, **kwargs):
            try:
                return _original_init_subclass(**kwargs)
            except AssertionError as e:
                # Check if this is the TypingOnly error
                error_str = str(e)
                if 'TypingOnly' in error_str and 'additional attributes' in error_str:
                    # This is the SQLAlchemy Python 3.13 issue - suppress it
                    import warnings
                    warnings.filterwarnings('ignore', category=RuntimeWarning)
                    return
                raise
        return classmethod(patched)
    
    typing.Generic.__init_subclass__ = _make_patched_init_subclass()
    
    # Set environment variable
    os.environ.setdefault('SQLALCHEMY_SILENCE_UBER_WARNING', '1')

