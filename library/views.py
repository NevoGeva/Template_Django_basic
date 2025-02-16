from asyncio import Task
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes
from rest_framework import viewsets
from .models import Books
from .serializers import BooksSerializer
from rest_framework.permissions import IsAuthenticated
from .serializers import BooksSerializer
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Customer
from .serializers import CustomerSerializer
from .models import Loan
from .serializers import LoanSerializer

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def index(req):
    return Response('Hello')



@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def order_books(request):
   if request.method == 'POST':
       serializer = BooksSerializer(data=request.data)
   if serializer.is_valid():
       serializer.save(user=request.user)
       return Response(serializer.data, status=status.HTTP_201_CREATED)
   return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getImages(request):
    res=[] #create an empty list
    for img in Task.objects.all(): #run on every row in the table...
        res.append({"title":img.title,
                "description":img.description,
                "completed":False,
               "image":str( img.image)
                }) #append row by to row to res list
    return Response(res) #return array as json response


# upload image method (with serialize)
class APIViews(APIView):
    parser_class=(MultiPartParser,FormParser)
    def post(self,request,*args,**kwargs):
        api_serializer=BooksSerializer(data=request.data)
        if api_serializer.is_valid():
            api_serializer.save()
            return Response(api_serializer.data,status=status.HTTP_201_CREATED)
        else:
            print('error',api_serializer.errors)
            return Response(api_serializer.errors,status=status.HTTP_400_BAD_REQUEST)






@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def loans(req):
    return Response('about loans')
          
# login
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom columns


        token['username'] = user.username
        # ...
        return token
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# register
@api_view(['POST'])
def register(request):
    user = User.objects.create_user(
                username=request.data['username'],
                email=request.data['email'],
                password=request.data['password']
            )
    user.is_active = True
    user.is_staff = True
    user.save()
    return Response("new user born")
# crud for books
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_books(req):
    user = req.user
    books = Books.objects.all()  
    serializer = BooksSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_book(request):
    serializer = BooksSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def retrieve_book(request, pk):
    try:
        book = Books.objects.get(pk=pk, user=request.user)
    except Books.DoesNotExist:
        return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = BooksSerializer(book)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_book(request, pk):
    try:
        book = Books.objects.get(pk=pk, user=request.user)
    except Books.DoesNotExist:
        return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = BooksSerializer(book, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_book(request, pk):
    try:
        book = Books.objects.get(pk=pk, user=request.user)
    except Books.DoesNotExist:
        return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

    book.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# crud for customer:
# GET all customers (READ)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_customers(request):
    customers = Customer.objects.filter(user=request.user)  # Get customers for the authenticated user
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)

# POST to create a customer (CREATE)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_customer(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)  # Save with user relationship
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# GET a specific customer by ID (READ)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def retrieve_customer(request, pk):
    try:
        customer = Customer.objects.get(pk=pk, user=request.user)
    except Customer.DoesNotExist:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CustomerSerializer(customer)
    return Response(serializer.data)

# PUT to update a customer (UPDATE)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_customer(request, pk):
    try:
        customer = Customer.objects.get(pk=pk, user=request.user)
    except Customer.DoesNotExist:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CustomerSerializer(customer, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# DELETE a specific customer (DELETE)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_customer(request, pk):
    try:
        customer = Customer.objects.get(pk=pk, user=request.user)
    except Customer.DoesNotExist:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

    customer.delete()
    return Response({'message': 'Customer deleted successfully'}, status=status.HTTP_204_NO_CONTENT)



#crud for loans
# GET all loans (READ)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_loans(request):
    loans = Loan.objects.filter(user=request.user)  # Fetch loans for the authenticated user
    serializer = LoanSerializer(loans, many=True)
    return Response(serializer.data)

# POST to create a loan (CREATE)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_loan(request):
    serializer = LoanSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)  # Save with the authenticated user
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# GET a specific loan by ID (READ)         
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_loan_by_id(request, pk):
    try:
        loan = Loan.objects.get( pk=pk, user=request.user)
    except Loan.DoesNotExist:
        return Response({'error': 'Loan not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = LoanSerializer(loan)
    return Response(serializer.data)


# PUT to update a loan (UPDATE)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_loan(request, pk):
    try:
        loan = Loan.objects.get(pk=pk, user=request.user)
    except Loan.DoesNotExist:
        return Response({'error': 'Loan not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = LoanSerializer(loan, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# DELETE a specific loan (DELETE)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_loan(request, pk):
    try:
        loan = Loan.objects.get(pk=pk, user=request.user)
    except Loan.DoesNotExist:
        return Response({'error': 'Loan not found'}, status=status.HTTP_404_NOT_FOUND)

    loan.delete()
    return Response({'message': 'Loan deleted successfully'}, status=status.HTTP_204_NO_CONTENT)




## make the changes with the models name if you have and put inside the object.get