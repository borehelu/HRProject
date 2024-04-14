from django.urls import path
from rest_framework_simplejwt.views import  TokenRefreshView
from .views import employees_list, employee_detail, leave_type_list, leave_type_detail, leave_balance_list, \
    leave_balance_detail, login, leave_request_detail, leave_request_list, employee_leave_request_detail, \
    employee_leave_requests_list, employee_leave_balances_list

urlpatterns = [
    path("auth/login/", login, name="get token"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="refresh token"),
    path("employees", employees_list),
    path("employees/<int:employee_id>", employee_detail),
    path("employees/<int:employee_id>/leave-balances", employee_leave_balances_list),
    path("employees/<int:employee_id>/leave-requests", employee_leave_requests_list),
    path("employees/<int:employee_id>/leave-requests/<int:leave_request_id>", employee_leave_request_detail),
    path("leave-types", leave_type_list),
    path("leave-types/<int:leave_type_id>", leave_type_detail),
    path("leave-balances", leave_balance_list),
    path("leave-balances/<int:leave_balance_id>", leave_balance_detail),
    path("leave-requests", leave_request_list),
    path("leave-requests/<int:leave_request_id>", leave_request_detail)

]
