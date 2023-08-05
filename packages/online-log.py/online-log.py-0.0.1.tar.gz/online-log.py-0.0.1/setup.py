import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="online-log.py",
    version="0.0.1",
    author="Pablo Sánchez Morillo-Velarde",
    author_email="psanchezmvelarde@gmail.com",
    description="module to generate an online endpoint to visualize flask application log",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pabloiea1995/online-log.py.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 