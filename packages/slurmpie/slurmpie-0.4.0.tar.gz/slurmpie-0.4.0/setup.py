import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="slurmpie",
    version="0.4.0",
    author="Sebastian van der Voort",
    author_email="svoort25@gmail.com",
    description="Package to interact with SLURM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/svdvoort/slurmpie",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
)
