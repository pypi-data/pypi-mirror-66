from setuptools import setup, find_packages
from os.path import join, dirname, basename


long_description = '''The official pytorch implementation of "*Style transfer with variational autoencoders is a promising approach to RNA-Seq data harmonization and analysis*".
The package contains a code for training and testing the model, as well as a code for working with different types of datasets.'''

with open('requirements.txt', 'r') as req_file:
    requirements = req_file.read().split('\n')


setup_requirements = ["pip>=18.1"]

authors = [
    "N. Russkikh",
    "A. Makarov",
    "D. Antonets",
    "D. Shtokalo"
]

setup(
    author = authors,
    author_email = "makarov.alxr@yandex.ru",
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Natural Language :: Russian",
        "Programming Language :: Python :: 3.7",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    description = "Style transfer variational autoencoder",
    name = "stVAE",
    long_description = long_description,
    python_requires=">=3.6",
    license = "MIT license",
    packages = find_packages(),
    setup_requires = setup_requirements,
    version = "0.1a",
    url = "https://github.com/NRshka/stvae/source"
)
