Mercurial hook for jira
==================================

The Mercurial hook checks that jira key exist in commit message.

If no jira key provided, hook fails and commit transaction rollback.

JIRA projects set in regex of checkMessage function

Installation
------------
1. Copy `jirakeycheck.py` to ~/.hg (or any dir you like)
2. Add the following line to $HOME/.hgrc
<div>
<pre>
[hooks]
   pretxncommit.jirakeycheck = python:~/.hg/jirakeycheck.py:checkCommitMessage
   pretxnchangegroup.jirakeycheckall = python:~/.hg/jirakeycheck.py:checkAllCommitMessage
</pre>

</div>

3. Set your JIRA project keys in `JIRA_RE` regexp in jirakeycheck.py
