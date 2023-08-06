from pathlib import Path
from unittest import mock

import pytest

from ndd_test4p.differences_viewers import MeldViewerDelegate
from ndd_test4p.test_cases import AbstractTest


class TestMeldViewerDelegate(AbstractTest):

    @mock.patch('subprocess.Popen')
    @pytest.mark.slow
    def test_with_non_blocking_process(self, popen_mock):
        actual_file_path = Path('actual')
        expected_file_path = Path('expected')

        delegate = MeldViewerDelegate()
        delegate.non_blocking_process_delay = 0.01
        delegate.view(actual_file_path, expected_file_path)
        popen_mock.assert_called_with(['meld', '--newtab', expected_file_path, actual_file_path])

        delegate = MeldViewerDelegate(new_instance=False)
        delegate.non_blocking_process_delay = 0.01
        delegate.view(actual_file_path, expected_file_path)
        popen_mock.assert_called_with(['meld', '--newtab', expected_file_path, actual_file_path])

        delegate = MeldViewerDelegate(new_instance=True)
        delegate.non_blocking_process_delay = 0.01
        delegate.view(actual_file_path, expected_file_path)
        popen_mock.assert_called_with(['meld', expected_file_path, actual_file_path])

        delegate = MeldViewerDelegate(blocking_process=False)
        delegate.non_blocking_process_delay = 0.01
        delegate.view(actual_file_path, expected_file_path)
        popen_mock.assert_called_with(['meld', '--newtab', expected_file_path, actual_file_path])

        delegate = MeldViewerDelegate(blocking_process=False, new_instance=False)
        delegate.non_blocking_process_delay = 0.01
        delegate.view(actual_file_path, expected_file_path)
        popen_mock.assert_called_with(['meld', '--newtab', expected_file_path, actual_file_path])

        delegate = MeldViewerDelegate(blocking_process=False, new_instance=True)
        delegate.non_blocking_process_delay = 0.01
        delegate.view(actual_file_path, expected_file_path)
        popen_mock.assert_called_with(['meld', expected_file_path, actual_file_path])

    @mock.patch('subprocess.call')
    def test_with_blocking_process(self, call_mock):
        actual_file_path = Path('actual')
        expected_file_path = Path('expected')

        delegate = MeldViewerDelegate(blocking_process=True)
        delegate.view(actual_file_path, expected_file_path)
        call_mock.assert_called_with(['meld', '--newtab', expected_file_path, actual_file_path])

        delegate = MeldViewerDelegate(blocking_process=True, new_instance=False)
        delegate.view(actual_file_path, expected_file_path)
        call_mock.assert_called_with(['meld', '--newtab', expected_file_path, actual_file_path])

        delegate = MeldViewerDelegate(blocking_process=True, new_instance=True)
        delegate.view(actual_file_path, expected_file_path)
        call_mock.assert_called_with(['meld', expected_file_path, actual_file_path])

        delegate = MeldViewerDelegate(**{'blocking_process': True, 'new_instance': True})
        delegate.view(actual_file_path, expected_file_path)
        call_mock.assert_called_with(['meld', expected_file_path, actual_file_path])
