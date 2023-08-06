from pathlib import Path
from types import GeneratorType

import pytest
from expects import *

from ndd_test4p.test_cases import AbstractTest


class AbstractTestAbstractTest(AbstractTest):

    @pytest.fixture()
    def tests_directory_path(self) -> Path:
        return Path(__file__).parent.parent.parent

    @pytest.fixture()
    def test_case_directory_path(self, tests_directory_path: Path) -> Path:
        test_case_directory_path = tests_directory_path.joinpath('ndd_test4p', 'test_cases')
        expect(test_case_directory_path.as_posix()).to(end_with('/tests/ndd_test4p/test_cases'))
        return test_case_directory_path


class TestAbstractTest(AbstractTestAbstractTest):

    def test_test_file_path(self, test_case_directory_path: Path):
        expected_path = test_case_directory_path.joinpath('test_abstract_test.py')
        expect(self._test_file_path()).to(equal(expected_path))
        expect(self._test_file_path().is_file()).to(be_true)

    def test_test_directory_path(self, test_case_directory_path: Path):
        expected_path = test_case_directory_path
        expect(self._test_directory_path()).to(equal(expected_path))
        expect(self._test_directory_path().is_dir()).to(be_true)


class TestAbstractTest_Data(AbstractTestAbstractTest):  # pylint: disable=invalid-name

    @pytest.fixture()
    def test_abstract_test_path(self, test_case_directory_path: Path):
        return test_case_directory_path.joinpath('_test_abstract_test')

    def test_test_data_directory_path(self, test_case_directory_path: Path):
        expected_path = test_case_directory_path.joinpath('_test_abstract_test')
        expect(self._test_data_directory_path()).to(equal(expected_path))
        expect(self._test_data_directory_path().is_dir()).to(be_true)

    def test_test_data_subdirectory_path(self, test_abstract_test_path: Path):
        # one level deep
        expected_path = test_abstract_test_path.joinpath('subdirectory')
        expect(self._test_data_subdirectory_path('subdirectory')).to(equal(expected_path))
        expect(self._test_data_subdirectory_path('subdirectory').is_dir()).to(be_true)

        # two levels deep
        expected_path = test_abstract_test_path.joinpath('subdirectory', 'subdirectory-L2')
        expect(self._test_data_subdirectory_path('subdirectory', 'subdirectory-L2')).to(equal(expected_path))
        expect(self._test_data_subdirectory_path('subdirectory', 'subdirectory-L2').is_dir()).to(be_true)

        # non existing
        expected_path = test_abstract_test_path.joinpath('non-existing-subdirectory')
        expect(self._test_data_subdirectory_path('non-existing-subdirectory')).to(equal(expected_path))
        expect(self._test_data_subdirectory_path('non-existing-subdirectory').exists()).to(be_false)

    def test_test_data_file_path(self, test_abstract_test_path: Path):
        # one level deep
        expected_path = test_abstract_test_path.joinpath('some-file.txt')
        expect(self._test_data_file_path('some-file.txt')).to(equal(expected_path))
        expect(self._test_data_file_path('some-file.txt').is_file()).to(be_true)

        # two levels deep
        expected_path = test_abstract_test_path.joinpath('subdirectory', 'some-file-L2.txt')
        expect(self._test_data_file_path('subdirectory', 'some-file-L2.txt')).to(equal(expected_path))
        expect(self._test_data_file_path('subdirectory', 'some-file-L2.txt').is_file()).to(be_true)

        # non existing
        expected_path = test_abstract_test_path.joinpath('non-existing-file.txt')
        expect(self._test_data_file_path('non-existing-file.txt')).to(equal(expected_path))
        expect(self._test_data_file_path('non-existing-file.txt').exists()).to(be_false)

    def test_test_data_file_paths(self, test_abstract_test_path: Path):
        # one level deep
        expected_paths = [
            test_abstract_test_path.joinpath('another-file.txt'),
            test_abstract_test_path.joinpath('some-file.txt'),
        ]
        expect(self._test_data_file_paths('*.txt')).to(equal(expected_paths))
        for expected_path in expected_paths:
            expect(expected_path.is_file()).to(be_true)

        # two levels deep
        expected_paths = [
            test_abstract_test_path.joinpath('another-file.txt'),
            test_abstract_test_path.joinpath('some-file.txt'),
            test_abstract_test_path.joinpath('subdirectory', 'some-file-L2.txt'),
        ]
        expect(self._test_data_file_paths('**/*.txt')).to(equal(expected_paths))
        for expected_path in expected_paths:
            expect(expected_path.is_file()).to(be_true)

        # non existing
        expect(self._test_data_file_paths('*.invalid')).to(be_empty)

    def test_test_data_from(self):
        # one level deep
        expected_content = 'content of some-file.txt'
        expect(self._test_data_from('some-file.txt')).to(equal(expected_content))

        # two levels deep
        expected_content = 'content of some-file-L2.txt'
        expect(self._test_data_from('subdirectory', 'some-file-L2.txt')).to(equal(expected_content))

        # non existing
        with pytest.raises(FileNotFoundError):
            self._test_data_from('non-existing-file.txt')

    def test_test_data_from_json(self):
        # one level deep
        expected_content = {'file': 'some-file.json'}
        expect(self._test_data_from_json('some-file.json')).to(equal(expected_content))

        # two levels deep
        expected_content = {'file': 'some-file-L2.json'}
        expect(self._test_data_from_json('subdirectory', 'some-file-L2.json')).to(equal(expected_content))

        # non existing
        with pytest.raises(FileNotFoundError):
            self._test_data_from_json('non-existing-file.json')

    def test_test_data_from_yaml(self):
        # one level deep
        expected_content = {'file': 'some-file.yaml'}
        expect(self._test_data_from_yaml('some-file.yaml')).to(equal(expected_content))

        # two levels deep
        expected_content = {'file': 'some-file-L2.yaml'}
        expect(self._test_data_from_yaml('subdirectory', 'some-file-L2.yaml')).to(equal(expected_content))

        # non existing
        with pytest.raises(FileNotFoundError):
            self._test_data_from_yaml('non-existing-file.yaml')


class TestAbstractTest_SharedData(AbstractTestAbstractTest):  # pylint: disable=invalid-name

    @pytest.fixture()
    def test_shared_data_l1_path(self, tests_directory_path: Path):
        return tests_directory_path.joinpath('ndd_test4p', '_test_shared_data')

    @pytest.fixture()
    def test_shared_data_l2_path(self, tests_directory_path: Path):
        return tests_directory_path.joinpath('ndd_test4p', 'test_cases', '_test_shared_data')

    def test_test_shared_data_directory_paths(self, test_case_directory_path: Path):
        expected_path = [
            test_case_directory_path.joinpath('_test_shared_data'),
            test_case_directory_path.parent.joinpath('_test_shared_data'),
        ]
        expect(self._test_shared_data_directory_paths()).to(be_a(GeneratorType))
        expect(list(self._test_shared_data_directory_paths())).to(equal(expected_path))

    def test_test_shared_data_subdirectory_path(self, test_shared_data_l1_path: Path, test_shared_data_l2_path: Path):
        # one level deep
        expected_path = test_shared_data_l2_path.joinpath('subdirectory_L2')
        actual_path = self._test_shared_data_subdirectory_path('subdirectory_L2')
        expect(actual_path).to(equal(expected_path))
        expect(actual_path.is_dir()).to(be_true)

        expected_path = test_shared_data_l1_path.joinpath('subdirectory_L1')
        actual_path = self._test_shared_data_subdirectory_path('subdirectory_L1')
        expect(actual_path).to(equal(expected_path))
        expect(actual_path.is_dir()).to(be_true)

        # two levels deep
        expected_path = test_shared_data_l2_path.joinpath('subdirectory_L2', 'subdirectory_L2-2')
        actual_path = self._test_shared_data_subdirectory_path('subdirectory_L2', 'subdirectory_L2-2')
        expect(actual_path).to(equal(expected_path))
        expect(actual_path.is_dir()).to(be_true)

        expected_path = test_shared_data_l1_path.joinpath('subdirectory_L1', 'subdirectory_L1-2')
        actual_path = self._test_shared_data_subdirectory_path('subdirectory_L1', 'subdirectory_L1-2')
        expect(actual_path).to(equal(expected_path))
        expect(actual_path.is_dir()).to(be_true)

        # non existing
        with pytest.raises(FileNotFoundError,
                           match='No subdirectory named "non-existing-directory" was found in shared data directories'):
            self._test_shared_data_subdirectory_path('non-existing-directory')

    def test_test_shared_data_file_path(self, test_shared_data_l1_path: Path, test_shared_data_l2_path: Path):
        # one level deep
        expected_path = test_shared_data_l2_path.joinpath('shared-file-L2.txt')
        actual_path = self._test_shared_data_file_path('shared-file-L2.txt')
        expect(actual_path).to(equal(expected_path))
        expect(actual_path.is_file()).to(be_true)

        expected_path = test_shared_data_l1_path.joinpath('shared-file-L1.txt')
        actual_path = self._test_shared_data_file_path('shared-file-L1.txt')
        expect(actual_path).to(equal(expected_path))
        expect(actual_path.is_file()).to(be_true)

        # two levels deep
        expected_path = test_shared_data_l2_path.joinpath('subdirectory_L2', 'shared-file-L2-2.txt')
        actual_path = self._test_shared_data_file_path('subdirectory_L2', 'shared-file-L2-2.txt')
        expect(actual_path).to(equal(expected_path))
        expect(actual_path.is_file()).to(be_true)

        expected_path = test_shared_data_l1_path.joinpath('subdirectory_L1', 'shared-file-L1-2.txt')
        actual_path = self._test_shared_data_file_path('subdirectory_L1', 'shared-file-L1-2.txt')
        expect(actual_path).to(equal(expected_path))
        expect(actual_path.is_file()).to(be_true)

        # non existing
        with pytest.raises(FileNotFoundError,
                           match='No file named "non-existing-file.txt" was found in shared data directories'):
            self._test_shared_data_file_path('non-existing-file.txt')

    def test_test_shared_data_from(self):
        # one level deep
        expected_content = 'shared content of shared-file-L2.txt'
        expect(self._test_shared_data_from('shared-file-L2.txt')).to(equal(expected_content))

        expected_content = 'shared content of shared-file-L1.txt'
        expect(self._test_shared_data_from('shared-file-L1.txt')).to(equal(expected_content))

        # two levels deep
        expected_content = 'shared content of shared-file-L2-2.txt'
        expect(self._test_shared_data_from('subdirectory_L2', 'shared-file-L2-2.txt')).to(equal(expected_content))

        expected_content = 'shared content of shared-file-L1-2.txt'
        expect(self._test_shared_data_from('subdirectory_L1', 'shared-file-L1-2.txt')).to(equal(expected_content))

        # non existing
        with pytest.raises(FileNotFoundError,
                           match='No file named "non-existing-file.txt" was found in shared data directories'):
            self._test_shared_data_from('non-existing-file.txt')

    def test_test_shared_data_from_json(self):
        # one level deep
        expected_content = {'file': 'shared-file-L2.json'}
        expect(self._test_shared_data_from_json('shared-file-L2.json')).to(equal(expected_content))

        expected_content = {'file': 'shared-file-L1.json'}
        expect(self._test_shared_data_from_json('shared-file-L1.json')).to(equal(expected_content))

        # two levels deep
        expected_content = {'file': 'shared-file-L2-2.json'}
        expect(self._test_shared_data_from_json('subdirectory_L2', 'shared-file-L2-2.json')).to(equal(expected_content))

        expected_content = {'file': 'shared-file-L1-2.json'}
        expect(self._test_shared_data_from_json('subdirectory_L1', 'shared-file-L1-2.json')).to(equal(expected_content))

        # non existing
        with pytest.raises(FileNotFoundError,
                           match='No file named "non-existing-file.json" was found in shared data directories'):
            self._test_shared_data_from_json('non-existing-file.json')

    def test_test_shared_data_from_yaml(self):
        # one level deep
        expected_content = {'file': 'shared-file-L2.yaml'}
        expect(self._test_shared_data_from_yaml('shared-file-L2.yaml')).to(equal(expected_content))

        expected_content = {'file': 'shared-file-L1.yaml'}
        expect(self._test_shared_data_from_yaml('shared-file-L1.yaml')).to(equal(expected_content))

        # two levels deep
        expected_content = {'file': 'shared-file-L2-2.yaml'}
        expect(self._test_shared_data_from_yaml('subdirectory_L2', 'shared-file-L2-2.yaml')).to(equal(expected_content))

        expected_content = {'file': 'shared-file-L1-2.yaml'}
        expect(self._test_shared_data_from_yaml('subdirectory_L1', 'shared-file-L1-2.yaml')).to(equal(expected_content))

        # non existing
        with pytest.raises(FileNotFoundError,
                           match='No file named "non-existing-file.yaml" was found in shared data directories'):
            self._test_shared_data_from_yaml('non-existing-file.yaml')
