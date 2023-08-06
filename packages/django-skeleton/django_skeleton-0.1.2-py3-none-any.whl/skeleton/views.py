from django.http import HttpResponse


def site_index(request):
    return HttpResponse("this is the SITE index")


def index(request):
    return HttpResponse("this is the (app) index")
