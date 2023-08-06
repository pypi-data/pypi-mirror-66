"""Real signature module."""

from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from django.shortcuts import redirect

from appel_crises.data import POSTAL_CODE_TO_DISTRICT, DISTRICT_TO_MP
from appel_crises.mailer import send_mail, MAIN_PERSON, mailing_person
from appel_crises.models import Signature


def sign(request: HttpRequest):
    """Main signature function"""
    try:
        first_name = request.POST['firstname']
        surname = request.POST['surname']
        email = request.POST['email']
    except KeyError:
        return HttpResponseBadRequest()

    signature = Signature(
        first_name=first_name,
        surname=surname,
        email=email,
    )

    try:
        # Validate, among other things, the uniqueness of the email
        signature.full_clean()
    except ValidationError as e:
        # Probably a duplicate email, or a wrong email, or too long values
        return HttpResponseBadRequest(e)

    # I would put a try catch, but at this point i don't know what could go wrong
    signature.save()

    send_mail(
        sender=MAIN_PERSON,
        to=(mailing_person(signature.email, signature.first_name + ' ' + signature.surname),),
        html_content="<p>Thank you for signing</p>",
        text_content="Thank you for signing",
        subject="Thank you for signin"
    )

    return redirect('success')


def search_depute(request: HttpRequest):
    """Take input as POST parameter and return the corresponding depute as JSON"""

    postal_code = request.POST['postal_code']

    if postal_code not in POSTAL_CODE_TO_DISTRICT:
        return HttpResponseNotFound()

    districts = POSTAL_CODE_TO_DISTRICT[postal_code]

    mp_data = [DISTRICT_TO_MP[d] for d in districts if d in DISTRICT_TO_MP]

    # We have to pass safe=False, because we want to serialize an Array, see:
    # https://docs.djangoproject.com/en/3.0/ref/request-response/#serializing-non-dictionary-objects
    return JsonResponse(mp_data, safe=False)
