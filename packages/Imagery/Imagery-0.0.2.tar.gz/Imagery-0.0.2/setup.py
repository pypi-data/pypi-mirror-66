import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Imagery", 
    version="0.0.2",
    author="Prakash",
    author_email="prankster999prakash@gmail.com",
    description="A package which aims at providing the basic intial steps required to image related operations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/prakashclt",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
