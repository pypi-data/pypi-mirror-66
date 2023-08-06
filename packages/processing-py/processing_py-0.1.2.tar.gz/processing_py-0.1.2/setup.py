import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="processing_py", 
    version="0.1.2",
    author="Faruk Hammoud",
    author_email="farukhammoud@student-cs.fr",
    description="Graphics Library for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://py.processing.org/",
    packages=setuptools.find_packages(),
	include_package_data = True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)