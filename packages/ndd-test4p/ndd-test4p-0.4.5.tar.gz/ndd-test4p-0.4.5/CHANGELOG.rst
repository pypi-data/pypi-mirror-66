#########
Changelog
#########


Version 0.4.5
=============

**Issues:**

Fix vulnerabilities by replacing yaml#load with yaml#save_load

**Improvements:**

- Update dependencies
- Add tests for Python 3.8


Version 0.4.4
=============

**Features:**

- Add variable arguments to ``ndd_test4p.test_cases.AbstractTest#_test_shared_data_*`` methods
- Add variable arguments to ``ndd_test4p.test_cases.AbstractTest#_test_data_*`` methods

**Improvements:**

- Update dependencies


Version 0.4.3
=============

**Issues:**

- Update return hints of methods:

  - ``ndd_test4p.AbstractTest#_test_data_from_json``
  - ``ndd_test4p.AbstractTest#_test_data_from_yaml``
  - ``ndd_test4p.AbstractTest#_test_shared_data_from_json``
  - ``ndd_test4p.AbstractTest#_test_shared_data_from_yaml``

**Improvements:**

- Update build documentation


Version 0.4.2
=============

**Issues:**

- Revert ``ndd_test4p.differences_viewers.MeldViewerDelegate`` to use a blocking process by default.
  Add a delay to the settings for the non-blocking process case.


Version 0.4.1
=============

**Features:**

- Add an environment variable to set ``ndd_test4p.differences_viewers.DifferencesViewerDelegate`` settings
- Add options to ``ndd_test4p.differences_viewers.MeldViewerDelegate`` (blocking or non-blocking mode, create a new instance or reuse an old one)

**Improvements:**

- Update and refactor documentation


Version 0.4.0
=============

**Breaking changes:**

- Rename ``ndd_test.differences_viewers.TextFileDifferencesViewer`` to ``ndd_test.differences_viewers.TextDifferencesViewer``

**Features:**

- Add to ``TextDifferencesViewer`` the capability of comparing:

  - actual file content with expected data
  - actual file content with expected file content
  - actual data with expected file content

- Add to ``YamlDifferencesViewer`` the capability of comparing:

  - actual file content with expected data
  - actual file content with expected file content

**Quality:**

- Improve code quality using pylint and flake8
- Refactor ``TextDifferencesViewer`` and ``YamlDifferencesViewer``
- Replace all ``pathlib.PosixPath`` with ``pathlib.Path``


Version 0.3.0
=============

**Features:**

- Add ``ndd_test4p.test_cases.AbstractTest#_test_shared_data_`` methods

**Issues:**

- Fix missing ``wheel`` dependency


Version 0.2.2
=============

**Improvements:**

- Fix error message in ``ndd_test4p.expects.content_matchers.have_same_content_recursively_as``
- Replace all ``pathlib.PosixPath`` with ``pathlib.Path``

**Quality:**

- Add comments to Flake8 configuration file
- Update README to use ``pyenv``

Version 0.2.1
=============

**Features:**

- Add ``ndd_test4p.test_cases.AbstractTest#_test_data_subdirectory_path``

Version 0.2.0
=============

**Breaking changes:** None

**Features:**

- Add ``ndd_test4p.differences_viewers.YamlDifferencesViewer``
- Add ``ndd_test4p.expects.content_matchers.have_same_content_recursively_as``
- Add ``ndd_test4p.comparators.DirectoryContentComparator``
- Add ``ndd_test4p.comparators.TextFileContentComparator#unified_diff``
- Add diff output in ``ndd_test4p.expects.content_matchers.have_same_content_as``

**Improvements:**

- Change implementation of ``ndd_test4p.differences_viewers.DiffViewerDelegate`` to difflib
- Rename GitLab CI stages

**Issues:** None

**Quality:**

- Improve code quality using pylint and flake8
- Fix distribution documentation

Version 0.1.1
=============

- Add 'deploy to PyPI' stage to GitLab CI
- Fix project URLs in ``setup.cfg``
- Fix regular expression in ``.gitlab-ci``


Version 0.1.0
=============

- Add ``ndd_test4p.AbstractTest``
- Add Flake8 linter
- Add Pylint linter
- Add Sphinx documentation
- Add Tox testing
- Add ``doctest`` tests
- Add ``ndd_test4p.expects.numeric_matchers.approximate``
- Add ``ndd_test4p.expects.content_matchers.have_same_content_as``
- Add ``ndd_test4p.comparators.TextFileContentComparator``
- Add ``ndd_test4p.differences_viewers``
- Add ``ndd_test.differences_viewers.TextFileDifferencesViewer``
- Add testing and code coverage to GitLab CI

