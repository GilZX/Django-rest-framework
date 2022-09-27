

from watchlist_app.models import WatchList,StreamPlataform,Review
from .serializers import WatchListSerializer,StreamPlatafotmSerializer,ReviewsSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins


from rest_framework import viewsets
from rest_framework.exceptions  import ValidationError


from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from watchlist_app.api.permissions import AdminOrReadOnly,ReviewUserOrReadOnlt


#Para Filtrar los datos con django -filter 
###############################################################
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
###############################################################

class WatchListFilter(generics.ListAPIView):
    queryset=WatchList.objects.all()
    serializer_class=WatchListSerializer
    #filter_backends=[DjangoFilterBackend]
    #filterset_fields=['title','plataform__name','avg_rating']
    filter_backends=[filters.SearchFilter]
    search_fields=['title','plataform__name','avg_rating']



class ReviewCreate(generics.CreateAPIView):


    serializer_class=ReviewsSerializer

    def get_queryset(self):
        return Review.objects.all()
    def perform_create(self, serializer):
        pk=self.kwargs.get('pk')
        movie=WatchList.objects.get(pk=pk)
        review_user=self.request.user
        review_Queryset=Review.objects.filter(watchlist=movie,review_user=review_user)
        if review_Queryset.exists():
            raise ValidationError("Ya tienes una review de esta pelicula")

        #Mecanismo de raiting y avgraiting
        if movie.number_rating==0:
            movie.avg_rating=serializer.validated_data['rating']
        else:
            movie.avg_rating=(movie.avg_rating + serializer.validated_data['rating'])/2

        movie.number_rating=movie.number_rating + 1
        movie.save()         
        serializer.save(watchlist=movie,review_user=review_user) 



class ReviewList(generics.ListAPIView):
    #queryset=Review.objects.all()
    permission_classes=[IsAuthenticated]
    serializer_class=ReviewsSerializer
    #Filtrado Bcakends
    filter_backends=[DjangoFilterBackend]
    filterset_fields=['review_user__username','active','watchlist']
    def get_queryset(self):
        pk=self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)




class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Review.objects.all()
    serializer_class=ReviewsSerializer






"""
class ReviewsAV(APIView):
    def get(self,request):
        reviews=Review.objects.all()
        serializer_data=ReviewsSerializer(reviews)
        return Response(serializer_data.data)

    def post(self,request):
        serializer=ReviewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
"""
"""class ReviewList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewsSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
"""
class ReviewDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Review.objects.all()
    serializer_class =ReviewsSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)        

class StreamPlataformAV(APIView):
    def get(self,request):
        streams_plataforms=StreamPlataform.objects.all()
        serializer_data=StreamPlatafotmSerializer(streams_plataforms,many=True)
        return Response(serializer_data.data)
    def post(self,request):
        serializer=StreamPlatafotmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)      


#Alternativa con ViewSets Y Router en urls.py 

class StreamPlataformVS(viewsets.ViewSet):
    def list(self,request):
        queryset=StreamPlataform.objects.all()
        serializer=StreamPlatafotmSerializer(queryset,many=True)
        return Response(serializer.data)
    def retrieve(self,request,pk=None):
        queyset=StreamPlataform.objects.all()
        watchlist=get_object_or_404(queyset,pk=pk)
        serializer=StreamPlatafotmSerializer(watchlist)
        return Response(serializer.data)

#Alternativa con empaquetado de todas las peticiones ModelViewSet

class SreamPlataformMVS(viewsets.ModelViewSet):
    queryset=StreamPlataform.objects.all()
    serializer_class=StreamPlatafotmSerializer

class StreamPlataformDetailsAV(APIView):

    def get(self,request,pk):
        try:
            plataform=StreamPlataform.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer_data=StreamPlatafotmSerializer(plataform)
        return Response(serializer_data.data)

    def put(self,request,pk):
        plataform=StreamPlataform.objects.get(pk=pk)

        serializer_data=StreamPlatafotmSerializer(data=request.data)

        if serializer_data.is_valid():
            serializer_data.save()
            return Response(serializer_data.data)
        else:
            return Response(serializer_data.errors)
    def delete(self,request,pk):
        plataform=StreamPlataform.get(pk=pk)
        plataform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)        


class WatchListAV(APIView):

    def get(self,request):
        watch_list=WatchList.objects.all()
        serializer_data=WatchListSerializer(watch_list,many=True)
        return Response(serializer_data.data)

    def post(self,request):
        serializer_data=WatchListSerializer(data=request.data)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(serializer_data.data)    
        else:
            return Response(serializer_data.errors)

class WatchListDetalisAV(APIView):

    def get(self,request,pk):
        try:
            watch_list=WatchList.objects.get(pk=pk)
        except:
            return Response({'message':'not found'},status=status.HTTP_404_NOT_FOUND)

        serializer_data=WatchListSerializer(watch_list)
        return Response(serializer_data.data)

    def put(self,request,pk):
        movie=WatchList.objects.get(pk=pk)
        serializer_data=WatchListSerializer(movie,data=request.data)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(serializer_data.data)
        else:
            return Response(serializer_data.errors,status=status.HTTP_400_BAD_REQUEST)      

    def delete(self,request,pk):
        movie=WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
@api_view(['GET','POST'])
def movies_list(request):
    if request.method=='GET':
     movies=Movie.objects.all()
     Serializer_data=MovieSerializer(movies,many=True)
     return Response(Serializer_data.data)
    if request.method=='POST':
        serializer=MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)     


@api_view(['GET','PUT','DELETE'])
def movie_details(request,pk):
    if request.method=='GET':
        try:
            movie=Movie.objects.get(pk=pk)
        except:
            return Response({'message':"movie not found"},status=status.HTTP_404_NOT_FOUND)    
        Serializer_data=MovieSerializer(movie)
        return Response(Serializer_data.data)
    if request.method=='PUT':
        movie=Movie.objects.get(pk=pk)
        serializer=MovieSerializer(movie,data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)    
    if request.method=='DELETE':
        movie=Movie.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 

        """