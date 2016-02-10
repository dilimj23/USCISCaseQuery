import urllib
from BeautifulSoup import *

global update
update = ""

def get_status(case_number):
    global update
    url = "https://egov.uscis.gov/casestatus/mycasestatus.do?changeLocale=&appReceiptNum=%s&initCaseSearch=CHECK+STATUS" % (case_number)
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html)
    tags = soup('p')
    for tag in tags:
        text = tag.getText()
        if case_number in text and "we received" not in text:
            update = text
            return True
    return False

def send_email(user, pwd, recipient, subject, body):
    import smtplib

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)
    server.sendmail(FROM, TO, message)
    server.close()
    print 'successfully sent the mail'



case_number = YourCaseNum
user = userid
pwd = password
recipient = recipientemail
subject = "case update"
if get_status(case_number):
    body = update
    send_email(user, pwd, recipient, subject, body)