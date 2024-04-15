# Human Resource Management System (HRMS) API

## Introduction

This REST API is designed to provide backend functionality for a Human Resource Management System (HRMS). It is built using Python Django Rest Framework (DRF) and provides endpoints for managing employees, departments, leaves, and other HR-related functionalities.

## Features

- CRUD operations for employees, departments, and roles.
- Authentication and authorization using JWT tokens.
- Pagination and filtering for efficient data retrieval.
- Custom endpoints for specific HR-related tasks.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   
3. Apply database migrations:
      ```bash
   python manage.py migrate
      
4. Create a superuser(for admin access):
      ```bash
   python manage.py createsuperuser
      
5. Start the development server
   ```bash
   python manage.py runserver

## Usage

### Authentication
To access protected endpoints, you need to obtain an access token by sending a POST request to the `/api/v1/login` endpoint with your email and password. Two tokens will be returned - access and refresh tokens - in the response, which you should include in the `Authorization` header of subsequent requests as `Bearer <access-token>`.

### Endpoints

### Auth Endpoints:

POST /api/v1/auth/login: Get token pairs - Access and Refresh token.
POST /api/v1/auth/token/refresh: Obtain new access token after expiry.


### Employee Endpoints:
GET /api/v1/employees/: List all employees.
POST /api/v1/employees/: Create a new employee.
GET /api/v1/employees/<employee-id>/: Retrieve a specific employee.
PUT /api/v1/employees/<employee-id>/: Update a specific employee.
DELETE /api/v1/employees/<employee-id>/: Delete a specific employee.

### Leave Types Endpoints
GET /api/v1/leave-types/: List all leave types.
POST /api/v1/leave-types/: Create a new leave type.
GET /api/v1/leave-types/<leave-type-id>/: Retrieve a specific leave type.
PUT /api/v1/leave-types/<leave-type-id>/: Update a specific leave type.
DELETE /api/v1/leave-types/<leave-type-id>/: Delete a specific leave type.

### Leave Balances Endpoints
GET /api/v1/leave-balances/: List all leave balances.
POST /api/v1/leave-balances Create a new leave balance.
GET /api/v1/leave-balances/<leave-balance-id>/: Retrieve a specific leave balance.
PUT /api/v1/leave-balances/<leave-balance-id>/: Update a specific leave balance.
DELETE /api/v1/leave-balances/<leave-balance-id>/: Delete a specific leave balance.

### Leave Requests Endpoints
GET /api/v1/leave-requests/: List all leave requests.
POST /api/v1/leave-requests Create a new leave request.
GET /api/v1/leave-requests/<leave-request-id>/: Retrieve a specific leave request.
PUT /api/v1/leave-requests/<leave-request-id>/: Update a specific leave request.
DELETE /api/v1/leave-requests/<leave-request-id>/: Delete a specific leave request.

### Sample Requests

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Django Rest Framework: [https://www.django-rest-framework.org/](https://www.django-rest-framework.org/)
- JWT Authentication: [https://github.com/davesque/django-rest-framework-simplejwt](https://github.com/davesque/django-rest-framework-simplejwt)



