from django.urls import path
from api import views

urlpatterns = [
    #path('author', views.AuthorList.as_view()),
    path('upload', views.UploadFile.as_view()),
    path('analytic',views.analysis.as_view())
]