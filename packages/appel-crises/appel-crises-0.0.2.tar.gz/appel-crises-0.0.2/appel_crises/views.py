"""Module that provides the views of the app."""
from django.http import HttpRequest
from django.shortcuts import render

from appel_crises.models import Signature


def home(request: HttpRequest):
    """Home view."""
    context = dict(
        counter=Signature.get_count(),
    )

    return render(request, "home.html", context=context)


def success(request: HttpRequest):
    """Signature success page"""
    return render(request, "success.html")


def form_no_js(request: HttpRequest):
    return render(request, "form_no_js.html")
