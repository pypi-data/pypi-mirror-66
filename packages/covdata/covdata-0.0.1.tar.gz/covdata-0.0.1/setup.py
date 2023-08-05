import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="covdata",
    version="0.0.1",
    author="Dripta senapati",
    author_email="driptasenapati97@gmail.com",
    description="A package that can grap all data of Covid-19 cases in India",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kalyaniuniversity/covidindia",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
