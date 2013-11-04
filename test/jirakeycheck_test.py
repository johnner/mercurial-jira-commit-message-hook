#coding: utf-8

import sys
import unittest
from mock import MagicMock, patch

sys.path.append('../')
import jirakeycheck as jk
#from jirakeycheck import checkCommitMessage, checkMessage


class MockRepo():
    """ Mock for mercurial repo object which is sent by enviroment """

    def __getitem__(self, item):
        """ for simplicity all sub-methods present in same class """
        return self

    def description(self):
        return "mocked description"


class MockUI():
    """
    Mock for UI object. It's used for user interaction like
    sending the message on screen.
    """
    def warn(self, msg):
        print msg


class TestParsedThreadGrab(unittest.TestCase):
    """Test ThreadGrabAudio worker class"""

    def setUp(self):
        self.BAD_COMMIT = True
        self.OK = False
        self.repo = MockRepo()
        self.ui = MockUI()

    def test_check_msg_call(self):
        """
        Test that checkMessage has been called
        """
        jk.checkMessage = MagicMock(return_value=True)
        jk.checkCommitMessage(ui=self.ui, repo=self.repo)
        self.assertTrue(jk.checkMessage.called)

    def test_check_msg_ok(self):
        """
        Test when checkMessage returns True the script
        finished with success
        """
        jk.checkMessage = MagicMock(return_value=True)
        res = jk.checkCommitMessage(ui=self.ui, repo=self.repo)
        self.assertEqual(res, self.OK)

    def test_check_msg_fail(self):
        """
         Test when checkMessage is not passed (returned False)
         the whole script fails and block commit
        """
        jk.checkMessage = MagicMock(return_value=False)
        res = jk.checkCommitMessage(ui=self.ui, repo=self.repo)
        self.assertEqual(res, self.BAD_COMMIT)

    def test_fail_user_message(self):
        """
        When script fails and blocks commit, the user
        must see output info message.
        """
        with patch.object(MockUI, 'warn') as self.ui.warn:
            jk.checkMessage = MagicMock(return_value=False)
            jk.checkCommitMessage(ui=self.ui, repo=self.repo)
            self.assertTrue(self.ui.warn.called)

if __name__ == '__main__':
    unittest.main()
