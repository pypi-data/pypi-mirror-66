from distutils.core import setup as cysetup
from Cython.Build import cythonize

cysetup(
    ext_modules=cythonize("test.py",
                          language_level=3),
)
