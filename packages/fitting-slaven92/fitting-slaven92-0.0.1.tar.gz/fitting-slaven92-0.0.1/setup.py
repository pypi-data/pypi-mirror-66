import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fitting-slaven92", # Replace with your own username
    version="0.0.1",
    author="Slaven Tepsic",
    author_email="stepsic@icfo.eu",
    description="fitting personal data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/slaven92/fitting",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)