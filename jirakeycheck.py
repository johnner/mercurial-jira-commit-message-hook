#coding: utf-8
import re
#Если хук возвращает True - условия не удовлетворены, хук отвалится
BAD_COMMIT = True
OK = False
# Jira regexp
JIRA_RE = '^(JIRAPROJ-\d+|JIRAPROJ2-\d+) - '

def checkCommitMessage(ui, repo, **kwargs):
    """
	Проверяет сообщение коммита на соответствие правилу
	Коммит должен содержать номер задачи в JIRA.
	Пример:
	
	PRJ-42 - added meaning of life

	Чтобы включить нужно добавить в проектный .hg/hgrc
	или в локальный hgrc следующее:

	[hooks]
	pretxncommit.jirakeycheck = python:/path/to/jirakeycheck.py:checkCommitMessage
	
    """	
    hg_commit_message = repo['tip'].description()
    if(checkMessage(hg_commit_message) == False):
        printUsage(ui)
		
		#Все плохо, откатываем транзакцию
        return BAD_COMMIT
    else:
        return OK
	return BAD_COMMIT

def checkAllCommitMessage(ui, repo, node, **kwargs):
    """
	Для push: проверяет сообщения всех входящих коммитов на наличие номера задачи в JIRA
	
    [hooks]
	pretxnchangegroup.jirakeycheckall = python:/path/to/jirakeycheck.py:checkAllCommitMessage
    """
    for rev in xrange(repo[node].rev(), len(repo)):
        message = repo[rev].description()
        if(checkMessage(message) == False):
            ui.warn("Ревизия "+str(rev)+" commit message:["+message+"] | не указан номер задачи JIRA\n")
            printUsage(ui)
			#Все плохо, откатываем транзакцию
            return BAD_COMMIT
    return OK

def checkMessage(msg):
	"""
	Проверяет сообщение по регулярке

	Пример коммита:
	#"JIRAPROJ-123 -" необходимый префикс
	JIRAPROJ-123 - комментарий к коммиту
	"""
	is_correct = False
	p = re.compile(JIRA_RE)
	r = p.search(msg)
	if r:
		is_correct = True
	return is_correct

def printUsage(ui):
	ui.warn('=====\n')
	ui.warn('Комментарий к коммиту должен содержать номер задачи в JIRA\n')
	ui.warn('Пример:\n')
	ui.warn('AVIAFE-42 - Ответ на главный вопрос жизни, вселенной и всего такого\n')
	ui.warn('=====\n')
