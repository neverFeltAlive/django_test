from django.urls import path

from . import views

app_name = 'poll'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),                          # https://sitename/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),               # https://sitename/question_id/
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),     # https://sitename/question_id/results/
    path('<int:question_id>/vote/', views.vote, name='vote'),                   # https://sitename/question_id/vote/
]
