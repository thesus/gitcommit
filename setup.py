import setuptools

setuptools.setup(
    name="igit-pkg",
    version="0.0.1",
    description="intelligent git",
    scripts=['igit'],
    url="https://gitlab.lrz.de/ge39rec/gitcommit",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)
