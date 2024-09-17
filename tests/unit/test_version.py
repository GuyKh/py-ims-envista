"""Test Version."""
import unittest

import pytest

from ims_envista.version import Version


class TestVersion(unittest.TestCase):
    """Test Version."""

    def test_set_version(self) -> None:
        ver = Version("1.0.0")
        if ver.number != "1.0.0":
            msg = "Expected Version 1.0.0"
            raise ValueError(msg)

    def test_version_immutable(self) -> None:
        ver = Version("1.0.0")
        with pytest.raises(TypeError):
            ver.number = "1.1.0"
