import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="expand_string",
    version="0.0.1",
    author="J. A. Odur",
    author_email="odurjoseph8@gmail.com",
    description="A helper package for expanding strings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ja-odur/exapnd-string",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)
