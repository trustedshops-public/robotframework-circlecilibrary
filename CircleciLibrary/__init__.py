from robot.api.deco import library
from .keywords import CircleciLibraryKeywords

__version__ = '0.1.4'

@library(version=__version__, scope="GLOBAL")
class CircleciLibrary(CircleciLibraryKeywords):
    """
    circleci keywords
    """
