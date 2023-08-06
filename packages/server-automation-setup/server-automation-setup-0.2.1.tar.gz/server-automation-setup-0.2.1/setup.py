import setuptools

PACKAGE = 'serverautomation'

with open(f"{PACKAGE}/README.md", "r") as file:
    description = file.read()

setuptools.setup(
    name="server-automation-setup",
    version='0.2.1',
    author="miversen33",
    author_email="miversen33@gmail.com",
    description="A helper program that will setup a remote server for you",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/miversen33/Server-Automation-Setup",
    packages='./',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>3.0',
)