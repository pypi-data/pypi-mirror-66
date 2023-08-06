import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jzip",
    version="1.0.0",
    author="Jilani Shaik",
    author_email="iammrj.java@gmail.com",
    description="JZip is a general purpose utility to uncompress the GZipped content in base64 to plain base64 or into files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iammrj/JZip",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)