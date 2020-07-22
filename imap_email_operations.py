# coding: utf-8
"""
MOTIVATION:
    Various operations that can be performed on IMAP mail boxes.
    And also on MS-Exchange (once you get its IMAP server address), as this link shows:
    http://stackoverflow.com/questions/288546/connect-to-exchange-mailbox-with-python


HOW THIS WORKS:
    To keep your e-mail and password safer, create two environment variables on your shell:
        LINUX:
            # export EMAIL_ACCOUNT=account@provider.com
            # export EMAIL_PASSWORD=secret
            # export IMAP_SERVER=imap.domain.com
                To check if them were created correctly:
                    # echo $EMAIL_ACCOUNT
                    # echo $EMAIL_PASSWORD
                    # echo $IMAP_SERVER
        WINDOWS:
            # set EMAIL_ACCOUNT=account@provider.com
            # set EMAIL_PASSWORD=secret
            # set IMAP_SERVER=imap.domain.com
                To check if them were created correctly:
                    # echo %EMAIL_ACCOUNT%
                    # echo %EMAIL_PASSWORD%
                    # echo %IMAP_SERVER%
        => Make sure to not put double-quotes or quotes wrapping the environment
        variables' values. This leads to not being able to connect with 'getaddinfo'
        cryptic error, but in fact that is because the domains won't resolve with
        double or single quotes.

IMPLEMENTATION NOTES:
    * For this to work, you have to:
        $ pip install Unidecode
    * Based on code from http://pymotw.com/2/imaplib/
    * http://bioportal.weizmann.ac.il/course/python/PyMOTW/PyMOTW/docs/imaplib/index.html
    * http://bitsofpy.blogspot.com.br/2010/05/python-and-gmail-with-imap.html
    * http://segfault.in/2010/07/playing-with-python-and-gmail-part-1/
    * http://segfault.in/2010/08/playing-with-python-and-gmail-part-2/
    * http://yuji.wordpress.com/2011/06/22/python-imaplib-imap-example-with-gmail/
"""

import re
import sys
import traceback
import logging
import imaplib
import email
from os import environ, path, mkdir, sep
from datetime import datetime
from email.parser import HeaderParser
from unidecode import unidecode

# Constants section
DEBUG_MODE = True
ENVIRONMENT_VARIABLES = ['EMAIL_ACCOUNT', 'EMAIL_PASSWORD', 'IMAP_SERVER']
USE_SSL = True
SSL_PORT = 993  # gmail default port
ROOT_PATH = path.realpath(path.dirname(__file__))
MAIN_OUTPUT_DIR = path.join('D:\TEMP', 'OUTPUT')
ATTACHMENTS_OUTPUT_DIR = path.join(MAIN_OUTPUT_DIR, datetime.now().strftime('%Y%m%d_%H%M%S'))
SLUGIFY_REGEX = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
LOG_FILE_NAME = ROOT_PATH + sep + __file__.split('.')[0]+'.log'

# Sets up the logging
logging.basicConfig(filename = LOG_FILE_NAME,
                    format = "[%(asctime)s - PID %(process)s - %(module)s.py - %(levelname)s] %(message)s",
                    filemode='a',  # or 'w' to write a new file at each execution
                    level=logging.DEBUG if DEBUG_MODE else logging.ERROR)


def get_exception_full_stacktrace(e):
    trace = traceback.format_tb(sys.exc_info()[2])
    unicode_trace = []
    for elem in trace:
        unicode_trace.append(elem.decode('utf8'))
        trace_str = u'\n'.join(unicode_trace)
        excecao = u'EXCEPTION: "%s"\t- EXCEPTION TYPE: "%s"\t- TRACEBACK:\t%s' % (
            e, type(e), trace_str)
        unicode_trace.append(excecao)
    return '\n'.join(unicode_trace)


def slugify(text, delim = u'-'):
    """
    Generates an ASCII-only slug.
    ( reference: http://flask.pocoo.org/snippets/5/ )
    """
    result = []
    for word in SLUGIFY_REGEX.split(text.lower()):
        result.extend(unidecode(word).split())
    return unicode(delim.join(result))


def sanitize_filename(file_name):
    file_extension = file_name.split('.')[-1]
    file_name = file_name.replace('.%s' % file_extension, '')
    file_name = slugify(file_name) + '.' + file_extension
    return file_name


class IMAPStorage(object):
    def __init__(self):
        try:
            if self.environment_variables_not_set():
                raise Exception(u"%s" % repr("\n".join(self.environment_variables_not_set())))

            if USE_SSL:
                self.imap_mailbox = imaplib.IMAP4_SSL(environ.get('IMAP_SERVER'), SSL_PORT)
            else:
                self.imap_mailbox = imaplib.IMAP4(environ.get('IMAP_SERVER'))
            self.imap_mailbox.login(environ.get('EMAIL_ACCOUNT'), environ.get('EMAIL_PASSWORD'))

            if not path.exists(MAIN_OUTPUT_DIR):
                mkdir(MAIN_OUTPUT_DIR)

            if not path.exists(ATTACHMENTS_OUTPUT_DIR):
                mkdir(ATTACHMENTS_OUTPUT_DIR)

        except Exception, e:
            raise Exception(u"Couldn't create an IMAPStorage instance: %s" % get_exception_full_stacktrace(e))
            sys.exit(1)

    def environment_variables_not_set(self):
        not_set = []
        for var in ENVIRONMENT_VARIABLES:
            if not environ.get(var):
                not_set.append("Environment variable '%s' not set." % var)
            else:
                logging.debug("%s : %s" % (var, environ.get(var)))
        return not_set

    def get_all_mailboxes(self):
        mailboxes = []
        for item in self.imap_mailbox.list()[1]:
            # TODO: GMAIL SPECIFIC RULE?
            mailbox_name = item.split(' "/" ')[-1]
            status, data = self.imap_mailbox.select(mailbox_name)
            if status != 'OK':
                logging.debug("Mailbox %s parsed but does not exist, will be ignored." % mailbox_name)
            else:
                mailboxes.append(mailbox_name)
        return mailboxes

    def get_total_mails_from_mailbox(self, mailbox_name):
        typ, data = self.imap_mailbox.select(mailbox_name)
        return int(data[0])

    def get_total_unread_mails_from_mailbox(self, mailbox_name):
        typ, data = self.imap_mailbox.status(mailbox_name, "(UNSEEN)")
        total = re.search("UNSEEN (\d+)", data[0]).group(1)
        return total

    def get_message_headers(self, message_content):
        headers_fields = ['From', 'To', 'Subject', 'Date']
        headers = {}
        parser = HeaderParser().parsestr(message_content)
        for field in headers_fields:
            headers[field] = parser[field]
        return headers

    def get_content_types(self, message_content):
        mail = email.message_from_string(message_content)
        parts = []
        for part in mail.walk():
            part_dict = {}
            part_dict['Content-Type'] = part.get_content_type()
            part_dict['Main Content'] = part.get_content_maintype()
            part_dict['Sub Content'] = part.get_content_subtype()
            parts.append(part_dict)
        return parts

    def get_message_body(self, message_content):
        mail = email.message_from_string(message_content)
        body = []
        for part in mail.walk():
            # multipart are just containers, so we skip them
            if part.get_content_maintype() == 'multipart':
                continue
            # TODO: Improve below to get also html messages
            # we are interested only in the simple text messages
            if part.get_content_subtype() != 'plain':
                continue

            text_message_body = part.get_payload()
            body.append(text_message_body)
        return body

    def extract_attachments_and_save_to_disk(self, message_content, message_id):
        mail = email.message_from_string(message_content)
        parts = mail.get_payload()
        for part in parts:
            if not isinstance(part, basestring):  # if it is not a string
                if (part.get_filename() is None) or (part.get_filename().strip() == ''):
                    continue

                where_to_save = ATTACHMENTS_OUTPUT_DIR + sep + message_id + sep
                if not path.exists(where_to_save):
                    mkdir(where_to_save)
                file_to_save = where_to_save + sanitize_filename(unicode(part.get_filename()))

                file_object = open(file_to_save, 'w')  # 'w' or wb'?

                if part.get_content_maintype() == 'text':  # text file
                    file_object = open(file_to_save, 'w')
                else:  # binary file
                    file_object = open(file_to_save, 'wb')

                content = part.get_payload(decode=True)

                file_object.write(content)
                file_object.close()

                logging.debug("File SAVED: '%s'" % file_to_save)

    #TODO: Clean this code, it is ugly
    def convert_email_header_received_date_to_localtime(self, msg_receive_date):
        from email.utils import parsedate_tz, mktime_tz
        date_tuple = parsedate_tz(msg_receive_date)
        if date_tuple:
            local_date = datetime.fromtimestamp(mktime_tz(date_tuple)).strftime("%Y-%m-%d %H:%M:%S")
            return local_date
        else:
            return 'CONVERSION ERROR'

    def get_all_mails_from_mailbox(self, mailbox_name, get_attachments=False):
        typ, data = self.imap_mailbox.select(mailbox_name)
        status, content = self.imap_mailbox.search(None, 'ALL')
        for message_number in content[0].split():
            message_id = "%s-%s-%s" % (mailbox_name, datetime.now().strftime('%Y%m%d%H%M%S%f'), str(message_number))

            resp, data = self.imap_mailbox.fetch(message_number, '(RFC822)')

            headers = self.get_message_headers(data[0][1])

            logging.debug(repr(headers))

            content_types = self.get_content_types(data[0][1])
            message_body = self.get_message_body(data[0][1])

            if get_attachments:
                self.extract_attachments_and_save_to_disk(message_id = message_id,
                                                          message_content = data[0][1])

'''
    TODO:
            get_all_mails_from_mailbox(mailbox)
            get_mails_from_mailbox_by_subject(mailbox, subject)
            get_mails_from_mailbox_by_sender(mailbox, sender)
            get_mails_from_mailbox_by_recipient(mailbox, recipient)
            get_mail_headers(mail)
            get_mail_body(mail)
            get_mail_attachment(mail)
            delete_mail(mailbox, mail)
    '''

if __name__ == "__main__":
    try:
        logging.debug("executing... [WAIT]")
        imap_mailbox = IMAPStorage()
        if DEBUG_MODE:
            logging.debug("CONNECTED")

        logging.debug("MAILBOXES AVAILABLE:")
        for mailbox in imap_mailbox.get_all_mailboxes():
            unread_count = imap_mailbox.get_total_unread_mails_from_mailbox(mailbox)
            total_mails = imap_mailbox.get_total_mails_from_mailbox(mailbox)
            logging.debug("Mailbox {{%s}} has {{%s}} TOTAL message(s)." % (mailbox, str(total_mails)))
            logging.debug("Mailbox {{%s}} has {{%s}} UNREAD message(s)." % (mailbox, str(unread_count)))

        logging.debug("ALL MAILS FROM [INBOX]:")
        imap_mailbox.get_all_mails_from_mailbox("INBOX")

        # TODO: make the other operations here

        logging.debug("disconnecting from the imap server...")

        imap_mailbox.imap_mailbox.close()
        imap_mailbox.imap_mailbox.logout()

        logging.debug("executing... [DONE]")
    except Exception, e:
        logging.error(get_exception_full_stacktrace(e), error=True)
        sys.exit(1)
