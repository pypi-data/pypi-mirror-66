import setuptools
from setuptools import setup, find_packages

with open(f"README.md", "r") as file:
    description = file.read()

setup(
    name="server-automation-setup",
    version='0.3.1',
    install_requires=["pyyaml", "fabric", "pyinvoke", "paramiko"],
    # Fuck you setuptools... It keeps excluding everything in the root directory because it feels like it
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>3.0',
    # install_requires
    author="miversen33",
    author_email="miversen33@gmail.com",
    description="A helper program that will setup a remote server for you",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/miversen33/Server-Automation-Setup",
    entry_points={
        "console_scripts": [
            "serverautomation = serverautomation.__main__:main"
        ]
    }
)