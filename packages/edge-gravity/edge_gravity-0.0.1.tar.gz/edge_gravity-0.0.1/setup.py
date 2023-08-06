from setuptools import setup
from setuptools.extension import Extension
from pathlib import Path

USE_CYTHON = "auto"

if USE_CYTHON:
    try:
        from Cython.Build import cythonize
    except ImportError:
        if USE_CYTHON == 'auto':
            USE_CYTHON = False
        else:
            raise

ext = '.pyx' if USE_CYTHON else '.c'

extension = Extension(name="edge_gravity.edge_gravity",
                      sources=["edge_gravity/edge_gravity" + ext])

if USE_CYTHON:
    extensions = cythonize(extension)

setup(
    name="edge_gravity",
    version="0.0.1",
    author="Lukas Erhard",
    author_email="luerhard@googlemail.com",
    include_package_data=True,
    description="Calculates Edge Gravity for a given networkx DiGraph",
    url="https://github.com/luerhard/edge_gravity/",
    license="MIT",
    keywords="edge gravity network networkx graph edgegravity",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=["edge_gravity"],
    install_requires=["networkx"],
    python_requires=">=3.6",
    ext_modules=extensions
)
