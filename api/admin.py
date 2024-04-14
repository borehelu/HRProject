from django.contrib import admin
from .models import Departments, Employees, EmergencyContact, Skills, EmployeeSkills, LeaveRequests, LeaveTypes, LeaveBalances

# Register your models here.
admin.site.register(Employees)
admin.site.register(Departments)
admin.site.register(EmergencyContact)
admin.site.register(Skills)
admin.site.register(EmployeeSkills)
admin.site.register(LeaveTypes)
admin.site.register(LeaveRequests)
admin.site.register(LeaveBalances)