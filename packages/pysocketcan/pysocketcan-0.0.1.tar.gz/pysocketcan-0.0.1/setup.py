import setuptools

with open("README.md", "r") as rm:
    long_description = rm.read()

with open("requirements.txt") as r:
    requirements = r.readlines()

setuptools.setup(
    name="pysocketcan",
    version="0.0.1",
    author="Tj Bruno",
    author_email="Tbruno25@gmail.com",
    description="Python wrapper around common Linux SocketCAN commands",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tbruno25/pysocketcan",
    install_requires=requirements,
    packages=setuptools.find_packages(),
)
