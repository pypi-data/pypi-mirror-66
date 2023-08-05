from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.8',
    install_requires=[
        'pylint', "pylint_django",
        "coverage",
    ],
)
