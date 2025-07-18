from django.urls import path
from .views import GetModelData, GetAllModelData

app_name = 'explain_db'

urlpatterns = [
    path('<str:model_name>/', GetModelData.as_view(), name='get_model_data'),
    path('all/', GetAllModelData.as_view(), name='get_all_model_data'),
] 