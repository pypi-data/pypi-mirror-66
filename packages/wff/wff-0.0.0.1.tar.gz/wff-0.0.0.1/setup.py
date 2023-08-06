from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="wff",
    version="0.0.0.1",
    packages=["wff",],
    install_requires=[],
    license="MIT",
    url="https://github.com/reity/wff",
    author="Andrei Lapets",
    author_email="a@lapets.io",
    description="Python library for building and working " +\
                "with propositional formulas.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    test_suite="nose.collector",
    tests_require=["nose"],
)
