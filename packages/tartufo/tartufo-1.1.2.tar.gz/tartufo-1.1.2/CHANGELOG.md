v1.1.2 - 21 April 2020
----------------------

* #48 (Backport of #45 & #46)
  * Documented Docker usage
  * Small fixes to Docker to allow SSH clones and avoid scanning tartufo itself
* Docs have been backported from the `master` branch.

v1.1.1 - 13 December 2019
-------------------------

* Fix the docs and pre-commit hook to use hyphens in CLI arguments, as opposed
  to underscores.

v1.1.0 - 27 November 2019
-------------------------

* Support reading config from `tartufo.toml` for non-Python projects
* #17 - A separate repository can be used for storing rules files
* #18 - Read the `pyproject.toml` or `tartufo.toml` from the repo being scanned

v1.0.2 - 19 November 2019
-------------------------

This release is essentially the same as the v1.0.0 release, but with a new number.
Unfortunately, we had historical releases versioned as v1.0.0 and v1.0.1. Due to
limitations in PyPI (https://pypi.org/help/#file-name-reuse), even if a previous
release has been deleted, the version number may not be reused.

v1.0.0 - 19 November 2019
-------------------------

Version 1.0.0! Initial stable release!

* Finished the "hard fork" process, so that our project is now independent of `truffleHog`.
* #13 - Tests are now split into multiple files/classes
* #14 - `tartufo` is now configurable via `pyproject.toml`
* #15 - Code is fully type annotated
* #16 - Fully fleshed out "Community Health" files
* #20 - Code is now fully formatted by `black`

v0.0.2 - 23 October 2019
------------------------

Automated Docker builds!

* Docker images are built and pushed automatically to https://hub.docker.com/r/godaddy/tartufo
* The version of these images has been synchronized with the Python version via the VERSION file
* Gave the Python package a more verbose long description for PyPi, straight from the README.

v0.0.1 - 23 October 2019
------------------------

This is the first public release of `tartufo`, which has been forked off from `truffleHog`.

The primary new features/bugfixes include:

* Renamed everything to `tartufo`
* #1 - Additive whitelist/blacklist support
* #4 - `--pre_commit` support
* #6 - Documented the `--cleanup` switch which cleans up files in `/tmp`
* #10 - Running `tartufo` with no arguments would produce an error
* Added support for https://pre-commit.com/ style hooks
