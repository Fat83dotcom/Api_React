
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
        'error': 'Não foi possivel registrar os dados.'
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
                    {"msg": "Nenhum item foi encontrado"},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = CustomerSearchSerializer(
                instance=item,
                many=True
            )

            return Response(serializer.data, status=status.HTTP_200_OK)

        part: list = search_name.split()

        if len(part) == 2:

            first_name, second_name = part

            item = Customer.objects.filter(
                Q(name__icontains=first_name),
                Q(second_name__icontains=second_name)
            )

            if not item.exists():
                return Response(
                    {"msg": "Nenhum item foi encontrado"},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = CustomerSearchSerializer(
                instance=item,
                many=True
            )

            return Response(serializer.data, status=status.HTTP_200_OK)

        item = Customer.objects.filter(
            Q(name__icontains=search_name)
        )

        if not item.exists():
            return Response(
                {"msg": "Nenhum item foi encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CustomerSearchSerializer(
            instance=item,
            many=True
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


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
                status=status.HTTP_400_BAD_REQUES
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
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class AppendItemsToOrder(APIView):
    def post(self, request):
        print(request.data)
        req = request.data
        if CheckStock.check(req['quantity'], req['id_product']):
            # se ok entao gravar o item senão retornar um erro de estoque
            response = AddItemToOrder.add(request.data)
            print(response)
            SumOrder.add_up(req['id_order'], req['id_product'])
            # alterar o valor do pedido
            # alterar a quantidade de produto

            return Response({'msg': 'ok'}, status=status.HTTP_200_OK)
        return Response(
            {'msg': 'Estoque insuficiente.'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class SearchOrderCustomerIdGetView(APIView):
    def get(self, request):
        search_order = request.query_params.get('search_order', None)

        if not search_order:
            error = {'error': 'Falta parametro de consulta.'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        if search_order.isnumeric():
            query = Order.objects.filter(id_customer=search_order).last()
            serializer = OrderSerializer(instance=query)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


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
        total_order = Order.objects.filter()
        pass
