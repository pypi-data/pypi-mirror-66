Changelog
=========

The purpose of this document is to list all of the notable changes to this
project. The format was inspired by `Keep a Changelog`_. This project adheres
to `semantic versioning`_.

.. contents::
   :local:

.. _Keep a Changelog: http://keepachangelog.com/
.. _semantic versioning: http://semver.org/

`Release 7.0`_ (2020-04-16)
---------------------------

This is a maintenance release that (primarily) updates Python compatibility.

**Backwards incompatible changes:**

- Python 3.7 and 3.8 are now officially supported.

- Python 2.6 and 3.4 are no longer supported.

- Added ``python_requires`` to ``setup.py`` to aid :pypi:`pip` in version
  selection given these compatibility changes.

**Significant changes:**

- Updated the releases bundled in the :mod:`apt_mirror_updater.releases` module
  to include the following:

  - Ubuntu 19.04 (Disco Dingo)
  - Ubuntu 19.10 (Eoan Ermine)
  - Ubuntu 20.04 (Focal Fossa).

- Bug fix for "accidental tuple" in :func:`apt_mirror_updater.releases.parse_csv_file()`.

**Miscellaenous changes:**

- Spent some time stabilizing the test suite on Travis CI (tests were passing
  for me locally but not on Travis CI because the mirror selection differed).
  As a result the test suite got a bit slower, but it's not too bad.

- Move caching decorator to :pypi:`humanfriendly`.

- Fixed deprecation warnings emitted by recent :pypi:`humanfriendly` releases
  and bumped requirements I authored that went through similar changes.

- Made :mod:`multiprocessing` usage compatible with coverage collection. Note
  that I don't expect this to increase coverage, I just wanted to get rid of
  the warnings 😇 (because warnings about harmless things are just as
  distracting as more pertinent warnings).

- Default to Python 3 for local development (required by :pypi:`Sphinx` among
  other things).

- Fixed existing :pypi:`Sphinx` reference warnings in the documentation and
  changed the :man:`sphinx-build` invocation to promote warnings to errors (to
  aid me in the discipline of not introducing broken references from now on).

.. _Release 7.0: https://github.com/xolox/python-apt-mirror-updater/compare/6.1...7.0

`Release 6.1`_ (2018-10-19)
---------------------------

- Bug fix for Ubuntu keyring selection that prevented
  ``ubuntu-archive-removed-keys.gpg`` from being used.
- Bug fix for :func:`~apt_mirror_updater.releases.coerce_release()`
  when given a release number.
- Moved pathnames of Debian and Ubuntu keyring files to constants.
- Added logging to enable debugging of keyring selection process.
- Added proper tests for keyring selection and release coercion.

.. _Release 6.1: https://github.com/xolox/python-apt-mirror-updater/compare/6.0...6.1

`Release 6.0`_ (2018-10-14)
---------------------------

Enable the creation of Ubuntu <= 12.04 chroots on Ubuntu >= 17.04 hosts by
working around (what I am convinced is) a bug in :man:`debootstrap` which picks
the wrong keyring when setting up chroots of old releases. For more information
refer to issue `#8`_.

I've bumped the major version number for this release because the highly
specific ``apt_mirror_updater.eol`` module changed into the much more generic
:mod:`apt_mirror_updater.releases` module. Also the ``release_label`` property was
removed.

.. _Release 6.0: https://github.com/xolox/python-apt-mirror-updater/compare/5.2...6.0
.. _#8: https://github.com/xolox/python-apt-mirror-updater/issues/8

`Release 5.2`_ (2018-10-08)
---------------------------

Use `mirrors.ubuntu.com/mirrors.txt`_ without placing our full trust in it like
older versions of :pypi:`apt-mirror-updater` did 😇.

Feedback in issue `#6`_ suggested that `mirrors.ubuntu.com/mirrors.txt`_ is
working properly (again) and should be preferred over scraping Launchpad.
However I prefer for :pypi:`apt-mirror-updater` to be a reliable "do what I
mean" program and `mirrors.ubuntu.com/mirrors.txt`_ has proven to be unreliable
in the past (see the discussion in `#6`_). As a compromise I've changed the
Ubuntu mirror discovery as follows:

1. Discover Ubuntu mirrors on Launchpad.

2. Try to discover mirrors using `mirrors.ubuntu.com/mirrors.txt`_ and iff
   successful, narrow down the list produced in step 1 based on the URLs
   reported in step 2.

3. Rank the discovered / narrowed down mirrors and pick the best one.

The reason why I've decided to add this additional complexity is because it has
bothered me in the past that Ubuntu mirror discovery was slow and this does
help a lot. Also, why not use a service provided by Ubuntu to speed things up?

Unrelated to the use of `mirrors.ubuntu.com/mirrors.txt`_ I've also bumped the
:pypi:`executor` requirement (twice) in order to pull in upstream improvements
discussed in `executor issue #10`_ and `executor issue #15`_.

.. _Release 5.2: https://github.com/xolox/python-apt-mirror-updater/compare/5.1...5.2
.. _mirrors.ubuntu.com/mirrors.txt: http://mirrors.ubuntu.com/mirrors.txt
.. _#6: https://github.com/xolox/python-apt-mirror-updater/issues/6
.. _executor issue #10: https://github.com/xolox/python-executor/issues/10
.. _executor issue #15: https://github.com/xolox/python-executor/issues/15

`Release 5.1`_ (2018-06-22)
---------------------------

Work on release 5.1 started with the intention of publishing a 5.0.2 bug fix
release for the EOL detection of Debian LTS releases reported in `#5`_, however
unrelated changes were required to stabilize the test suite. This explains how
5.0.2 became 5.1 😇.

When I started working on resolving the issue reported in `#5`_ it had been
quite a while since the previous release (233 days) and so some technical debt
had accumulated in the project, causing the test suite to break. Most
significantly, Travis CI switched their workers from Ubuntu 12.04 to 14.04.

Here's a detailed overview of changes:

- Bug fix for EOL detection of Debian LTS releases (reported in `#5`_).
- Bug fix for trivial string matching issue in test suite (caused by a naively
  written test).
- Bug fix for recursive ``repr()`` calls potentially causing infinite
  recursion, depending on logging level (see e.g. build 395421319_).
- Updated bundled EOL dates based on distro-info-data available in Ubuntu 18.04.
- Added this changelog to the documentation, including a link in the readme.
- Make sure the ``test_gather_eol_dates`` test method runs on Travis CI (by
  installing the distro-info-data_ package). This exposed a Python 3
  incompatibility (in build 395410569_) that has since been resolved.
- Include documentation in source distributions (``MANIFEST.in``).
- Silence flake8 complaining about bogus D402 issues.
- Add license='MIT' key to ``setup.py`` script.
- Bumped copyright to 2018.

.. _Release 5.1: https://github.com/xolox/python-apt-mirror-updater/compare/5.0.1...5.1
.. _#5: https://github.com/xolox/python-apt-mirror-updater/issues/5
.. _395421319: https://travis-ci.org/xolox/python-apt-mirror-updater/jobs/395421319
.. _distro-info-data: https://packages.ubuntu.com/distro-info-data
.. _395410569: https://travis-ci.org/xolox/python-apt-mirror-updater/jobs/395410569

`Release 5.0.1`_ (2017-11-01)
-----------------------------

Bug fix release for invalid enumeration value (oops).

.. _Release 5.0.1: https://github.com/xolox/python-apt-mirror-updater/compare/5.0...5.0.1

`Release 5.0`_ (2017-11-01)
---------------------------

.. |smart_update| replace:: :func:`~apt_mirror_updater.AptMirrorUpdater.smart_update()`
.. |validate_mirror| replace:: :func:`~apt_mirror_updater.AptMirrorUpdater.validate_mirror()`

Reliable end of life (EOL) detection.

Recently I ran into the issue that the logic to check whether a release is EOL
(that works by checking if the security mirror serves a ``Release.gpg`` file
for the release) failed on me. More specifically the following URL existed at
the time of writing (2017-11-01) even though Ubuntu 12.04 went EOL back in
April:

http://security.ubuntu.com/ubuntu/dists/precise/Release.gpg

At the same time issue `#1`_ and pull request `#2`_ were also indications that
the EOL detection was fragile and error prone. This potential fragility had
bugged me ever since publishing :pypi:`apt-mirror-updater` and this week I
finally finished a more robust and deterministic EOL detection scheme.

This release includes pull requests `#2`_ and `#4`_,  fixing issues `#1`_ and
`#3`_. Here's a detailed overview of changes:

- Addition: Allow optional arguments to ``apt-get update`` (`#3`_, `#4`_).

  - I simplified and improved the feature requested in issue `#3`_ and
    implemented in pull request `#4`_ by switching from an optional list
    argument to 'star-args' and applying the same calling convention to
    |smart_update| as well.

  - This is backwards incompatible with the implementation in pull request
    `#4`_ (which I merged into the ``dev`` branch but never published to PyPI)
    and it's also technically backwards incompatible in the sense that keyword
    arguments could previously be given to |smart_update| as positional
    arguments. This explains why I'm bumping the major version number.

- Bug fix for incorrect marking of EOL when HTTP connections fail (`#2`_).
- Refactoring: Apply timeout handling to HTTP response bodies.
- Refactoring: Distinguish 404 from other HTTP errors:

  - This change enhances |validate_mirror| by making a distinction between
    a confirmed HTTP 404 response versus other error conditions which may be of
    a more transient nature.
  - The goal of this change is to preserve the semantics requested in issue
    `#1`_ and implemented in pull request `#2`_ without needing the additional
    HTTP request performed by ``can_connect_to_mirror()``.
  - Because |validate_mirror| previously returned a boolean but now returns
    an enumeration member this change is technically backwards incompatible,
    then again |validate_mirror| isn't specifically intended for callers
    because it concerns internal logic of apt-mirror-updater. I'm nevertheless
    bumping the major version number.

- Refactoring: Improve HTTP request exception handling:

  - 404 responses and timeouts are no longer subject to retrying.
  - The exception :exc:`apt_mirror_updater.http.NotFoundError` is now raised on
    HTTP 404 responses. Other unexpected HTTP response codes raise
    :exc:`apt_mirror_updater.http.InvalidResponseError`.
  - The specific distinction between 404 and !200 was made because the 404
    response has become significant in checking for EOL status.

.. _Release 5.0: https://github.com/xolox/python-apt-mirror-updater/compare/4.0...5.0
.. _#1: https://github.com/xolox/python-apt-mirror-updater/issues/1
.. _#2: https://github.com/xolox/python-apt-mirror-updater/pull/2
.. _#3: https://github.com/xolox/python-apt-mirror-updater/issues/3
.. _#4: https://github.com/xolox/python-apt-mirror-updater/pull/4

`Release 4.0`_ (2017-06-14)
---------------------------

Robust validation of available mirrors (backwards incompatible).

.. _Release 4.0: https://github.com/xolox/python-apt-mirror-updater/compare/3.1...4.0

`Release 3.1`_ (2017-06-13)
---------------------------

Made mirror comparison more robust.

.. _Release 3.1: https://github.com/xolox/python-apt-mirror-updater/compare/3.0...3.1

`Release 3.0`_ (2017-06-13)
---------------------------

Added Debian archive support (with old releases):

- Addition: Added Debian archive support (old releases).
- Improvement: Don't bother validating archive / old-releases mirror.
- Refactoring: Moved URLs to backend specific modules.

.. _Release 3.0: https://github.com/xolox/python-apt-mirror-updater/compare/2.1...3.0

`Release 2.1`_ (2017-06-12)
---------------------------

Restored Python 3 compatibility, improved robustness:

- Improvement: Make the ``is_available`` and ``is_updating`` properties of the
  ``CandidateMirror`` class more robust.
- Bug fix: I suck at Unicode in Python (most people do :-p).
- Cleanup: Remove unused import from test suite.

.. _Release 2.1: https://github.com/xolox/python-apt-mirror-updater/compare/2.0...2.1

`Release 2.0`_ (2017-06-11)
---------------------------

Generation of ``sources.list`` files and chroot creation.

Detailed overview of changes:

- Addition: Added a simple :man:`debootstrap` wrapper.
- Addition: Programmatic ``/etc/apt/sources.list`` generation
- Bug fix for ``check_suite_available()``.
- Bug fix: Never apply Ubuntu's old release handling to Debian.
- Bug fix: Never remove ``/var/lib/apt/lists/lock`` file.
- Improvement: Enable stable mirror selection
- Improvement: Make it possible to override distributor ID and codename
- Improvement: Render interactive spinner during mirror ranking.
- Refactoring: Generalize AptMirrorUpdater initializer (backwards incompatible!)
- Refactoring: Generalize backend module loading
- Refactoring: Modularize ``/etc/apt/sources.list`` writing.

.. _Release 2.0: https://github.com/xolox/python-apt-mirror-updater/compare/1.0...2.0

`Release 1.0`_ (2017-06-08)
---------------------------

Improved Ubuntu mirror discovery, added an automated test suite, and more.

The bump to version 1.0 isn't so much intended to communicate that this
is now mature software, it's just that I made several backwards
incompatible changes in order to improve the modularity of the code
base, make it easier to develop automated tests, maintain platform
support, etc :-).

A more detailed overview of (significant) changes:

- Improved Ubuntu mirror discovery (by scraping Launchpad instead).
- Extracted mirror discovery to separate (backend specific) modules.
- Extracted HTTP handling to a separate module.
- Enable Control-C to interrupt concurrent connection tests.
- Expose limit in Python API and command line interface and make limit optional by passing 0.
- Bug fix for Python 3 incompatibility: Stop using :data:`sys.maxint` :-).

.. _Release 1.0: https://github.com/xolox/python-apt-mirror-updater/compare/0.3.1...1.0

`Release 0.3.1`_ (2016-06-29)
-----------------------------

Avoid 'nested' smart updates (the old code worked fine but gave confusing
output and performed more work than necessary, which bothered me :-).

.. _Release 0.3.1: https://github.com/xolox/python-apt-mirror-updater/compare/0.3...0.3.1

`Release 0.3`_ (2016-06-29)
---------------------------

Make smart update understand EOL suites.

.. _Release 0.3: https://github.com/xolox/python-apt-mirror-updater/compare/0.2...0.3

`Release 0.2`_ (2016-06-29)
---------------------------

Bug fix: Replace ``security.ubuntu.com`` as well.

.. _Release 0.2: https://github.com/xolox/python-apt-mirror-updater/compare/0.1.2...0.2

`Release 0.1.2`_ (2016-06-29)
-----------------------------

Bug fix: Explicitly terminate multiprocessing pool.

.. _Release 0.1.2: https://github.com/xolox/python-apt-mirror-updater/compare/0.1.1...0.1.2

`Release 0.1.1`_ (2016-03-10)
-----------------------------

Initial release (added ``MANIFEST.in``).

.. _Release 0.1.1: https://github.com/xolox/python-apt-mirror-updater/compare/0.1...0.1.1

`Release 0.1`_ (2016-03-10)
---------------------------

Initial commit.

.. _Release 0.1: https://github.com/xolox/python-apt-mirror-updater/tree/0.1
