from rest_framework.serializers import ModelSerializer
from .models import Employees, Departments, Skills, EmployeeSkills, EmergencyContact, LeaveTypes, LeaveBalances, \
    LeaveRequests


class EmployeeSerializer(ModelSerializer):
    class Meta:
        model = Employees
        fields = '__all__'


class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = Departments
        fields = '__all__'


class EmergencyContactSerializer(ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = '__all__'


class SkillSerializer(ModelSerializer):
    class Meta:
        model = Skills
        fields = '__all__'


class EmployeeSkillSerializer(ModelSerializer):
    class Meta:
        model = EmployeeSkills
        fields = '__all__'


class LeaveTypeSerializer(ModelSerializer):
    class Meta:
        model = LeaveTypes
        fields = '__all__'


class LeaveBalanceSerializer(ModelSerializer):
    class Meta:
        model = LeaveBalances
        fields = '__all__'


class LeaveRequestSerializer(ModelSerializer):
    class Meta:
        model = LeaveRequests
        fields = '__all__'
