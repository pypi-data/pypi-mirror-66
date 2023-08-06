[![Release](https://github.com/MultimediaExtensibleGit/Runtime/workflows/Release/badge.svg?event=release)](https://github.com/MultimediaExtensibleGit/Runtime/releases/latest) [![Build](https://github.com/MultimediaExtensibleGit/Runtime/workflows/Build/badge.svg?branch=master)](https://github.com/MultimediaExtensibleGit/Runtime/actions/) [![Testing](https://github.com/MultimediaExtensibleGit/Runtime/workflows/Testing/badge.svg?branch=testing)](https://github.com/MultimediaExtensibleGit/Runtime/actions/)

# Multimedia Extensible Git (MEG) Runtime Library

* [Setup](#setup)

* [Build](#build)

## Setup

* Install [Python 3.7](https://www.python.org/downloads/) or newer.

* Install [pipenv](https://packaging.python.org/tutorials/managing-dependencies/).

* Clone the repository and execute the following command from the working copy in Python:

  `pipenv sync --dev`

## Build

* Build python package

  `pipenv run setup.py sdist bdist_wheel`
