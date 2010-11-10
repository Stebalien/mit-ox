from exchange import models
from exchange import forms
from exchange.index import complete_indexer
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import Http404
from tagging.models import TaggedItem, Tag
from django.core.paginator import Paginator
from django.core.context_processors import csrf
from django.utils.http import urlencode
from django.db.models import Count
from django.contrib.auth.decorators import login_required

@login_required
def additem(request, mode="buy", category=""):
    if mode not in ('buy', 'sell'):
        raise Http404("You can buy or sell. You can't %s." % mode)
    # initialize context
    user = request.user
    context = {
        "searchform": forms.SearchForm(),
        'mode': mode,
        'user': user,
    }
    # probably slower than a table but it works.
    if category:
        try:
            form = getattr(forms, "%sForm" % category.capitalize())
        except AttributeError:
            raise Http404("Uh... IIRC, %s is not a valid category." % category)

        context['category'] = category
        if request.POST:
            form = form(request.POST, request.FILES)
            if form.is_valid():
                item = form.save(commit=False)
                item.mode = (mode == "buy" and "sell" or "buy")
                item.owner = user
                item.save()
                context["item"] = item
                return render_to_response("additem_done.html", context)
        else:
            form = form()
    else:
        if request.POST:
            form = forms.CategoryForm(request.POST)
            if form.is_valid():
                mode = dict(models.Item.MODE_CHOICES).get(
                    form.cleaned_data["mode"]
                ).lower()
                category = form.cleaned_data["category"]
                return redirect('additem', mode, category)
        else:
            form = forms.CategoryForm()

    # Add the form and csrf
    context.update({'form': form})
    context.update(csrf(request))
    # render
    return render_to_response("additem.html", context)

@login_required
def categories(request, mode):
    if mode not in ('buy', 'sell'):
        raise Http404("You can buy or sell. You can't %s." % mode)
    context = {
        'searchform': forms.SearchForm(),
        'mode': mode,
        'user': request.user,
    }
    return render_to_response("categories.html", context)

@login_required
def search(request, mode):
    #FIXME: THIS CODE IS VERY REDUNDENT/TERRIBLE
    if mode not in ('buy', 'sell'):
        raise Http404("You can buy or sell. You can't %s." % mode)
    user=request.user
    context = {
        'model': models.Item,
        'mode': mode,
        'user': user,
    }
    if request.POST:
        pk = request.POST.get("pk")
        if pk is not None:
            item = models.Item.objects.get(pk=pk)
            item.customers.add(user)
            #FIXME: This should check to make sure that someone
            #       is not claiming the same item twice
            item.save()
            context['claimed_item'] = item
    if request.GET:
        searchform = forms.SearchForm(request.GET)
        if searchform.is_valid():
            query = searchform.cleaned_data["query"]
            category = searchform.cleaned_data["category"]
            tags = searchform.cleaned_data["tags"]

            # Deal with category first
            if category:
                try:
                    model = getattr(models, "%sItem" % category.capitalize())
                    indexer = model.indexer
                except AttributeError:
                    raise Http404("Uh... IIRC, %s is not a valid category." % category)
            else:
                model = models.Item
                indexer = complete_indexer

            # Now perform search if necessary
            if query:
                result_pks = [result.pk
                            for result in indexer.search(query).all()
                            ]
                results = model.objects.available().filter(pk__in=result_pks)
            else:
                results = model.objects.all()

            base_url = "%s?query=%s" % (
                request.path,
                query,
            )
            # Filter by mode now (Stupid search engine)
            results = results.filter(mode__exact=mode)

            # Filter out mine and ones that I have claimed
            results = results.exclude(owner=user).exclude(customers=user)

            # Filter by tags
            if tags:
                results = TaggedItem.objects.get_by_model(results, tags) 

            # Filters
            condition_filter = request.GET.get("condition", '4')
            price_filter = request.GET.get("price", '-1')
            claims_filter = request.GET.get("claims", '3')

            results = results.filter(condition__lte = condition_filter)
            if int(price_filter) >= 0:
                results = results.filter(price__lte = price_filter)
            results = results.annotate(claims=Count('customers', distinct=True))
            if int(claims_filter) >= 0:
                results = results.filter(claims__lt = claims_filter)

    else:
        searchform = forms.SearchForm()
        condition_filter = '4'
        price_filter = '-1'
        claims_filter = '3'
        category = ''
        model = models.Item
        base_url = "%s?query=" % request.path
        # get the results and filter
        results = model.objects.all()
        ## Filter by mode now
        results = results.filter(mode__exact=mode)
        ## Filter out mine and ones that I have claimed
        results = results.exclude(owner=user).exclude(customers=user)
        ## Claims
        results = results.annotate(claims=Count('customers', distinct=True))
        results = results.filter(claims__lt = claims_filter)

    # Paginate
    if results:
        paginator = Paginator(results, 5)
        items = paginator.page(int(request.GET.get('page', 1)))
    else:
        items = None
    context.update({
        'condition_filter': condition_filter,
        'price_filter': price_filter,
        'claims_filter': claims_filter,
        'base_url': base_url,
        'items': items,
        'searchform': searchform,
        'category': category,
        'tags': Tag.objects.cloud_for_model(model),
    })
    context.update(csrf(request))
    return render_to_response("results.html", context)

@login_required
def transactions(request):
    context = {
        'searchform': forms.SearchForm(),
    }
    return render_to_response("transactions.html", context)

