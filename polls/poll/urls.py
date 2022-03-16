from django.urls import path

from . import views

app_name = 'poll'
urlpatterns = [
    path('', views.index, name='index'),                                    # https://sitename/
    path('<int:question_id>/', views.detail, name='detail'),                # https://sitename/question_id/
    path('<int:question_id>/results/', views.results, name='results'),      # https://sitename/question_id/results/
    path('<int:question_id>/vote/', views.vote, name='vote'),               # https://sitename/question_id/vote/
]
