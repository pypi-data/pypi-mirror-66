from unittest import TestCase
from unittest.mock import Mock, patch


class TestWasdi(TestCase):

    @patch
    def test_get_workspaces(self):
        self.assert_(True, )
