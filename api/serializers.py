from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError as SValidationError
from rest_framework.validators import ValidationError
from .models import Employees, Departments, Skills, EmployeeSkills, EmergencyContact, LeaveTypes, LeaveBalances, \
    LeaveRequests
from django.utils.timezone import now
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta


class EmployeeSerializer(ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = Employees
        fields = ['id', 'first_name', 'last_name', 'password', 'phone', 'email', 'address', 'role', 'date_of_birth',
                  'gender',
                  'department', 'username']

    def validate(self, attrs):
        email_exists = Employees.objects.filter(email=attrs["email"]).exists()

        if email_exists:
            raise ValidationError("Email has already been used")
        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop("password")
        employee = super().create(validated_data)
        employee.set_password(password)
        employee.save()
        return employee


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

    def validate_start_date(self, value):
        if value < now().date():
            raise serializers.ValidationError("Start date cannot be in the past.")
        return value

    def validate_end_date(self, value):
        start_date = parse(self.initial_data.get('start_date')).date()
        if value < start_date:
            raise serializers.ValidationError("End date must be after the start date.")
        return value

    def create(self, validated_data):
        employee = validated_data['employee']
        leave_type = validated_data['leave_type']
        start_date = validated_data['start_date']
        end_date = validated_data['end_date']

        try:
            leave_balance = LeaveBalances.objects.get(employee=employee, leave_type=leave_type)
            if leave_balance.remaining_balance < (relativedelta(end_date, start_date).days):
                raise serializers.ValidationError("Insufficient leave balance.")
        except LeaveBalances.DoesNotExist:
            raise serializers.ValidationError("Leave balance not found for the employee and leave type")

        leave_request = super().create(validated_data)
        leave_request.save()

        return leave_request

    def update(self, instance, validated_data):
        user = self.context['request'].user
        status = validated_data.get('status', instance.status)

        if not user.is_staff and status == 'Approved':
            raise SValidationError("You are not authorized to perform that operation")
        else:
            instance.status = validated_data.get('status', instance.status)
            instance.leave_type = validated_data.get('leave_type', instance.leave_type)
            instance.start_date = validated_data.get('start_date', instance.start_date)
            instance.end_date = validated_data.get('end_date', instance.end_date)
            instance.comments = validated_data.get('comments', instance.comments)
            instance.save()
            return instance
