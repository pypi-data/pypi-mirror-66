import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fifa_preprocessing",
    version="0.3.0",
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
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    install_requires=["pandas"],
    python_requires='>=3.6',
)
