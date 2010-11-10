from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import Http404
from exchange.forms import SearchForm

def about(request):
    context = {
        'searchform': SearchForm,
    }
    return render_to_response("about/about.html", context)

def contact(request):
    context = {
        'searchform': SearchForm,
    }
    return render_to_response("about/contact.html", context)

def faq(request):
    context = {
        'searchform': SearchForm,
    }
    return render_to_response("about/faq.html", context)
