from django.urls import path

from cards import views

urlpatterns = [
    # Play game
    path('', views.PlayView.as_view(), name='home'),

    # Show all words
    path('cards/', views.CardsView.as_view(), name='cards_display'),

    # Add a new word
    path('add/', views.CardAddView.as_view(), name='cards_add'),

    # Card remembered
    path('cards/<id>/success/',
         views.CardSuccessView.as_view(),
         name='cards_success'),

    # Card forgotten
    path('cards/<id>/failure/',
         views.CardFailureView.as_view(),
         name='cards_failure'),
]
