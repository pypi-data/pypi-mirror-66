# asterism

Helpers and common patterns used in Project Electron infrastructure. This package is named after a pattern or group of stars that is visually obvious, but not officially recognized as a constellation. Read more about asterisms on [Wikipedia](https://en.wikipedia.org/wiki/Asterism_(astronomy)).

[![Build Status](https://travis-ci.org/RockefellerArchiveCenter/asterism.svg?branch=master)](https://travis-ci.org/RockefellerArchiveCenter/asterism)

## Setup

Make sure this library is installed:

    $ pip install git+git://github.com/RockefellerArchiveCenter/asterism.git


## Usage

You can then use `asterism` in your python scripts by importing it:

    import asterism

### What's here

`bagit_helpers` - contains generic bagit functions to validate and update bags.
`file_helpers` - generic functions for manipulating files and directories, as well as working with ZIP and TAR files.
`models` - a `BasePackage` abstract base model that represents a bag of archival records.
`resources` - Odin representations of ArchivesSpace resources.
`views` - a `BaseServiceView` and a `RoutineView` which provide abstract wrapping methods for handling JSON requests and responses.


## License

This code is released under an [MIT License](LICENSE).
