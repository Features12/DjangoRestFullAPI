from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status, generics, reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .permissions import IsOwnerOrReadOnly
from .models import Game, PlayerScore, Player, GameCategory
from django.contrib.auth.models import User
from .api.serializers import (GameSerializer, ScoreSerializer, GameCategorySerializer, PlayerSerializer,
                              PlayerScoreSerializer, UserSerializer)
from rest_framework import permissions
from rest_framework.throttling import ScopedRateThrottle
from rest_framework import filters
from django_filters import NumberFilter, DateTimeFilter, AllValuesFilter



# class JSONResponse(HttpResponse):
#     def __init__(self, data, **kwargs):
#         content = JSONRenderer().render(data)
#         kwargs['content_type'] = 'application/json'
#         super().__init__(content, **kwargs)
#
#
# @csrf_exempt
# def game_list(request):
#     if request.method == 'GET':
#         games = Game.objects.all()
#         games_serializer = GameSerializer(games, many=True)
#         return JSONResponse(games_serializer.data)
#
#     elif request.method == 'POST':
#         game_data = JSONParser().parse(request)
#         games_serializer = GameSerializer(data=game_data)
#         if games_serializer.is_valid():
#             games_serializer.save()
#             return JSONResponse(games_serializer.data, status=status.HTTP_201_CREATED)
#         return JSONResponse(games_serializer.data, status=status.HTTP_400_BAD_REQUEST)
#
#
# @csrf_exempt
# def game_detail(request, pk):
#     try:
#         game = Game.objects.get(pk=pk)
#     except Game.DoesNotExist:
#         return HttpResponse(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         game_serializer = GameSerializer(game)
#         return JSONResponse(game_serializer.data)
#
#     elif request.method == 'PUT':
#         game_data = JSONParser().parse(request)
#         game_serializer = GameSerializer(data=game_data)
#         if game_serializer.is_valid():
#             game_serializer.save()
#             return JSONResponse(game_serializer.data)
#         return JSONResponse(game_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         game.delete()
#         return HttpResponse(status=status.HTTP_204_NO_CONTENT)
#
#
# @api_view(['GET', 'POST'])
# def game_list(request):
#     if request.method == 'GET':
#         games = Game.objects.all()
#         games_serializer = GameSerializer(games, many=True)
#         return Response(games_serializer.data)
#
#     elif request.method == 'POST':
#         games_serializer = GameSerializer(data=request.data)
#         if games_serializer.is_valid():
#             games_serializer.save()
#             return Response(games_serializer.data, status=status.HTTP_201_CREATED)
#         return Response(games_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-list'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    )
    filter_fields = ('name', 'game_category', 'release_date', 'played', 'owner')
    search_fileds = ('^name',)
    ordering_fields = ('name', 'release_date')

    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)



class GameCategoryList(generics.ListCreateAPIView):
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    name = 'gamecategory-list'
    throttle_scope = 'game-categories'
    throttle_classes = (ScopedRateThrottle, )
    filter_fields = ('name', )
    search_fileds = ('^name', )
    ordering_fields = ('name', )



class PlayerList(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    name = 'player-list'
    filter_fields = ('name', 'gender')
    search_fileds = ('^name',)
    ordering_fields = ('name',)



class PlayerScoreList(generics.ListCreateAPIView):
    queryset = PlayerScore.objects.all()
    serializer_class = PlayerScoreSerializer
    name = 'playerscore-list'
    filter_class = PlayerScoreFilter
    ordering_fields = (
        'score',
        'score_date',
    )


class PlayerScoreFilter(filters.FilterSet):
    min_score = NumberFilter(name='score', lookup_expr='gte')
    msx_score = NumberFilter(name='score', lookup_expr='lte')
    from_score_date = DateTimeFilter(name='score_date', lookup_expr='gte')
    to_score_Date = DateTimeFilter(name='score_date', lookup_expr='lte')
    player_name = AllValuesFilter(name='player__name')
    game_name = AllValuesFilter(name='game__name')

    class Meta:
        model = PlayerScore
        fields = (
            'score',
            'from_score_date',
            'to_score_date',
            'min_score',
            'max_score',
            'player_name',
            'game_name',
        )


class GameCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    name = 'gamecategory-detail'
    throttle_scope = 'game-categories'
    throttle_classes = (ScopedRateThrottle,)


class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-detail'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    )


class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    name = 'player-detail'


class PlayerScoreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlayerScore.objects.all()
    serializer_class = PlayerScoreSerializer
    name = 'playerscore-detail'


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({
            'players': reverse(PlayerList.name, request=request),
            'game-categories': reverse(GameCategoryList.name, request=request),
            'games': reverse(GameList.name, request=request),
            'scores':reverse(PlayerScoreList.name, request=request),
            'users': reverse(UserList.name, request=request),
        })


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-list'


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'




