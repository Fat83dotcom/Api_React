from django.urls import path
from api.views import CustomerGetView, CustomerPostView
from api.views import ProductPostView, CustomerGetSearchView
from api.views import CategoryGetView, ProductCategoryPostView
from api.views import CreateOrder, SearchLastOrderCustomerView
from api.views import ProductGetView, SearchProductByCategory
from api.views import SearchProductByName, AppendItemsToOrder
from api.views import SearchProductsByOrder, DeleteItemsFromOrder
from api.views import CloseOrder, AllOrdersFromCustomerView

urlpatterns = [
    path('get_products/', ProductGetView.as_view(), name='product_g'),
    path('get_customers/', CustomerGetView.as_view(), name='customers_g'),
    path(
        'register_customers/', CustomerPostView.as_view(), name='customers_p'
    ),
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
        SearchLastOrderCustomerView.as_view(),
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
    path('append_items/', AppendItemsToOrder.as_view(), name='append_items'),
    path(
        'search_products_by_order/',
        SearchProductsByOrder.as_view(),
        name='products_by_order'
    ),
    path(
        'delete_items/<int:id_item>/<int:id_order>/<int:id_prod>/<int:qtd>/',
        DeleteItemsFromOrder.as_view(),
        name='delete_items'
    ),
    path(
        'close_order/', CloseOrder.as_view(), name='close_order'
    ),
]
