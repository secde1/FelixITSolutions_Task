from django.urls import path
from .views import DistributeMaterialsView

urlpatterns = [
    path('distribute-materials/', DistributeMaterialsView.as_view(), name='distribute-materials'),
]
