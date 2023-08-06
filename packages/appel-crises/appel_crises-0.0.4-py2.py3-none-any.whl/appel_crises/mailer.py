"""Python module that manages the emails for the app.

It uses SendinBlue API as documented here : https://developers.sendinblue.com/reference

"""
from datetime import datetime
from typing import Dict, Iterable, Tuple, List

import requests

from appel_crises.settings import SENDIN_BLUE_API_KEY, MAIN_EMAIL, MAIN_NAME

SB_SEND_MAIL_URL = "https://api.sendinblue.com/v3/smtp/email"

SB_FETCH_EVENTS_URL = "https://api.sendinblue.com/v3/smtp/statistics/events"

SB_POST_HEADERS = {
    'accept': "application/json",
    'content-type': "application/json",
    'api-key': SENDIN_BLUE_API_KEY
}

SB_GET_HEADERS = {
    'accept': "application/json",
    'api-key': SENDIN_BLUE_API_KEY
}


MailingPerson = Dict[str, str]


def mailing_person(email: str, name: str = None) -> MailingPerson:
    """Build a MailingPerson dict."""
    if name is not None:
        return dict(name=name, email=email)
    else:
        return dict(email=email)


MAIN_PERSON = mailing_person(MAIN_EMAIL, MAIN_NAME)


def send_mail(sender: MailingPerson,
              to: Iterable[MailingPerson],
              html_content: str,
              subject: str,
              text_content: str = "",
              bcc: Iterable[MailingPerson] = None,
              cc: Iterable[MailingPerson] = None):
    """Uses SendinBlue API to send an email"""

    body = dict(
        sender=sender,
        to=to,
        htmlContent=html_content,
        textContent=text_content,
        subject=subject,
    )

    if bcc is not None:
        body['bcc'] = bcc

    if cc is not None:
        body['cc'] = cc

    response = requests.post(SB_SEND_MAIL_URL, headers=SB_POST_HEADERS, json=body)

    return response.json()


def get_delivered_emails(offset: int, limit: int = 100) -> List[Tuple[str, datetime]]:
    """Fetch the delivered emails."""
    params = dict(offset=offset, limit=limit, event="delivered")

    response = requests.get(SB_FETCH_EVENTS_URL, headers=SB_GET_HEADERS, params=params)

    data = response.json()
    if 'events' not in data:
        return []

    result = [(e['email'], datetime.fromisoformat(e['date'])) for e in data['events']]

    return result
