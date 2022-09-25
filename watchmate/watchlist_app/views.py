"""from http.client import HTTPResponse
from django.shortcuts import render
from .models import Movie
from django.http import JsonResponse
# Create your views here.

def movies_list(request):
    movies=Movie.objects.all()
    data={'movies':list(movies.values())}
    return JsonResponse(data)

def movie_detail(request,pk):
    data=Movie.objects.get(pk=pk)
    json={'name':data.name,'description':data.description,'activate':data.activate}
    return JsonResponse(json)
"""