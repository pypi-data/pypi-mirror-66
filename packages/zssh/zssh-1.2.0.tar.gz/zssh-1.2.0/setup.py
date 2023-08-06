import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zssh",
    version="1.2.0",
    author="Aslam Anver",
    author_email="aslammohammedb@outlook.com",
    description="ZSSH - ZIP over SSH",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aslamanver/zssh",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
