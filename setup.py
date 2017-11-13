#!/usr/bin/env python
import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


version = "0.1.0"


if sys.argv[-1] == "publish":
    try:
        import wheel
        print("Wheel version: ", wheel.__version__)
    except ImportError:
        print("Wheel library missing. Please run 'pip install wheel'")
        sys.exit()
    os.system("python setup.py sdist upload")
    os.system("python setup.py bdist_wheel upload")
    sys.exit()

if sys.argv[-1] == "tag":
    print("Tagging the version on git:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()


readme = open("README.rst").read()
history = open("HISTORY.rst").read().replace(".. :changelog:", "")

setup(
    name="dj-guitar",
    version=version,
    description="""Complementary core components for Django.""",
    long_description=readme + "\n\n" + history,
    author="Pascal Polleunus",
    author_email="pascal@myrty.be",
    url="https://github.com/ppo/dj-guitar",
    packages=["guitar"],
    include_package_data=True,
    python_requires=">=3.5",

    # List run-time dependencies here. These will be installed by pip when your project is installed.
    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        "django>=1.10",
        "django-model-utils>=3.0.0",
    ],
    license="MIT",
    zip_safe=False,
    keywords="django components dj-guitar",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Framework :: Django :: 1.10",
        "Framework :: Django :: 1.11",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
    ],
)
