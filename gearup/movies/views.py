from django.shortcuts import render
# Create your views here.
from .models import Movies
from .serializers import MovieSerializer
from rest_framework import generics
from rest_framework.views import APIView
import imdb
from django.http import JsonResponse
from rest_framework.response import Response

class MovieListView(generics.ListAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        queryset = Movies.objects.all()
        id = self.request.query_params.get('id', None)
        title = self.request.query_params.get('title', None)
        year = self.request.query_params.get('year', None)
        year_gte = self.request.query_params.get('year_gte', None)
        year_lte = self.request.query_params.get('year_lte', None)
        genre = self.request.query_params.get('genre', None)
        if id:
            queryset = queryset.filter(id=id)
        if year:
            queryset = queryset.filter(year=year)
        if title:
            queryset = queryset.filter(title__icontains=title)
        if genre:
            queryset = queryset.filter(genres__icontains=genre)
        if year_gte:
            queryset = queryset.filter(year__gte=year_gte)
        if year_lte:
            queryset = queryset.filter(year__lte=year_lte)
        return queryset[:20]

class MovieUpdateView(generics.UpdateAPIView):
    queryset = Movies.objects.all()
    serializer_class = MovieSerializer
    lookup_field = 'id'

class MovieCreateView(APIView):

    def get(self,request):
        title = self.request.query_params.get('title', None)

        if title:
            mov = Movies.objects.filter(title=title).first()
            if mov:
                serializer = MovieSerializer(mov)
                return  Response(serializer.data)

            else:
                ia = imdb.IMDb()
                movies = ia.search_movie(title)
                if movies:
                    movie = movies[0]
                    m = Movies(title=movie.get('title',None),year=movie.get('year',None),rating=movie.get('rating',0),genres=','.join(movie.get('genres',[])))
                    m.save()
                    serializer = MovieSerializer(m)
                    return Response(serializer.data)
                else:
                    return JsonResponse("Movie title not found", safe=False)
        else:
            return JsonResponse("Must pass title as query parameter", safe=False)

