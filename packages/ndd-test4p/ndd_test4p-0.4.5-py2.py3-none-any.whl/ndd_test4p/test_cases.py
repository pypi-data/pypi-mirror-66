"""
Utilities helping writing test cases.
"""

import json
import os
import sys
from abc import ABC
from pathlib import Path
from typing import Dict
from typing import Iterator
from typing import List
from typing import Union

import yaml


class AbstractTest(ABC):
    """
    Base class for tests providing convenient methods to:

    - find test directories and test files
    - read data from test files containing text, JSON or YAML

    :Examples:

    See the documentation blocks of the methods.

    >>> from tests.ndd_test4p.test_cases.test_abstract_test import TestAbstractTest
    >>> my_abstract_test = TestAbstractTest()

    .. automethod:: _test_file_path
    .. automethod:: _test_directory_path
    .. automethod:: _test_data_directory_path
    .. automethod:: _test_data_subdirectory_path
    .. automethod:: _test_data_file_path
    .. automethod:: _test_data_file_paths
    .. automethod:: _test_data_from
    .. automethod:: _test_data_from_json
    .. automethod:: _test_data_from_yaml
    .. automethod:: _test_shared_data_directory_paths
    .. automethod:: _test_shared_data_subdirectory_path
    .. automethod:: _test_shared_data_file_path
    .. automethod:: _test_shared_data_from
    .. automethod:: _test_shared_data_from_json
    .. automethod:: _test_shared_data_from_yaml
    """

    def _test_file_path(self) -> Path:
        """
        Returns:
            pathlib.Path: The file of the class under test.

        :Example:

        >>> file_path = my_abstract_test._test_file_path()
        >>> file_path.as_posix().endswith('/tests/ndd_test4p/test_cases/test_abstract_test.py')
        True
        """
        return Path(sys.modules[self.__module__].__file__)

    def _test_directory_path(self) -> Path:
        """
        Returns:
           pathlib.Path: The directory containing the file of the class under test.

        :Example:

        >>> directory_path = my_abstract_test._test_directory_path()
        >>> directory_path.as_posix().endswith('/tests/ndd_test4p/test_cases')
        True
        """
        return self._test_file_path().parent

    # ------------------------------------------------------------------------------------------------------- data -----

    def _test_data_directory_path(self) -> Path:
        """
        Returns:
           pathlib.Path: The directory beside the file of the class under test and named after the test file
           prefixed with an underscore.

        :Example:

        >>> data_directory_path = my_abstract_test._test_data_directory_path()
        >>> data_directory_path.as_posix().endswith('/tests/ndd_test4p/test_cases/_test_abstract_test')
        True
        """
        return self._test_directory_path().joinpath('_' + self._test_file_path().stem)

    def _test_data_subdirectory_path(self, path_segment: str, *path_segments: str) -> Path:
        """
        Args:
            path_segment (str): The first segment of the child directory path.
            *path_segments (str): The other segments of the child directory path.

        Returns:
           pathlib.Path: The subdirectory (existing or not) under the "data directory"
           (see :func:`_test_data_directory_path`) with the given path (see :func:`pathlib.PurePath.joinpath`).

        :Example:

        >>> data_directory_path = my_abstract_test._test_data_subdirectory_path('subdirectory')
        >>> data_directory_path.as_posix().endswith('/tests/ndd_test4p/test_cases/_test_abstract_test/subdirectory')
        True
        >>> data_directory_path = my_abstract_test._test_data_subdirectory_path('subdirectory', 'subdirectory-L2')
        >>> data_directory_path.as_posix().endswith(
        ...     '/tests/ndd_test4p/test_cases/_test_abstract_test/subdirectory/subdirectory-L2')
        True
        """
        return self._test_data_directory_path().joinpath(path_segment, *path_segments)

    def _test_data_file_path(self, path_segment: str, *path_segments: str) -> Path:
        """
        Args:
            path_segment (str): The first segment of the file path.
            *path_segments (str): The other segments of the file path.

        Returns:
           pathlib.Path: The file (existing or not) under the "data directory"
           (see :func:`_test_data_directory_path`) with the given path (see :func:`pathlib.PurePath.joinpath`).

        :Example:

        >>> data_file_path = my_abstract_test._test_data_file_path('some-file.txt')
        >>> data_file_path.as_posix().endswith('/tests/ndd_test4p/test_cases/_test_abstract_test/some-file.txt')
        True
        >>> data_file_path = my_abstract_test._test_data_file_path('subdirectory', 'some-file-L2.txt')
        >>> data_file_path.as_posix().endswith(
        ...     '/tests/ndd_test4p/test_cases/_test_abstract_test/subdirectory/some-file-L2.txt')
        True
        """
        return self._test_data_directory_path().joinpath(path_segment, *path_segments)

    def _test_data_file_paths(self, pattern: str) -> [Path]:
        """
        Args:
            pattern (str): The glob pattern of the files to find.

        Returns:
            [pathlib.Path]: The files under the "data directory" (see :func:`_test_data_directory_path`)
            with their name matching the given glob pattern.

        :Example:

        >>> data_file_paths = my_abstract_test._test_data_file_paths('*.txt')
        >>> len(data_file_paths)
        2
        >>> data_file_paths[0].as_posix().endswith('/tests/ndd_test4p/test_cases/_test_abstract_test/another-file.txt')
        True
        >>> data_file_paths[1].as_posix().endswith('/tests/ndd_test4p/test_cases/_test_abstract_test/some-file.txt')
        True
        """
        return sorted(self._test_data_directory_path().glob(pattern))

    def _test_data_from(self, path_segment: str, *path_segments: str) -> str:
        """
        Args:
            path_segment (str): The first segment of the file path.
            *path_segments (str): The other segments of the file path.

        Returns:
            str: The content of the given "data file" (see :func:`_test_data_file_path`).

        :Example:

        >>> my_abstract_test._test_data_from('some-file.txt')
        'content of some-file.txt'
        >>> my_abstract_test._test_data_from('subdirectory', 'some-file-L2.txt')
        'content of some-file-L2.txt'
        """
        return self._test_data_file_path(path_segment, *path_segments).read_text()

    def _test_data_from_json(self, path_segment: str, *path_segments: str) -> Union[Dict, List]:
        """
        Args:
            path_segment (str): The first segment of the file path.
            *path_segments (str): The other segments of the file path.

        Returns:
            Union[Dict, List]: The content of the given JSON "data file" (see :func:`_test_data_file_path`).

        :Example:

        >>> my_abstract_test._test_data_from_json('some-file.json')
        {'file': 'some-file.json'}
        >>> my_abstract_test._test_data_from_json('subdirectory','some-file-L2.json')
        {'file': 'some-file-L2.json'}
        """
        return json.loads(self._test_data_from(path_segment, *path_segments))

    def _test_data_from_yaml(self, path_segment: str, *path_segments: str) -> Union[Dict, List]:
        """
        Args:
            path_segment (str): The first segment of the file path.
            *path_segments (str): The other segments of the file path.

        Returns:
            Union[Dict, List]: The content of the given YAML "data file" (see :func:`_test_data_file_path`).

        :Example:

        >>> my_abstract_test._test_data_from_yaml('some-file.yaml')
        {'file': 'some-file.yaml'}
        >>> my_abstract_test._test_data_from_yaml('subdirectory','some-file-L2.yaml')
        {'file': 'some-file-L2.yaml'}
        """
        return yaml.safe_load(self._test_data_from(path_segment, *path_segments))

    # ------------------------------------------------------------------------------------------------ shared data -----

    #: The default name of the shared data directory.
    SHARED_DATA_DIRECTORY_NAME = '_test_shared_data'

    def _test_shared_data_directory_paths(self) -> Iterator[Path]:
        """
        Returns:
           Iterator[pathlib.Path]: An iterator on all "shared data directories",
           i.e. directories named :attr:`AbstractTest.SHARED_DATA_DIRECTORY_NAME` in the filesystem hierarchy.

        :Example:

        >>> data_directory_paths = my_abstract_test._test_shared_data_directory_paths()
        >>> data_directory_path_1 = next(data_directory_paths)
        >>> data_directory_path_1.as_posix().endswith('/tests/ndd_test4p/test_cases/_test_shared_data')
        True
        >>> data_directory_path_2 = next(data_directory_paths)
        >>> data_directory_path_2.as_posix().endswith('/tests/ndd_test4p/_test_shared_data')
        True
        """
        current_directory = self._test_directory_path()

        while current_directory is not None:
            current_shared_directory = current_directory.joinpath(AbstractTest.SHARED_DATA_DIRECTORY_NAME)

            if current_shared_directory.is_dir():
                yield current_shared_directory

            previous_directory = current_directory
            current_directory = current_directory.parent

            if current_directory == previous_directory:
                return

    def _test_shared_data_subdirectory_path(self, path_segment: str, *path_segments: str) -> Path:
        """
        Args:
            directory_name (str): The name of the child directory.

        Returns:
           pathlib.Path: The first existing subdirectory under a "shared data directory"
           (see :func:`_test_shared_data_directory_path`) with the given name.

        Raises:
            :obj:`FileNotFoundError`: raised if no directory can be found.

        :Example:

        >>> data_directory_path = my_abstract_test._test_shared_data_subdirectory_path('subdirectory_L2')
        >>> data_directory_path.as_posix().endswith('/tests/ndd_test4p/test_cases/_test_shared_data/subdirectory_L2')
        True
        >>> data_directory_path = my_abstract_test._test_shared_data_subdirectory_path(
        ...     'subdirectory_L2', 'subdirectory_L2-2')
        >>> data_directory_path.as_posix().endswith(
        ...     '/tests/ndd_test4p/test_cases/_test_shared_data/subdirectory_L2/subdirectory_L2-2')
        True
        """
        for directory in self._test_shared_data_directory_paths():
            subdirectory = directory.joinpath(path_segment, *path_segments)
            if subdirectory.is_dir():
                return subdirectory
        path = os.path.join(path_segment, *path_segments)
        raise FileNotFoundError(f'No subdirectory named "{path}" was found in shared data directories')

    def _test_shared_data_file_path(self, path_segment: str, *path_segments: str) -> Path:
        """
        Args:
            file_name (str): The name of the file.

        Returns:
           pathlib.Path: The first existing file under a "shared data directory"
           (see :func:`_test_shared_data_directory_path`) with the given name.

        Raises:
            :obj:`FileNotFoundError`: raised if no file can be found.

        :Example:

        >>> data_file_path = my_abstract_test._test_shared_data_file_path('shared-file-L2.txt')
        >>> data_file_path.as_posix().endswith('/tests/ndd_test4p/test_cases/_test_shared_data/shared-file-L2.txt')
        True
        >>> data_file_path = my_abstract_test._test_shared_data_file_path('subdirectory_L2', 'shared-file-L2-2.txt')
        >>> data_file_path.as_posix().endswith(
        ...     '/tests/ndd_test4p/test_cases/_test_shared_data/subdirectory_L2/shared-file-L2-2.txt')
        True
        """
        for directory in self._test_shared_data_directory_paths():
            file = directory.joinpath(path_segment, *path_segments)
            if file.is_file():
                return file
        path = os.path.join(path_segment, *path_segments)
        raise FileNotFoundError(f'No file named "{path}" was found in shared data directories')

    def _test_shared_data_from(self, path_segment: str, *path_segments: str) -> str:
        """
        Args:
            path_segment (str): The first segment of the file path.
            *path_segments (str): The other segments of the file path.

        Returns:
            str: The content of the given "shared data file" (see :func:`_test_shared_data_file_path`).

        Raises:
            :obj:`FileNotFoundError`: raised if no file can be found.

        :Example:

        >>> my_abstract_test._test_shared_data_from('shared-file-L2.txt')
        'shared content of shared-file-L2.txt'
        >>> my_abstract_test._test_shared_data_from('subdirectory_L2', 'shared-file-L2-2.txt')
        'shared content of shared-file-L2-2.txt'
        """
        return self._test_shared_data_file_path(path_segment, *path_segments).read_text()

    def _test_shared_data_from_json(self, path_segment: str, *path_segments: str) -> Union[Dict, List]:
        """
        Args:
            path_segment (str): The first segment of the file path.
            *path_segments (str): The other segments of the file path.

        Returns:
            Union[Dict, List]: The content of the given JSON "shared data file"
            (see :func:`_test_shared_data_file_path`).

        Raises:
            :obj:`FileNotFoundError`: raised if no file can be found.

        :Example:

        >>> my_abstract_test._test_shared_data_from_json('shared-file-L2.json')
        {'file': 'shared-file-L2.json'}
        >>> my_abstract_test._test_shared_data_from_json('subdirectory_L2', 'shared-file-L2-2.json')
        {'file': 'shared-file-L2-2.json'}
        """
        return json.loads(self._test_shared_data_from(path_segment, *path_segments))

    def _test_shared_data_from_yaml(self, path_segment: str, *path_segments: str) -> Union[Dict, List]:
        """
        Args:
            path_segment (str): The first segment of the file path.
            *path_segments (str): The other segments of the file path.

        Returns:
            Union[Dict, List]: The content of the given YAML "shared data file"
            (see :func:`_test_shared_data_file_path`).

        Raises:
            :obj:`FileNotFoundError`: raised if no file can be found.

        :Example:

        >>> my_abstract_test._test_shared_data_from_yaml('shared-file-L2.yaml')
        {'file': 'shared-file-L2.yaml'}
        >>> my_abstract_test._test_shared_data_from_yaml('subdirectory_L2', 'shared-file-L2-2.yaml')
        {'file': 'shared-file-L2-2.yaml'}
        """
        return yaml.safe_load(self._test_shared_data_from(path_segment, *path_segments))
