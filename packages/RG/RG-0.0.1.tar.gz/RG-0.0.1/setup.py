import setuptools


setuptools.setup(
    name="RG",
    version="0.0.1",
    author="Ryan Gosselin",
    author_email="ryan.gosselin@usherbrooke.ca",
    url="https://www.usherbrooke.ca/gchimiquebiotech/departement/professeurs/ryan-gosselin/",
    packages=["RG"],
    description="Ryan's go-to Python functions",
    long_description="Miscellaneous functions:\
    \n\nfct_xlsread\
    \nfct_regress\
    \nfct_R2\
    \nfct_PCA\
    \nfct_PLS\
    \nfct_snv\
    \nfct_colorspectra",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)