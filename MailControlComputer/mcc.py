#-*-coding:utf-8 -*-

import time
import logging
from utils.mailHelper import mailHelper
from utils.excutor import executor
from utils.configReader import configReader

__Author__ = 'kingname'
__oldVersion__ = 'based on 0.5 & 0.6'

__Modifier__ = 'wkee'
__Version__ = '1.0'
__Environment__ = 'Python 3.5.2'

logger = logging.getLogger('mcc')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

fh = logging.FileHandler('mccLog.log')
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)
fh.setFormatter(formatter)

logger.addHandler(ch)
logger.addHandler(fh)

class MCC(object):
    CONFIGPATH = '_config.ini'
    KEY_COMMAND = 'Command'
    KEY_OPEN = 'Open'
    KEY_BOSS = 'Boss'
    KEY_TIMELIMIT = 'timelimit'

    def __init__(self):
        self.mailHelper = mailHelper()
        self.configReader = configReader(self.CONFIGPATH)
        commandDict = self.configReader.getDict(self.KEY_COMMAND)
        openDict = self.configReader.getDict(self.KEY_OPEN)
        self.timeLimit = int(self.configReader.readConfig(self.KEY_BOSS, self.KEY_TIMELIMIT))
        self.excutor = executor(commandDict, openDict)
        self.toRun()

    def toRun(self):
        while True:
            self.mailHelper = mailHelper()
            self.run()
            time.sleep(self.timeLimit)

    def run(self):
        mailBody = self.mailHelper.acceptMail()
        if mailBody:
            exe = self.mailHelper.analysisMail(mailBody)
            if exe != None:
                self.excutor.execute(exe, self.mailHelper)

if __name__=='__main__':
        mcc = MCC()
