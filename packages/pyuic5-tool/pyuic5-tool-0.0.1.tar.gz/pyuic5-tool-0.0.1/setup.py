import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyuic5-tool", # Replace with your own username
    version="0.0.1",
    author="Abdelrahman Ahmed",
    author_email="abdelatief99@gmail.com",
    description="An automation tool for pyuic5 command",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Abdelatief/Pyuic5-Tool",
    py_modules= ["converter"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

