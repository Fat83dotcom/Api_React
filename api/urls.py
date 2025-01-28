from django.urls import path
from api.views import CustomerGetView, CustomerPostView, ProductPostView, CustomerGetSearchView
from api.views import CategoryGetView, ProductCategoryPostView

urlpatterns = [
    path('get_customers/', CustomerGetView.as_view(), name='customers_g'),
    path('register_customers/', CustomerPostView.as_view(), name='customers_p'),
    path('register_product/', ProductPostView.as_view(), name='customers_p'),
    path('search_customer/', CustomerGetSearchView.as_view(), name='search_customer_g'),
    path('search_product_category/', CategoryGetView.as_view(), name='search_product_category'),
    path(
        'register_product_category/',
        ProductCategoryPostView.as_view(),
        name='register_product_category'
    ),
]
