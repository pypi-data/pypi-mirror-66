import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cjkformat", # Replace with your own username
    version="0.1.1",
    author="Huidae Cho",
    author_email="grass4u@gmail.com",
    description="This Python 3 module provides utility functions for formatting fixed-width CJK strings.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HuidaeCho/cjkformat",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)
