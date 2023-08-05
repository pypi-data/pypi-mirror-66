"""
Solve numeric optimization problems with population-based methods.

Author: Nikolay Lysenko
"""


from . import crossentropy
from .crossentropy import optimize_with_crossentropy_method


__all__ = [
    'crossentropy',
    'optimize_with_crossentropy_method',
]
