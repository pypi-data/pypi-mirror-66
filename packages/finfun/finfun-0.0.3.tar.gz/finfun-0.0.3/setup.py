import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="finfun",
    version="0.0.3",
    author="Stefan Trost",
    author_email="stefan@techscene.de",
    description="Some useful financial functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/techscene/finfun",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    python_requires='>=3.6'
)
