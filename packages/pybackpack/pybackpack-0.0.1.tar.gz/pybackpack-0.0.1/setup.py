import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pybackpack",
    version="0.0.1",
    author="Pooya Vahidi",
    description="A collection of everyday utils, helpers and tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pvahidi/pybackpack",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)