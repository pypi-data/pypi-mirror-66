# First Party
from setuptools import setup


def get_version():
    return open("VERSION").read().strip()


def get_requirements():
    if "a" in get_version():
        return open("requirements/alpha.txt").read().splitlines()
    return open("requirements/base.txt").read().splitlines()


setup(
    name="kubesync",
    version=get_version(),
    packages=["kubesync"],
    install_requires=get_requirements(),
    package_data={"kubesync": ["requirements/base.txt", "requirements/alpha.txt"]},
    url="https://github.com/ahmetkotan/kubesync",
    license="",
    author="ahmetkotan",
    author_email="ahmtkotan@gmail.com",
    description="Kubernetes Host to Pod Synchronization Tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    entry_points={"console_scripts": ["kubesync = kubesync.arguments:execute"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Operating System :: Unix",
    ],
)
