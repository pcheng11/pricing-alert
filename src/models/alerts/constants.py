import os

COLLECTION = 'alerts'
ALERT_TIMEOUT = 10
URL = os.environ.get('MAILGUN_URL')
    #"https://api.mailgun.net/v3/sandboxbbc37c59039e4e428a66d2bf6f0f8510.mailgun.org/messages"
API_KEY = os.environ.get('MAILGUN_API_KEY')
    # "a0a4e49afef04624325ef846b38aa880-060550c6-3739d00a"
FROM = os.environ.get('MAILGUN_FROM')
#"Mailgun Sandbox <postmaster@sandboxbbc37c59039e4e428a66d2bf6f0f8510.mailgun.org>"
