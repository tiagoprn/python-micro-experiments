# coding: utf-8
"""
MOTIVATION:
    This sends an HTML e-mail only (no attachments, for example) to an specified e-mail address.
    I could use Zurb Inc e-mail marketing templates, for example.

HOW THIS WORKS:
    To keep your e-mail and password safer, create two environment variables on your shell:
        # export EMAIL_ACCOUNT="account@provider.com"
        # export EMAIL_PASSWORD="secret"
            To check if them were created correctly:
                # echo $EMAIL_ACCOUNT
                # echo $EMAIL_PASSWORD
        # If you are using a shell script to set the variables, run it with "." before, to the shell to get the varibles:
            # . script.sh

IMPLEMENTATION NOTES:
    None yet
"""
import os
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

environment_variables = ['SMTP_HOST', 'SMTP_PORT', 'SMTP_HOSTUSER', 'SMTP_HOSTPASSWORD']
exists = True
for var in environment_variables:
    if not os.environ.get(var):
        print "Environment variable '%s' not set." % var
        exists = False
if not exists:
    sys.exit(1)


def py_mail(SUBJECT, BODY, TO, FROM):
    """With this function we send out our html email"""

    # Create message container - the correct MIME type is multipart/alternative here!
    MESSAGE = MIMEMultipart('alternative')
    MESSAGE['subject'] = SUBJECT

    # [*] IMPORTANT: if you are using a list below, you must use the ','.join()
    #            function to cast it to a string, otherwise you'll have
    #            cryptic errors on sendmail() about 'lstrip()'.
    MESSAGE['To'] = TO

    MESSAGE['From'] = FROM
    MESSAGE.preamble = """
Your mail reader does not support the report format.
Please visit us <a href="http://www.mysite.com">online</a>!"""

    # Record the MIME type text/html.
    HTML_BODY = MIMEText(BODY, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    MESSAGE.attach(HTML_BODY)

    # The actual sending of the e-mail
    server = smtplib.SMTP('%s:%s' % (os.environ.get('SMTP_HOST'), os.environ.get('SMTP_PORT')))

    # Print debugging output when testing
    if __name__ == "__main__":
        server.set_debuglevel(1)

    # Credentials (if needed) for sending the mail
    password = "mypassword"

    # Below is required if you are using gmail's SMTP server
    server.ehlo()

    server.starttls()
    server.login(FROM, os.environ.get('SMTP_HOSTPASSWORD'))

    # Below, "TO" must be a list if you have multiple recipients.
    # But also make sure of [*] above.
    server.sendmail(FROM, [TO], MESSAGE.as_string())
    server.quit()

if __name__ == "__main__":
    """Executes if the script is run as main script (for testing purposes)"""

    email_content = u"""
<html lang="en">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <title>html title</title>
  <style type="text/css" media="screen">
    body {
        background-color: #f00;
        color: #fff;
    }
  </style>
</head>
<body>
    <p> <a href="http://zurb.com/ink/"> This </a> is Zurb Inc, which has responsive html mails. </p>
</body>
</html>
"""

    email_subject = "(tag) automatic mail send by my script - SALT %s" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    TO = 'projects@tiagoprnl.me'
    FROM = os.environ.get('SMTP_HOSTUSER')
    py_mail(email_subject, email_content, TO, FROM)
