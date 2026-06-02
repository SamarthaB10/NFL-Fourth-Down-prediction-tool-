"""Build the C++ possession simulator: pip install pybind11 && python setup_sim.py build_ext --inplace"""

from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup

ext_modules = [
    Pybind11Extension(
        "nfl4d_sim",
        ["simulation/bindings.cpp", "simulation/possession_sim.cpp"],
        include_dirs=["simulation"],
        cxx_std=17,
    ),
]

setup(
    name="nfl4d_sim",
    version="0.1.0",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
)
