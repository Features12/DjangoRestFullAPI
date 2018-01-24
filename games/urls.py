from django.conf.urls import url
from .import views

urlpatterns = [
    url(r'^games-categories/$',
        views.GameCategoryList.as_view(),
        name=views.GameCategoryList.name),
    url(r'^games-categories/(?P<pk>[0-9]+)/$',
        views.GameCategoryDetail.as_view(),
        name=views.GameCategoryDetail.name),
    url(r'^games/$',
        views.GameList.as_view(),
        name=views.GameList.name),
    url(r'^games/(?P<pk>[0-9]+)/$',
        views.GameDetail.as_view(),
        name=views.GameDetail.name),
    url(r'^players/$',
        views.PlayerList.as_view(),
        name=views.PlayerList.name),
    url(r'^player/(?P<pk>[0-9]+)/$',
        views.PlayerDetail.as_view(),
        name=views.PlayerDetail.name),
    url(r'^player-scores/$',
        views.PlayerScoreList.as_view(),
        name=views.PlayerScoreList.name),
    url(r'^player-scores/(?P<pk>[0-9]+)/$',
        views.PlayerScoreDetail.as_view(),
        name=views.PlayerScoreDetail.name),
    url(r'^$',
        views.ApiRoot.as_view(),
        name=views.ApiRoot.name)
    # url(r'^games/(?P<pk>[0-9]+)/$', game_detail),
]