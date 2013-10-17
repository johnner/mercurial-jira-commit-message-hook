#coding: utf-8
import re
#If the hook returns True - hook fails
BAD_COMMIT = True
OK = False
#List of the available JIRA projects
JIRA_PROJECTS = ['PRJ', 'TEST']


def checkCommitMessage(ui, repo, **kwargs):
    """Checks commit message for matching commit rule:
    Every commit message must include JIRA issue key
    Example:

    PRJ-42 - added meaning of life

    Include this hook in .hg/hgrc

    [hooks]
    pretxncommit.jirakeycheck = python:/path/jirakeycheck.py:checkCommitMessage
    """
    hg_commit_message = repo['tip'].description()
    if checkMessage(hg_commit_message) is False:
        printUsage(ui)
        #reject commit transaction
        return BAD_COMMIT
    else:
        return OK


def checkAllCommitMessage(ui, repo, node, **kwargs):
    """
    For pull: checks commit messages for all incoming commits
    It is good for master repo, when you pull a banch of commits

    [hooks]
    pretxnchangegroup.jirakeycheckall =
        python:/path/jirakeycheck.py:checkAllCommitMessage
    """
    for rev in xrange(repo[node].rev(), len(repo)):
        message = repo[rev].description()
        if checkMessage(message) is False:
            ui.warn(
                "Revision "
                + str(rev)
                + " commit message:["
                + message
                + "] | JIRA issue key is not set\n"
            )
            printUsage(ui)
            #reject
            return BAD_COMMIT
    return OK


def checkMessage(msg):
    """
    Checks message for matching regex

    Correct message example:
    PRJ-123 - your commit message here

    #"PRJ-123 - " is necessary prefix here
    """
    is_correct = False
    re_names = '|'.join(['%s-\d+' % name for name in JIRA_PROJECTS])
    p = re.compile('^(%s) - ' % re_names)
    res = p.search(msg)
    if res:
        is_correct = True
    return is_correct


def printUsage(ui):
    ui.warn('=====\n')
    ui.warn('Commit message must have JIRA issue key\n')
    ui.warn('Example:\n')
    ui.warn('PRJ-42 - the answer to life, universe and everything \n')
    ui.warn('=====\n')
