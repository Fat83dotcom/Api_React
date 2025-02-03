
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from api.models import Customer, Product, ProductCategory
from api.models import OrderItems, Order
from rest_framework import status
from django.db.models import Q, F

message = {
    'get': {
        'sucess': 'Consulta realizada com Sucesso.',
        'error': 'Faltam paramentros de consulta ou parametro incorreto.',
        'not_found': 'Não encontrado.',
    },
    'post': {
        'sucess': 'Item Registrado com Sucesso.',
        'error': 'Não foi possivel registrar os dados.',
        'stock_error': 'Estoque insuficiente.',
        'order_error': 'Não autorizado, cliente já possui pedido em aberto.'
    },
    'delete': {
        'sucess': 'Item excluído com sucesso.',
        'error': 'Não Foi possível excluir os dados.',
        'order_error': 'O pedido está fechado, não é permitido excluir.'
    }
}


class CustomerGetView(APIView):
    def get(self, request):
        query = Customer.objects.all()
        serializer = CustomerSerializer(
            instance=query,
            many=True
        )
        return Response(
            {'msg': message['get']['sucess'], 'data': serializer.data},
            status=status.HTTP_200_OK
        )


class CustomerGetSearchView(APIView):
    def get(self, request):
        search_name: str = request.query_params.get('search_name', None)
        if not search_name:
            return Response(
                {"error": "O parametro search_name é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if search_name.isnumeric():
            item = Customer.objects.filter(
                Q(id__icontains=search_name)
            )

            if not item.exists():
                return Response(
                    {'data': [], 'msg': message['get']['not_found']},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = CustomerSearchSerializer(
                instance=item,
                many=True
            )

            return Response(
                {'msg': message['get']['sucess'], 'data': serializer.data},
                status=status.HTTP_200_OK
            )

        part: list = search_name.split()

        if len(part) == 2:

            first_name, second_name = part

            item = Customer.objects.filter(
                Q(name__icontains=first_name),
                Q(second_name__icontains=second_name)
            )

            if not item.exists():
                return Response(
                    {'data': [], 'msg': message['get']['not_found']},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = CustomerSearchSerializer(
                instance=item,
                many=True
            )

            return Response(
                {'msg': message['get']['sucess'], 'data': serializer.data},
                status=status.HTTP_200_OK
            )

        item = Customer.objects.filter(
            Q(name__icontains=search_name)
        )

        if not item.exists():
            return Response(
                {'data': [], 'msg': message['get']['not_found']},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CustomerSearchSerializer(
            instance=item,
            many=True
        )

        return Response(
            {'msg': message['get']['sucess'], 'data': serializer.data},
            status=status.HTTP_200_OK
        )


class ProductGetView(APIView):
    def get(self, request):
        query = Product.objects.all()[:10]
        serializer = ProductSerializer(
            instance=query,
            many=True
        )
        return Response(
            {'msg': message['get']['sucess'], 'data': serializer.data},
            status=status.HTTP_200_OK
        )


class CategoryGetView(APIView):
    def get(self, request):
        query = ProductCategory.objects.all()
        if query.exists():
            serializer = ProductCategorySerializer(
                instance=query,
                many=True
            )
            return Response(
                {'msg': message['get']['sucess'], 'data': serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(
            {'msg': message['get']['error']}, status=status.HTTP_404_NOT_FOUND
        )


class CustomerPostView(APIView):
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'msg': message['post']['sucess'], 'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'msg': message['post']['error']},
            status=status.HTTP_400_BAD_REQUEST
        )


class ProductCategoryPostView(APIView):
    def post(self, request):
        serializer = CreateProductCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'msg': message['post']['sucess'], 'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'msg': message['post']['error']},
            status=status.HTTP_400_BAD_REQUEST
        )


class ProductPostView(APIView):
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'msg': message['post']['sucess'], 'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'msg': message['post']['error']},
            status=status.HTTP_400_BAD_REQUEST
        )


class SearchProductByName(APIView):
    def get(self, request):
        search_product_name = request.query_params.get('search_name', None)

        if search_product_name is not None:
            query = Product.objects.filter(name__icontains=search_product_name)
            if query.exists():
                serializer = ProductSerializer(
                    instance=query,
                    many=True
                )
                return Response(
                    {
                        'msg': message['get']['sucess'],
                        'data': serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                {'msg': message['get']['not_found']},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {'msg': message['get']['error']},
            status=status.HTTP_400_BAD_REQUEST
        )


class SearchProductByCategory(APIView):
    def get(self, request):
        search_category = request.query_params.get('search_category', None)

        if search_category.isnumeric() and search_category is not None:
            query = Product.objects.filter(category__id=search_category)
            if query.exists():
                serializer = ProductSerializer(
                    instance=query,
                    many=True
                )
                return Response({
                        'msg': message['get']['sucess'],
                        'data': serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                {'msg': message['get']['not_found']},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {'msg': message['get']['error']},
            status=status.HTTP_400_BAD_REQUEST
        )


class CreateOrder(APIView):
    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        customer_id = request.data['id_customer']
        if OrderValidator.check_order_open_to_customer(customer_id):
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            return Response(
                {'msg': message['post']['sucess'], 'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'data': [], 'msg': message['post']['order_error']},
            status=status.HTTP_401_UNAUTHORIZED
        )


class SearchProductsByOrder(APIView):
    def get(self, request):
        search_params = request.query_params.get('products_by_order')
        if search_params is not None:
            query = OrderItems.objects.filter(
                id_order=search_params
            ).select_related('id_product').values(
                'id',
                'id_order__id',
                'id_product__id',
                'id_product__name',
                'id_product__price',
                'quantity'
            )

            if query.exists():
                data: list = []
                for item in query:
                    item_data = {
                        'id_order_items': item['id'],
                        'id_order': item['id_order__id'],
                        'id_product': item['id_product__id'],
                        'product_name': item['id_product__name'],
                        'price': item['id_product__price'],
                        'quantity': item['quantity']
                    }
                    serializer = ItemsByOrderSerializer(
                        data=item_data
                    )
                    serializer.is_valid(raise_exception=True)
                    data.append(serializer.data)
                return Response(
                    {
                        'msg': message['get']['sucess'],
                        'data': data
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                {'msg': message['get']['not_found']},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {'msg': message['get']['error']},
            status=status.HTTP_400_BAD_REQUEST
        )


class AppendItemsToOrder(APIView):
    def post(self, request):
        if CheckStock.check(
            request.data['quantity'], request.data['id_product']
        ):
            # se ok entao gravar o item senão retornar um erro de estoque
            AddItemToOrder.add(request.data)

            # alterar o valor do pedido
            SumOrder.add_up(
                request.data['id_order'], request.data['id_product']
            )

            # alterar a quantidade de produto
            SubtractStockFromProduct.sub(
                request.data['id_product'], request.data['quantity']
            )

            return Response(
                {'msg': message['post']['sucess']},
                status=status.HTTP_200_OK
            )
        return Response(
            {'data': [], 'msg': message['post']['stock_error']},
            status=status.HTTP_400_BAD_REQUEST
        )


class SearchOrderCustomerIdGetView(APIView):
    def get(self, request):
        search_order = request.query_params.get('search_order', None)

        if not search_order:
            return Response(
                {'data': [], 'msg': message['get']['error']},
                status=status.HTTP_400_BAD_REQUEST
            )

        if search_order.isnumeric():
            query = Order.objects.filter(id_customer=search_order).last()
            serializer = OrderSerializer(instance=query)

            return Response(
                {'msg': message['get']['sucess'], 'data': serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(
            {'data': [], 'msg': message['get']['error']},
            status=status.HTTP_400_BAD_REQUEST
        )


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'name',
            'second_name',
            'email',
            'phone',
            'address',
        ]

    def create(self, validated_data):
        return Customer.objects.create(**validated_data)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'price',
            'quantity',
            'category'
        ]

    def create(self, validated_data):
        return Product.objects.create(**validated_data)


class CustomerSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'second_name']


class CreateProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['category_name']

    def create(self, validated_data):
        return ProductCategory.objects.create(**validated_data)


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'category_name']

    def create(self, validated_data):
        return ProductCategory.objects.create(**validated_data)


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id_customer', 'total']

    def create(self, validated_data):
        return Order.objects.create(**validated_data)


class OrderValidator():

    @classmethod
    def check_order_open_to_customer(cls, customer_id) -> bool:
        orders = Order.objects.all().filter(id_customer_id=customer_id)
        check_order_status: list = [
            order.order_status for order in orders
        ]
        if True in check_order_status:
            return False
        return True


class OrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(
        source='id_customer.name', read_only=True
    )
    customer_second_name = serializers.CharField(
        source='id_customer.second_name', read_only=True
    )

    class Meta:
        model = Order
        fields = [
            'customer_name',
            'customer_second_name',
            'pk',
            'date',
            'total',
            'order_status'
        ]


class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ['id_order', 'id_product', 'quantity']

    def create(self, validated_data):
        return OrderItems.objects.create(**validated_data)


class ItemsByOrderSerializer(serializers.Serializer):
    id_order = serializers.IntegerField()
    id_product = serializers.IntegerField()
    product_name = serializers.CharField(max_length=128)
    price = serializers.FloatField()
    quantity = serializers.IntegerField()


# Controlers


class CheckStock:

    @classmethod
    def check(cls, quantity, id):
        if quantity is not None:
            product = Product.objects.filter(pk=id).first()
            return True if (product.quantity - quantity) > 0 else False


class AddItemToOrder:

    @classmethod
    def add(cls, req: dict):
        serializer = OrderItemsSerializer(data=req)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        return {'error': 'Verifique os dados.'}


class SumOrder:

    @classmethod
    def add_up(cls, id_order, id_product):
        price = Product.objects.filter(id=id_product).values('price').first()
        print(price)
        total_order = Order.objects.filter(
            id=id_order
        ).update(total=F('total') + price['price'])
        return total_order
