
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
        'order_error': 'Não autorizado, cliente já possui pedido em aberto.',
        'order_closed_error': 'Pedido fechado, operação não permitida.'
    },
    'delete': {
        'sucess': 'Item excluído com sucesso.',
        'error': 'Não Foi possível excluir os dados.',
        'order_error': 'O pedido está fechado, não é permitido excluir.'
    },
    'patch': {
        'sucess': 'Item modificado com sucesso.',
        'error': 'Não foi possivel modificar o item.'
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
                    {
                        'msg': message['post']['sucess'],
                        'data': serializer.data
                    },
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
        if CheckOrderStatus.check(request.data['id_order']):
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
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(
            {'data': [], 'msg': message['post']['order_closed_error']},
            status=status.HTTP_401_UNAUTHORIZED
        )


class DeleteItemsFromOrder(APIView):
    def delete(self, request, **kwargs):
        try:
            id_item = kwargs.get('id_item')
            id_order = kwargs.get('id_order')
            id_product = kwargs.get('id_prod')
            quantity = kwargs.get('qtd')

            if CheckOrderStatus.check(id_order):
                item_deleted = OrderItems.objects.get(id=id_item)
                item_deleted.delete()

                # Estornar a quantidade de produto
                AddStockToProduct.add(id_product, quantity)

                # Estornar o valor do pedido
                SubtractOrder.sub_up(id_order, id_product)

                return Response(
                    {"data": [], "msg": message['delete']['sucess']},
                    headers={"Content-Type": "application/json"},
                    status=status.HTTP_204_NO_CONTENT
                )
            return Response(
                {"data": [], "msg": message['delete']['order_error']},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception:
            return Response(
                {"data": [], "msg": message['delete']['order_error']},
                status=status.HTTP_400_BAD_REQUEST
            )


class SearchLastOrderCustomerView(APIView):
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


class CloseOrder(APIView):
    def patch(self, request):
        id_order = request.data.get('id')
        print(id_order)
        query = Order.objects.get(id=id_order)
        serializer = OrderPureSerializer(
            query,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'data': serializer.data, 'msg': message['patch']['sucess']},
                status=status.HTTP_200_OK
            )
        return Response(
            {'data': [], 'msg': message['patch']['error']},
            status=status.HTTP_204_NO_CONTENT
        )


class AllOrdersFromCustomerView(APIView):
    def get(self, request):
        id_customer = request.query_params.get('id_customer')
        if isinstance(id_customer, str):
            query = Order.objects.filter(id_customer=id_customer)
            serializer = OrderPureSerializer(
                instance=query,
                many=True
            )

            if query:
                return Response(
                    {'data': serializer.data, 'msg': message['get']['sucess']},
                    status=status.HTTP_200_OK
                )
            return Response(
                {'data': [], 'msg': message['get']['not_found']},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {'data': [], 'msg': message['get']['error']},
            status=status.HTTP_400_BAD_REQUEST
        )


class OrderPureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'date',
            'total',
            'order_status'
        ]


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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['total'] = round(data.get('total'), 2)
        return data


class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ['id_order', 'id_product', 'quantity']

    def create(self, validated_data):
        return OrderItems.objects.create(**validated_data)


class CheckOrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_status']


class ItemsByOrderSerializer(serializers.Serializer):
    id_order_items = serializers.IntegerField()
    id_order = serializers.IntegerField()
    id_product = serializers.IntegerField()
    product_name = serializers.CharField(max_length=128)
    price = serializers.FloatField()
    quantity = serializers.IntegerField()


class SubtractProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'quantity']

# Controlers


class CheckStock:

    @classmethod
    def check(cls, quantity, product_id):
        if quantity is not None:
            product = Product.objects.filter(pk=product_id).first()
            return True if (product.quantity - quantity) >= 0 else False


class AddItemToOrder:

    @classmethod
    def add(cls, request: dict):
        serializer = OrderItemsSerializer(data=request)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        return {'error': 'Verifique os dados.'}


class SumOrder:

    @classmethod
    def add_up(cls, id_order, id_product):
        price = Product.objects.filter(id=id_product).values('price').first()
        total_order = Order.objects.filter(
            id=id_order
        ).update(total=F('total') + price['price'])
        return total_order


class SubtractOrder:

    @classmethod
    def sub_up(cls, id_order, id_product):
        price = Product.objects.filter(id=id_product).values('price').first()
        total_order = Order.objects.filter(
            id=id_order
        ).update(total=F('total') - price['price'])
        return total_order


class SubtractStockFromProduct:

    @classmethod
    def sub(cls, id_product, sub_quantity):
        if sub_quantity is not None:
            result = Product.objects.filter(
                id=id_product
            ).update(quantity=F('quantity') - int(sub_quantity))
            return result


class AddStockToProduct:

    @classmethod
    def add(cls, id_product, add_quantity):
        if add_quantity is not None:
            result = Product.objects.filter(
                id=id_product
            ).update(quantity=F('quantity') + int(add_quantity))
            return result


class CheckOrderStatus:

    @classmethod
    def check(cls, id_order):
        query = Order.objects.filter(id=id_order).first()
        serializer = CheckOrderStatusSerializer(instance=query)
        return serializer.data.get('order_status')
