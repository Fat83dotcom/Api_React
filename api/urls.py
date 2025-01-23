from django.urls import path
from api.views import CustomerGetView, CustomerPostView

urlpatterns = [
    path('get_customers/', CustomerGetView.as_view(), name='customers_g'),
    path('post_customers/', CustomerPostView.as_view(), name='customers_p'),
]
