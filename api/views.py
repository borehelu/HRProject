from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .models import Departments, Employees, EmergencyContact, Skills, EmployeeSkills, LeaveRequests, LeaveTypes, \
    LeaveBalances
from .serializers import DepartmentSerializer, EmployeeSerializer, SkillSerializer, EmployeeSkillSerializer, \
    EmergencyContactSerializer, LeaveRequestSerializer, LeaveBalanceSerializer, LeaveTypeSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from .tokens import create_jwt_pair_for_user
from .permissions import AdminOrReadOnly


# handle employees
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def employees_list(request):
    if request.method == 'GET':
        employees = Employees.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {"message": "Employee Created Successfully", "data": serializer.data}
            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    user = authenticate(email=email, password=password)

    if user is not None:
        tokens = create_jwt_pair_for_user(user)
        response = {"message": "Login Successful", "tokens": tokens}
        return Response(data=response, status=status.HTTP_200_OK)
    else:
        return Response(data={"message": "Invalid email or password"})


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def employee_detail(request, employee_id):
    try:
        employee = Employees.objects.get(pk=employee_id)
    except Employees.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "GET":
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_302_FOUND)
    elif request.method == 'DELETE':
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, AdminOrReadOnly])
def leave_type_list(request):
    if request.method == 'GET':
        leave_types = LeaveTypes.objects.all()
        serializer = LeaveTypeSerializer(leave_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = LeaveTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, AdminOrReadOnly])
def leave_type_detail(request, leave_type_id):
    try:
        leave_type = LeaveTypes.objects.get(pk=leave_type_id)
    except LeaveTypes.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = LeaveTypeSerializer(leave_type, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "GET":
        serializer = LeaveTypeSerializer(leave_type)
        return Response(serializer.data, status=status.HTTP_302_FOUND)
    elif request.method == 'DELETE':
        leave_type.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def leave_balance_list(request):
    if request.method == 'GET':
        leave_balances = LeaveBalances.objects.all()
        serializer = LeaveTypeSerializer(leave_balances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = LeaveBalanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AdminOrReadOnly])
def leave_balance_detail(request, leave_balance_id):
    try:
        leave_balance = LeaveBalances.objects.get(pk=leave_balance_id)
    except LeaveBalances.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = LeaveBalanceSerializer(leave_balance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "GET":
        serializer = LeaveBalanceSerializer(leave_balance)
        return Response(serializer.data, status=status.HTTP_302_FOUND)
    elif request.method == 'DELETE':
        leave_balance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def leave_request_list(request):
    if request.method == 'GET':
        leave_requests = LeaveRequests.objects.all()
        serializer = LeaveRequestSerializer(leave_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = LeaveRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def leave_request_detail(request, leave_request_id):
    try:
        leave_request = LeaveRequests.objects.get(pk=leave_request_id)
    except LeaveRequests.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = LeaveRequestSerializer(leave_request, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "GET":
        serializer = LeaveRequestSerializer(leave_request)
        return Response(serializer.data, status=status.HTTP_302_FOUND)
    elif request.method == 'DELETE':
        leave_request.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employee_leave_balances_list(request, employee_id):
    try:
        employee_leave_balances = LeaveBalances.objects.get(employee=employee_id)
        serializer = LeaveBalanceSerializer(employee_leave_balances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except LeaveBalances.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)




@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def employee_leave_requests_list(request, employee_id):
    if request.method == 'GET':
        leave_requests = LeaveRequests.objects.get(employee=employee_id)
        serializer = LeaveRequestSerializer(leave_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = LeaveRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def employee_leave_request_detail(request, employee_id, leave_request_id):
    try:
        leave_request = LeaveRequests.objects.get(pk=leave_request_id,employee=employee_id)
    except LeaveRequests.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = LeaveRequestSerializer(leave_request, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "GET":
        serializer = LeaveRequestSerializer(leave_request)
        return Response(serializer.data, status=status.HTTP_302_FOUND)
    elif request.method == 'DELETE':
        leave_request.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
