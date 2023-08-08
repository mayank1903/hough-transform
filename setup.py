import setuptools
from setuptools import find_packages
import pip


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def get_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        requires = fh.read().split("\n")
        requires = [r.strip() for r in requires if len(r.strip()) > 0]
        gh = [r for r in requires if "github" in r]
        pypi = list(set(requires) - set(gh))
        # setting global variable for setuptools.setup method
        requires = pypi

        # installing github repos directly
        for g in gh:
            pip.main(["install", g])

        return requires

setuptools.setup(
    name='hough-transform',
    packages=find_packages(),
    version='0.1.0',
    description='Repo for hough transform',
    author='mayank1903',
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mayank1903/hough-transform",
    project_urls={"Bug Tracker": "https://github.com/mayank1903/hough-transform/issues"},
    install_requires=get_requirements(),
)