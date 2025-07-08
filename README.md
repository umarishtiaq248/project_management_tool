# Project Management Tool API

A Django REST API for managing projects, tasks, and team collaboration.

## Features

- User authentication and authorization
- Project management with team members
- Task tracking with priorities and status
- Comments on tasks
- JWT token-based authentication
- Swagger/OpenAPI documentation

## Project Structure

```
project_management_tool/
├── manage.py
├── requirement.txt
├── db.sqlite3
├── .gitignore
├── test_project.py                  # Test script for project functionality
├── project_management_tool/          # Main Django project
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── views.py                      # User authentication views
│   ├── serializers.py               # User serializers
│   └── wsgi.py
├── projects/                        # Project management app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                    # Project and ProjectMember models
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── tests.py
│   └── migrations/
├── task/                           # Task management app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                   # Task model
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── tests.py
│   └── migrations/
└── comments/                       # Comments app
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py                   # Comment model
    ├── views.py
    ├── serializers.py
    ├── urls.py
    ├── tests.py
    └── migrations/
```

## Models

### Project Model
- `name`: CharField (max_length=255)
- `description`: TextField
- `owner`: ForeignKey to User
- `created_at`: DateTimeField

### ProjectMember Model
- `project`: ForeignKey to Project
- `user`: ForeignKey to User
- `role`: CharField (choices: 'Admin', 'Member')

### Task Model
- `title`: CharField (max_length=255)
- `description`: TextField
- `status`: CharField (choices: 'To Do', 'In Progress', 'Done')
- `priority`: CharField (choices: 'Low', 'Medium', 'High')
- `assigned_to`: ForeignKey to User (nullable)
- `project`: ForeignKey to Project
- `created_at`: DateTimeField
- `due_date`: DateTimeField (nullable)

### Comment Model
- `content`: TextField
- `user`: ForeignKey to User
- `task`: ForeignKey to Task
- `created_at`: DateTimeField

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirement.txt
   ```

4. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Testing the Installation

To verify that your installation is working correctly, you can run the included test script:

```bash
python test_project.py
```

This script will test:
- Model creation and relationships
- Serializer validation
- Import functionality
- Basic project functionality

The script should output "All tests passed!" if everything is working correctly.

## API Documentation

Once the server is running, you can access:
- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/
- Admin Panel: http://localhost:8000/admin/

## API Endpoints

### Authentication
- `POST /users/register/` - Register a new user
- `POST /users/login/` - Login user
- `POST /token/refresh/` - Refresh JWT token

### Users
- `GET /users/` - List all users
- `GET /users/{id}/` - Get user details
- `PUT /users/{id}/` - Update user
- `DELETE /users/{id}/` - Delete user

### Projects
- `GET /api/projects/projects/` - List projects
- `POST /api/projects/projects/` - Create project
- `GET /api/projects/projects/{id}/` - Get project details
- `PUT /api/projects/projects/{id}/` - Update project
- `DELETE /api/projects/projects/{id}/` - Delete project
- `POST /api/projects/projects/{id}/add_member/` - Add member to project
- `GET /api/projects/projects/{id}/tasks/` - Get tasks for a specific project

### Tasks
- `GET /api/task/tasks/` - List all tasks
- `POST /api/task/tasks/` - Create task
- `GET /api/task/tasks/{id}/` - Get task details
- `PUT /api/task/tasks/{id}/` - Update task
- `DELETE /api/task/tasks/{id}/` - Delete task
- `GET /api/task/projects/{project_id}/tasks/` - List tasks in specific project
- `POST /api/task/projects/{project_id}/tasks/` - Create task in specific project
- `GET /api/task/tasks/{id}/comments/` - Get comments for a specific task

### Comments
- `GET /api/comments/comments/` - List all comments
- `POST /api/comments/comments/` - Create comment
- `GET /api/comments/comments/{id}/` - Get comment details
- `PUT /api/comments/comments/{id}/` - Update comment
- `DELETE /api/comments/comments/{id}/` - Delete comment

## Usage Examples

### Register a new user
```bash
curl -X POST http://localhost:8000/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepassword123"
  }'
```

### Create a project (with JWT token)
```bash
curl -X POST http://localhost:8000/api/projects/projects/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "name": "Website Redesign",
    "description": "Complete redesign of company website"
  }'
```

### Create a task in a project
```bash
curl -X POST http://localhost:8000/api/task/projects/1/tasks/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "Design Homepage",
    "description": "Create wireframes and mockups for homepage",
    "priority": "High",
    "status": "To Do"
  }'
```

### Add a comment to a task
```bash
curl -X POST http://localhost:8000/api/comments/comments/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "content": "Task is progressing well",
    "task": 1
  }'
```

### Add a member to a project
```bash
curl -X POST http://localhost:8000/api/projects/projects/1/add_member/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "user_id": 2,
    "role": "Member"
  }'
```

### Get comments for a task
```bash
curl -X GET http://localhost:8000/api/task/tasks/1/comments/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Database Migration Commands

```bash
# Create and apply migrations for all apps
python manage.py makemigrations projects
python manage.py makemigrations task
python manage.py makemigrations comments
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

## Sample Data Creation Script

```python
# Run this in Django shell: python manage.py shell
from django.contrib.auth.models import User
from projects.models import Project, ProjectMember
from task.models import Task
from comments.models import Comment

# Create sample users
user1 = User.objects.create_user(
    username='admin',
    email='admin@example.com',
    password='admin123',
    first_name='Admin',
    last_name='User'
)

user2 = User.objects.create_user(
    username='developer',
    email='dev@example.com',
    password='dev123',
    first_name='Developer',
    last_name='User'
)

# Create sample project
project = Project.objects.create(
    name='Sample Project',
    description='This is a sample project for testing',
    owner=user1
)

# Add project members
ProjectMember.objects.create(project=project, user=user1, role='Admin')
ProjectMember.objects.create(project=project, user=user2, role='Member')

# Create sample tasks
task1 = Task.objects.create(
    title='Setup Database',
    description='Create and configure the database schema',
    status='Done',
    priority='High',
    assigned_to=user1,
    project=project
)

task2 = Task.objects.create(
    title='Implement API',
    description='Develop REST API endpoints',
    status='In Progress',
    priority='Medium',
    assigned_to=user2,
    project=project
)

# Create sample comments
Comment.objects.create(
    content='Database setup completed successfully',
    user=user1,
    task=task1
)

Comment.objects.create(
    content='API development is 50% complete',
    user=user2,
    task=task2
)

print("Sample data created successfully!")
```

## Security Features

- JWT token authentication
- Password validation
- User permission checks
- CORS configuration
- Input validation and sanitization

## Technologies Used

- Django 4.2+
- Django REST Framework
- Django REST Framework SimpleJWT
- drf-spectacular (for API documentation)
- SQLite (default database)

## Development and Debugging

### Running Tests
```bash
# Run the project test script
python test_project.py

# Run Django's built-in tests
python manage.py test

# Check for any issues
python manage.py check
```

### Common Issues and Solutions

1. **Import Errors**: Make sure all dependencies are installed with `pip install -r requirement.txt`
2. **Database Issues**: Run migrations with `python manage.py migrate`
3. **Permission Errors**: Ensure you're authenticated and have proper permissions for the resources you're trying to access
4. **CORS Issues**: Check the CORS settings in `settings.py` if you're having frontend integration issues

### Environment Variables

You can set the following environment variables for production:
- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to 'false' for production
