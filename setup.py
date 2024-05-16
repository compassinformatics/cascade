import re
from setuptools import setup
from io import open


def readme():
    with open("README.rst", "r", encoding="utf-8") as f:
        return f.read()


(__version__,) = re.findall('__version__ = "(.*)"', open("cascade/__init__.py").read())

setup(
    name="cascade-rivers",
    version=__version__,
    description="Python library to assign stream order to hydrometric networks",
    long_description=readme(),
    author="Seth Girvin",
    author_email="sgirvin@compass.ie",
    url="https://github.com/compassinformatics/cascade/",
    packages=["cascade"],
    package_dir={"cascade": "cascade"},
    include_package_data=True,
    install_requires=["wayfarer>=0.12.0"],
    zip_safe=False,
    keywords="cascade",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.9",
    ],
    test_suite="tests",
    tests_require=[],
)
