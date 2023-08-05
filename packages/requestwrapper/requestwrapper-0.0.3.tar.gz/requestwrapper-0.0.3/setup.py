import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="requestwrapper", # Replace with your own username
    version="0.0.3",
    author="J.S. Kroodsma",
    author_email="j.s.kroodsma@gmail.com",
    description="A simple wrapper for the requests package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jskroodsma",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)