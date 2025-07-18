from django.urls import path
from .views import GetIkshanaModelData

app_name = 'explain_db'

urlpatterns = [
    path('<str:model_name>/', GetIkshanaModelData.as_view(), name='get_model_data'),
] 