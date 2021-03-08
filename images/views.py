from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from .models import Image
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from django.http import HttpResponse
from django.core.paginator import Page, Paginator, EmptyPage,\
                                PageNotAnInteger

# Create your views here.

@login_required
def image_create(request):
    """
    1.You expect initial data via GET in order to create an instance of the form.
    This data will consis of the url and title attributes of an image from an external
    website and will be provided via GET by the JS tool that you will create.
    For now, you just assume that this data will be there initially.
    2.If the form submitted, you check whether it is valid. if the form data is valid,
    you create a new Image instance, but prevent the object form being saved to
    the DB yet passing commit=False to the forms save method.
    3. You Assign the current user to the new image object. This is how you can
    know who uploaded each image
    4. You save the image object to the DB
    5. Finally you create a success msg using the Django mssaging framework
    and redirect the user to the canonical URL of the new image. You havent yet implemented
    the get_absolute_url() method for the Image model; you will do that later.
    """
    if request.method == 'POST':
        # form is sent
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # form data is valid
            cd = form.cleaned_data
            new_item = form.save(commit=False)

            #assign current user to the item
            new_item.user = request.user
            new_item.save()
            messages.success(request, 'Imagen añadida exitosamente')

            # redirect to new created item detail view
            return redirect(new_item.get_absolute_url())
    else:
        # build form with data provided by the bookmarklet via GET
        form = ImageCreateForm(data=request.GET)

    return render(request, 'images/image/create.html', {'section': 'images', 'form' : form})


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request, 'images/image/detail.html', {'section': 'images', 'image': image})

@ajax_required
@login_required
@require_POST
def image_like(request):
    """ 
    You use two decorator for your view. The login_required decorator prevents
    users who are not logged in from accessing this view. The require_POST decorator
    returns an HttpResponseNotAllowed object (status code 405) if the HTTP request
    is not done via POST. this way, you only allow POST request for this view.

    Django also provides a require_GET decorator to only allow GET requests and
    require_http_methods decorator to which you can pass a list of allowed methods
    as an argument.

    image_id: The ID of the image object on which the user is performing the action
    action: the action that the user wants to perform, which you assume to be
    a string with the value like or unlike.

    You use the manager provided by Django for the users_like many-to-many field of
    the Image model in order to add or remove objects from the relationship using the
    add() or remove() methods. clear() removes all objects from the related object set.

    Finally you use the JsonResponse class provided by Django, which returns an Http
    response with an application/json content type, converting the given object
    into a JSON output.
    """
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'error'})


@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 4)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # If the request is AJAX and the page is out of range
            # return an empty page
            return HttpResponse('')
        # If page is out of range deliver last page of results
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'images/image/list_ajax.html', {'section': 'images', 'images': images})
    return render(request, 'images/image/list.html', {'section': 'images', 'images': images})
