import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aos-api-connector",
    version="0.1.0",
    author="Bjarne Kohnke",
    author_email="python@kohnkemail.de",
    description="Collection of API functions for Aruba products.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Linkk93/aos_api_connector",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)