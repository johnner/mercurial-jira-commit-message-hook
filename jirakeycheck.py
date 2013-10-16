#coding: utf-8
import re
#If the hook returns True - hook fails
BAD_COMMIT = True
OK = False

def checkCommitMessage(ui, repo, **kwargs):
    """
    	Checks commit message for matching commit rule:
	Every commit message must include JIRA issue key
	Example:
	
	PRJ-42 - added meaning of life

	Include this hook in .hg/hgrc

	[hooks]
	pretxncommit.jirakeycheck = python:/path/to/jirakeycheck.py:checkCommitMessage
	
    """	
    hg_commit_message = repo['tip'].description()
    if(checkMessage(hg_commit_message) == False):
        printUsage(ui)
		
	#reject commit transaction
        return BAD_COMMIT
    else:
        return OK
	return BAD_COMMIT

def checkAllCommitMessage(ui, repo, node, **kwargs):
    """
	For push: checks commit messages for all incoming commits
	
    [hooks]
	pretxnchangegroup.jirakeycheckall = python:/path/to/jirakeycheck.py:checkAllCommitMessage
    """
    for rev in xrange(repo[node].rev(), len(repo)):
        message = repo[rev].description()
        if(checkMessage(message) == False):
            ui.warn("Ревизия "+str(rev)+" commit message:["+message+"] | не указан номер задачи JIRA\n")
            printUsage(ui)
	    #reject
            return BAD_COMMIT
    return OK

def checkMessage(msg):
	"""
	Checks message for matching regex

	Correct message example:
	#"JIRAPROJ-123 -" necessary prefix
	JIRAPROJ-123 - your commit message here
	"""
	is_correct = False
	p = re.compile('^(JIRAPROJ-\d+|JIRAPROJ2-\d+) - ')
	r = p.search(msg)
	if r:
		is_correct = True
	return is_correct

def printUsage(ui):
	ui.warn('=====\n')
	ui.warn('Commit message must have JIRA issue key\n')
	ui.warn('Example:\n')
	ui.warn('JIRAPRO-42 - the answer to life, universe and everything \n')
	ui.warn('=====\n')
