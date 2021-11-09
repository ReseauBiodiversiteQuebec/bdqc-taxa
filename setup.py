import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bdqc_taxa",
    version="0.0.1",
    author="Vincent Beauregard",
    author_email="vincent.beauregard@usherbrooke.ca",
    description="`BIOQC-taxa` is a python package that interface with *Biodiversité Québec*'s database to query reference taxa sources, parse their return and generate records.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ReseauBiodiversiteQuebec/bdqc-taxa",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=['bdqc_taxa'],
    python_requires=">=3.6",
)