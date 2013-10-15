Mercurial commit message hook for jira
==================================

hg commit hook checks that jira key exist in commit message.

If no jira key provided, hook fails, commit transaction rolled back.

JIRA projects set in regex of checkMessage function
