import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chexampletest", #change to packet name
    version="0.0.1",
    author="Charlie Hodgkinson",
    author_email="charlotte.hodgkinson4@gmail.com",
    description="A small example package", #update
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject", #update
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", #update
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)