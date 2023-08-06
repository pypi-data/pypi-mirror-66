import setuptools
import os


readme_dir = os.path.dirname(__file__)
readme_path = os.path.join(readme_dir, 'README.md')
with open(readme_path, "r") as f:
    long_description = f.read()


required_packages = [
    "numpy"
]

setuptools.setup(
    name="proteinko",
    version="5.0",
    author="Stefan Stojanovic",
    author_email="stefs304@gmail.com",
    description="Encode protein sequence as a distribution of its physicochemical properties",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stefs304/proteinko",
    packages=[
        'proteinko',
    ],
    install_requires=required_packages,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Healthcare Industry",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Chemistry"
    ]
)
