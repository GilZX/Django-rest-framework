from django.urls import path,include
from watchlist_app.api.views import WatchListAV,WatchListDetalisAV,StreamPlataformAV,StreamPlataformDetailsAV,ReviewList,ReviewDetail,ReviewCreate,StreamPlataformVS,SreamPlataformMVS,WatchListFilter
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('plataform',SreamPlataformMVS,basename='steamplataform')
urlpatterns = [
    path('list/', WatchListAV.as_view()),
    path('<int:pk>',WatchListDetalisAV.as_view()),
    path('list/filter/',WatchListFilter.as_view()),
    #path('plataform/',StreamPlataformAV.as_view()),
    path('',include(router.urls)),
    path('plataform/<int:pk>',StreamPlataformDetailsAV.as_view()),

    #path('review/',ReviewList.as_view(),name="review-list"),
    #path('review/<int:pk>',ReviewDetail.as_view(),name="review-detail"),

    path('plataform/<int:pk>/review-create',ReviewCreate.as_view(),name='review-create'),
    path('plataform/<int:pk>/review',ReviewList.as_view(),name='review-list'),
    path('plataform/review/<int:pk>',ReviewDetail.as_view(),name='review-detail'),
]