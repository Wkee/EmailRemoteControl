
from email.mime.text import MIMEText
from configReader import configReader
import logging
import poplib
import smtplib
import re

class mailHelper(object):
    CONFIGPATH = '_config.ini'

    def __init__(self):
        self.mccLog = logging.getLogger('mcc')
        cfReader = configReader(self.CONFIGPATH)
        self.pophost = cfReader.readConfig('Slave', 'pophost')
        self.smtphost = cfReader.readConfig('Slave', 'smtphost')
        self.port = cfReader.readConfig('Slave', 'port')
        self.username = cfReader.readConfig('Slave', 'username')
        self.password = cfReader.readConfig('Slave', 'password')
        self.bossMail = cfReader.readConfig('Boss', 'mail')
        self.loginMail()
        self.configSlaveMail()

    def loginMail(self):
        self.mccLog.info(u'start to login in')
        try:
            self.pp = poplib.POP3_SSL(self.pophost)
            self.pp.set_debuglevel(1)
            self.pp.user(self.username)
            self.pp.pass_(self.password)
            self.pp.list()
            print(u'login successfully!')
            self.mccLog.info(u'login mailbox successfully!')
        except Exception as e:
            print(u'login in error!')
            self.mccLog.error(u'login in error!' + str(e))
            exit()

    def acceptMail(self):
        self.mccLog.info(u'start to capture mail')
        try:
            ret = self.pp.list()
            mailBody = self.pp.retr(len(ret[1]))
            self.mccLog.info(u'capture success')
            return mailBody
        except Exception as e:
            self.mccLog.info(u'capture failure, as {}'.format(e))
            return None

    def analysisMail(self, mailBody):
        self.mccLog.info(u'start to capture mail subject and sender')
        try:
            subject = re.search("'(s|S)ubject: (.*?)'", str(mailBody[1])).group(2)
            sender = re.search("'X-Sender: (.*?)',", str(mailBody[1])).group(1)

            # self.mccLog.debug('subject is:{}'.format(subject))
            # self.mccLog.debug('sender is:{}'.format(sender))


            command = {'subject': subject, 'sender': sender}
            self.mccLog.info(u'capture mail subject and sender success')
            return command
        except Exception as e:
            self.mccLog.error(u'capture subject and sender failure' + str(e))
            return None

    def configSlaveMail(self):
        self.mccLog.info(u'start to set out')
        try:
            self.handle = smtplib.SMTP(self.smtphost, self.port)
            self.handle.login(self.username, self.password)
            self.mccLog.info(u'outbox set success')
        except Exception as e:
            self.mccLog.error(u'outbox set error' + str(e))
            exit()

    def sendMail(self, subject, receiver, body='Success'):
        msg = MIMEText(body, 'plain', 'utf-8')  # only Chinese need parameter 'utf=8', single character no need
        msg['Subject'] = subject
        msg['from'] = self.username
        self.mccLog.info(u'start to send mail to {}'.format(receiver))
        if receiver == 'Slave':
            try:
                self.handle.sendmail(self.username, self.username, msg.as_string())
                self.mccLog.info(u'send to Slave success')
                return True
            except Exception as e:
                self.mccLog.info(u'send to Slave failure, as {}'.format(e))
                return False

        elif receiver == 'Boss':
            try:
                self.handle.sendmail(self.username, self.bossMail, msg.as_string())
                self.mccLog.info(u'send to Boss success')
            except Exception as e:
                self.mccLog.error(u'send to Boss success failure, as {}'.format(e))
                return False

# if __name__ == '__main__':
#     mail = mailHelper()
#     body = mail.acceptMail()
#     print(body)
#     print(mail.analysisMail(body))
#     # mail.sendMail('OK','Slave')
