# library_app/serializers.py
from rest_framework import serializers
from .models import *


class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = 
        fields = ['id', 'title', 'author', 'year_published', 'kind']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = 
        fields = ['id', 'name', 'city', 'age', 'phone_number']

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = 
        fields = ['cust_id', 'book_id', 'loan_date', 'return_date', 'phone_number']
