import os
import logging
import win32api
from configReader import configReader


class executor(object):

    CONFIGPATH = '_config.ini'

    def __init__(self, commandDict, openDict):
        self.mccLog = logging.getLogger('mcc')
        cfReader = configReader(self.CONFIGPATH)
        self.commandDict = commandDict
        self.openDict = openDict
        self.bossMail = cfReader.readConfig('Boss', 'mail')

    def execute(self, exe, mailHelper):
        self.mailHelper = mailHelper
        subject = exe['subject']
        sender = exe['sender']
        print(sender)
        self.mccLog.info(u'begin to propose order')
        if(sender == self.bossMail):
            self.mailHelper.sendMail('pass', 'Slave')
            if subject in self.commandDict:
                self.mccLog.info(u'execute order')
                try:
                    command = self.commandDict[subject]
                    os.system(command)
                    self.mailHelper.sendMail('Success', 'Boss')
                    self.mccLog.info(u'execute successfully')
                except Exception as e:
                    self.mccLog.error(u'execute order error' + str(e))
                    self.mailHelper.sendMail('error', 'Boss', e)
            elif subject in self.openDict:
                self.mccLog.info(u'open a file')
                try:
                    openFile = self.openDict[subject]
                    win32api.ShellExecute(0, 'open', openFile, '', '', 1)
                    self.mailHelper.sendMail('Success', 'Boss')
                    self.mccLog.info(u'open file success')
                except Exception as e:
                    self.mccLog.error(u'open file error：' + str(e))
                    self.mailHelper.sendMail('error', 'Boss', e)
            elif subject[:7].lower() == 'sandbox':
                self.sandBox(subject[8:])
            else:
                self.mailHelper.sendMail('error', 'boss', 'no such command')
        else:
            return 0



    def sandBox(self, code):
        """sandbox:test.py$n$import win32api$c$if 1 + 1 == 2:$c$$$$$win32api.MessageBox(0, 'sandbox', 'this is sandbox')"""

        name = code.split('$n$')[0]
        code = code.split('$n$')[1]
        codestr = '\n'.join(code.split('$c$'))
        codestr = codestr.replace('$', ' ')
        with open(name, 'a') as f:
            f.write(codestr)
        os.system('python ' + name)
