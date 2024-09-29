from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('game/<int:game_id>/', views.load_game, name='load_game'),
    path('game/<int:game_id>/move/', views.make_move, name='make_move'),
    path('game/<int:game_id>/lock_top_row/', views.lock_top_row, name='lock_top_row'),
    path('games/<int:game_id>/connect_all/', views.connect_all, name='connect_all'),
]
