from exchange.forms import SearchForm
from accounts.forms import *
from accounts.models import *
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import Http404
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.core.exceptions import *

@login_required
def profile(request):
    user = request.user
    try:
        profile = request.user.get_profile()
    except Profile.DoesNotExist:
        profile = Profile(user=user)
        profile.save()
    context = {'user':user}
    if request.POST:
        goback = request.POST.get("goback", '')
        userform = UserForm(request.POST, instance=user)
        profileform = ProfileForm(request.POST, instance=profile)
        if userform.is_valid() and profileform.is_valid():
            userform.save()
            profileform.save()
            context['saved'] = True
    else:
        goback = request.META.get('HTTP_REFERER')
        # FIXME: CHECK REFERER
        userform = UserForm(instance=user)
        profileform = ProfileForm(instance=profile)
    context.update({
        "userform": userform,
        "profileform": profileform,
        "goback": goback,
    })
    context.update(csrf(request))
    return render_to_response("accounts/profile.html", context)

