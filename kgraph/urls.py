from django.urls import path
from .views import search, img
app_name = 'kgraph'

urlpatterns = [
    path('search', search),
    # path('predict_image', predict_image),
    # path('predict_data', predict_data),
    path('img', img),
]
