from setuptools import setup
from setuptools.extension import Extension
from pathlib import Path
from Cython.Build import cythonize

setup(
    name="edge_gravity",
    version="0.0.3",
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
    ext_modules=cythonize("edge_gravity/edge_gravity.pyx"),
)
