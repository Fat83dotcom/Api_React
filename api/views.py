
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from api.models import Customer
from rest_framework import status


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'name',
            'email',
            'phone',
            'address',
        ]
    
    def create(self, validated_data):
        return Customer.objects.create(**validated_data)


class CustomerGetView(APIView):
    def get(self, request):
        query = Customer.objects.all()
        serializer = CustomerSerializer(
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