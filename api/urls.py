from django.urls import path
from api import views

urlpatterns = [
    #path('author', views.AuthorList.as_view()),
    path('upload', views.UploadFile.as_view()),
    path('analytic',views.analysis.as_view()),
    path('summarizer',views.summary.as_view()),
    path('planning',views.Planning.as_view()),
    path('sentiment',views.Sentiment.as_view()),
    path('total',views.total.as_view())
]