import os
import re

from setuptools import find_packages, setup

ROOT = os.path.dirname(__file__)

SEMVER_REGEX = r"(?P<semver>(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?)"  # noqa: E501
VERSION_RE = re.compile(r'__version__ = "' + SEMVER_REGEX + r'"')


def get_version():
    init = open(os.path.join(ROOT, "mondobrain", "__init__.py")).read()
    return VERSION_RE.search(init).group("semver")


setup(
    name="mondobrain",
    version=get_version(),
    description="MondoBrain API wrapper",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="MondoBrain",
    url="https://bitbucket.org/mondobrain/mondobrain-python",
    project_urls={
        "MondoBrain homepage": "https://mondobrain.com",
        "MondoBrain source": "https://bitbucket.org/mondobrain/mondobrain-python",
    },
    packages=find_packages(exclude=["tests*"]),
    package_data={"mondobrain": ["examples/*.md"]},
    include_package_data=True,
    license="MIT License",
    classifiers=[
        # How mature is this project?
        "Development Status :: 2 - Pre-Alpha",
        # Intended audience
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Topic :: Scientific/Engineering",
        # Language of project
        "Natural Language :: English",
        # License
        "License :: OSI Approved :: MIT License",
        # Versions supported
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        # Operating systems
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS",
    ],
    platforms="any",
    python_requires=">=3.6",
    install_requires=[
        "numpy ~= 1.18.1",
        "pandas ~= 1.0.1",
        "pyarrow ~= 0.16.0",
        "requests ~= 2.7.0",
        "scikit-learn ~= 0.22.1",
    ],
)
