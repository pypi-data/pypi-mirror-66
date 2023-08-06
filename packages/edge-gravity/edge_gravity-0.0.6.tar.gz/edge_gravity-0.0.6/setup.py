from distutils.core import setup
from distutils.extension import Extension
from pathlib import Path

try:
    from Cython.Distutils import build_ext
except ImportError:
    use_cython = False
else:
    use_cython = True

ext_modules = []
cmd_class = {}

if use_cython:
    print("use cython")
    ext_modules += [
        Extension(name="edge_gravity.edge_gravity",
                  sources=["edge_gravity/edge_gravity.pyx"])
    ]
    cmd_class.update({"build_ext": build_ext})
else:
    ext_modules += [
        Extension(name="edge_gravity.edge_gravity",
                  sources=["edge_gravity/edge_gravity.c"])
    ]

setup(
    name="edge_gravity",
    version="0.0.6",
    author="Lukas Erhard",
    author_email="luerhard@googlemail.com",
    description="Calculates Edge Gravity for a given networkx DiGraph",
    url="https://github.com/luerhard/edge_gravity/",
    license="MIT",
    keywords="edge gravity network networkx graph edgegravity",
    long_description="use 'from edge_gravity.edge_gravity import edge_gravity to use",
    packages=["edge_gravity"],
    ext_modules=ext_modules,
    cmdclass=cmd_class
)
