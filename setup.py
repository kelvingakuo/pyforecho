import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyforecho",
    version="0.0.1",
    author="Kelvin Gakuo",
    author_email="kelvingakuo@gmail.com",
    description="Python wrapper for the Echo Mobile API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kelvingakuo/pyforecho",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests==2.25.0"
    ],
	python_requires = ">3.6.0",
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)