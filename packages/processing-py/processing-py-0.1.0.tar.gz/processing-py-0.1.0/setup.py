import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="processing-py", 
    version="0.1.0",
    author="Faruk Hammoud",
    author_email="farukhammoud@student-cs.fr",
    description="Graphics Library for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://py.processing.org/",
    packages=setuptools.find_packages(),
	package_data={
        'processing.py': ['*'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)