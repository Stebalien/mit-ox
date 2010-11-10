from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse

def index(request):
    #TODO: Make this fetch "hot" items.
    if request.GET:
        buy, sell, query = request.GET.get("buy"), request.GET.get("sell"), request.GET.get("query")
        mode = (buy and "buy") or (sell and "sell") or "buy"
        if query:
            base = reverse('search', args=[mode])
            return redirect("%s?query=%s" % (base, query))
        else:
            return redirect('categories', mode=mode)
    else:
        return render_to_response("homepage.html")
