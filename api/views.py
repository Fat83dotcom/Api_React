
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from api.models import Customer, Product, ProductCategory
from rest_framework import status
from django.db.models import Q




class CustomerGetView(APIView):
    def get(self, request):
        query = Customer.objects.all()
        serializer = CustomerSerializer(
            instance=query,
            many=True
        )
        return Response(serializer.data)


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
                Q(name__icontains=first_name) , Q(second_name__icontains=second_name)
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
        query = Product.objects.all()
        serializer = ProductSerializer(
            instance=query,
            many=True
        )
        return Response(serializer.data)


class CustomerPostView(APIView):
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductCategoryPostView(APIView):
    pass


class ProductPostView(APIView):
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['category_name']
    
    def create(self, validated_data):
        return ProductCategory.objects.create(**validated_data)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name',
            'price',
            'quantity'
        ]

    def create(self, validated_data):
        return Product.objects.create(**validated_data)


class CustomerSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'second_name']