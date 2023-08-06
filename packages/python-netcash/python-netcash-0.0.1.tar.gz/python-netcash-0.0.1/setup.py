import setuptools

with open("./README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-netcash",
    version="0.0.1",
    author="Christo Crampton",
    author_email="info@38.co.za",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/schoolorchestration/libs/python-netcash",
    # packages=setuptools.find_packages(),
    packages=['netcash'],
    install_requires=['requests', 'python-benedict'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)