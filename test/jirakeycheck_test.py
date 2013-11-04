#coding: utf-8

import sys
import unittest
from mock import MagicMock, patch

sys.path.append('../')
import jirakeycheck as jk


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
        return msg


class TestParsedThreadGrab(unittest.TestCase):
    """Test ThreadGrabAudio worker class"""

    def setUp(self):
        self.BAD_COMMIT = True
        self.OK = False
        self.repo = MockRepo()
        self.ui = MockUI()

    def test_correct_commit_msg(self):
        """
        When message fits pattern and jira project exists
        script should pass successfully
        and return FALSE (yep, that's hg invert logic )
        """
        jk.JIRA_PROJECTS = ['MYPRJ']
        r = self.commit('MYPRJ-1 - test')
        self.assertEqual(r, self.OK)

        r = self.commit('MYPRJ-1 - test')
        self.assertEqual(r, self.OK)

        #message can be even empty but with project prefix
        r = self.commit('MYPRJ-1 - ')
        self.assertEqual(r, self.OK)

    def test_no_jira_prj(self):
        """
        When message fits pattern but jira project doesn't exist
        script should fail
        """
        jk.JIRA_PROJECTS = ['MYPRJ']
        r = self.commit('NOPROJ-1 - test')
        self.assertEqual(r, self.BAD_COMMIT)

    def test_bad_commit_msg(self):
        """
         Test all sorts of messages that not pass commit msg pattern:
         <PROJECT-111 - ><commit message>
        """
        jk.JIRA_PROJECTS = ['PRJ']

        r = self.commit('plain commit msg')
        self.assertEqual(r, self.BAD_COMMIT)

        r = self.commit('PRJ-123 commit msg')
        self.assertEqual(r, self.BAD_COMMIT)

        r = self.commit('PRJ- - commit msg')
        self.assertEqual(r, self.BAD_COMMIT)

        r = self.commit('XXX-123 - commit msg')
        self.assertEqual(r, self.BAD_COMMIT)

        r = self.commit('PRJ--123 - commit msg')
        self.assertEqual(r, self.BAD_COMMIT)

    def test_empty_msg(self):
        """
         Message can't be completely empty, it should be with
         jira project name prefix
        """
        jk.JIRA_PROJECTS = ['TEST', 'PRJ']
        r = self.commit('')
        self.assertEqual(r, self.BAD_COMMIT)

    @patch('jirakeycheck.checkMessage')
    def test_check_msg_call(self, test_checkMsg):
        """
        Test that checkMessage has been called
        """
        test_checkMsg.return_value = True
        jk.checkCommitMessage(ui=self.ui, repo=self.repo)
        self.assertTrue(jk.checkMessage.called)

    @patch('jirakeycheck.checkMessage')
    def test_check_msg_ok(self, test_checkMsg):
        """
        Test when checkMessage returns True the script
        finished with success
        """
        test_checkMsg.return_value = True
        res = jk.checkCommitMessage(ui=self.ui, repo=self.repo)
        self.assertEqual(res, self.OK)

    @patch('jirakeycheck.checkMessage')
    def test_check_msg_fail(self, test_checkMsg):
        """
         Test when checkMessage is not passed (returned False)
         the whole script fails and block commit
        """
        test_checkMsg.return_value = False
        res = jk.checkCommitMessage(ui=self.ui, repo=self.repo)
        self.assertEqual(res, self.BAD_COMMIT)

    @patch('jirakeycheck.checkMessage')
    def test_fail_user_message(self, test_checkMsg):
        """
        When script fails and blocks commit, the user
        must see output info message.
        """
        with patch.object(MockUI, 'warn') as self.ui.warn:
            #jk.checkMessage = MagicMock(return_value=False)
            test_checkMsg.return_value = False
            jk.checkCommitMessage(ui=self.ui, repo=self.repo)
            self.assertTrue(self.ui.warn.called)

    def commit(self, msg):
        """
         Emulate commit hook and return hook result:
         False - everything is ok, hook passed
         True - commit didn't pass, hook failed
        """
        self.repo.description = MagicMock(return_value=msg)
        hook_result = jk.checkCommitMessage(ui=self.ui, repo=self.repo)
        return hook_result


if __name__ == '__main__':
    unittest.main()
