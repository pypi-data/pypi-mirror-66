import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="econlib",
    version="0.0.2",
    author="Jianghao Chu",
    author_email="jianghaochu@gmail.com",
    description="A package for econometric models and methods",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jianghaochu/econlib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)