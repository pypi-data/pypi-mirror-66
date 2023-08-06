import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fifa_preprocessing",
    version="1.0.0",
    author="Piotr Frątczak",
    author_email="piotrfratczak99@gmail.com",
    description="A package providing methods to preprocess data, with the intent to perform Machine Learning.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/piotrfratczak/fifa_preprocessing/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
