from django.urls import path
from api.views import CustomerGetView, CustomerPostView, ProductPostView, CustomerGetSearchView
from api.views import CategoryGetView, ProductCategoryPostView, CreateOrder, SearchOrderCustomerIdGetView
from api.views import ProductGetView, SearchProductByCategory, SearchProductByName

urlpatterns = [
    path('get_products/', ProductGetView.as_view(), name='product_g'),
    path('get_customers/', CustomerGetView.as_view(), name='customers_g'),
    path('register_customers/', CustomerPostView.as_view(), name='customers_p'),
    path('register_product/', ProductPostView.as_view(), name='customers_p'),
    path(
        'search_customer/',
        CustomerGetSearchView.as_view(),
        name='search_customer_g'
    ),
    path(
        'search_product_category/',
        CategoryGetView.as_view(),
        name='search_product_category'
    ),
    path(
        'register_product_category/',
        ProductCategoryPostView.as_view(),
        name='register_product_category'
    ),
    path('create_order/', CreateOrder.as_view(), name='crete_order_p'),
    path(
        'search_order/',
        SearchOrderCustomerIdGetView.as_view(),
        name='ssearch_order_g'
    ),
    path(
        'search_product_by_category/',
        SearchProductByCategory.as_view(),
        name='search_p_category'
    ),
    path(
        'search_product_by_name/',
        SearchProductByName.as_view(),
        name='search_p_name'
    ),
]
