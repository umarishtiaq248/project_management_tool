#!/usr/bin/env python
"""
Test script to verify the project management tool functionality
"""
import os
import sys
import django
from django.conf import settings

# Add the project directory to Python path
sys.path.insert(0, '/home/umar-ishtiaq/Company Projects/project_management_tool')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_management_tool.settings')
django.setup()

def test_models():
    """Test model creation and relationships"""
    print("Testing models...")
    
    from django.contrib.auth.models import User
    from projects.models import Project, ProjectMember
    from task.models import Task
    from comments.models import Comment
    
    try:
        # Test user creation
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        print("✓ User creation successful")
        
        # Test project creation
        project = Project.objects.create(
            name='Test Project',
            description='A test project',
            owner=user
        )
        print("✓ Project creation successful")
        
        # Test project member creation
        member = ProjectMember.objects.create(
            project=project,
            user=user,
            role='Admin'
        )
        print("✓ ProjectMember creation successful")
        
        # Test task creation
        task = Task.objects.create(
            title='Test Task',
            description='A test task',
            project=project,
            assigned_to=user,
            status='To Do',
            priority='Medium'
        )
        print("✓ Task creation successful")
        
        # Test comment creation
        comment = Comment.objects.create(
            content='Test comment',
            user=user,
            task=task
        )
        print("✓ Comment creation successful")
        
        # Test relationships
        assert project.owner == user
        assert task.project == project
        assert comment.task == task
        assert comment.user == user
        print("✓ Model relationships working correctly")
        
        # Clean up
        comment.delete()
        task.delete()
        member.delete()
        project.delete()
        user.delete()
        print("✓ Model cleanup successful")
        
    except Exception as e:
        print(f"✗ Model test failed: {e}")
        return False
    
    return True

def test_serializers():
    """Test serializer validation"""
    print("\nTesting serializers...")
    
    from project_management_tool.serializers import UserRegistrationSerializer
    from projects.serializers import ProjectSerializer
    from task.serializers import TaskSerializer
    from comments.serializers import CommentSerializer
    
    try:
        # Test user registration serializer
        user_data = {
            'username': 'testuser2',
            'email': 'test2@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        user_serializer = UserRegistrationSerializer(data=user_data)
        assert user_serializer.is_valid(), f"User serializer errors: {user_serializer.errors}"
        print("✓ User registration serializer validation successful")
        
        # Test project serializer validation
        project_data = {
            'name': 'Test Project',
            'description': 'A test project description'
        }
        project_serializer = ProjectSerializer(data=project_data)
        assert project_serializer.is_valid(), f"Project serializer errors: {project_serializer.errors}"
        print("✓ Project serializer validation successful")
        
        # Test invalid project name
        invalid_project_data = {
            'name': '',
            'description': 'A test project description'
        }
        invalid_project_serializer = ProjectSerializer(data=invalid_project_data)
        assert not invalid_project_serializer.is_valid()
        print("✓ Project serializer properly rejects empty name")
        
        # Test task serializer validation
        task_data = {
            'title': 'Test Task',
            'description': 'A test task description',
            'status': 'To Do',
            'priority': 'Medium'
        }
        task_serializer = TaskSerializer(data=task_data)
        assert task_serializer.is_valid(), f"Task serializer errors: {task_serializer.errors}"
        print("✓ Task serializer validation successful")
        
        # Test comment serializer validation
        comment_data = {
            'content': 'Test comment content'
        }
        comment_serializer = CommentSerializer(data=comment_data)
        assert comment_serializer.is_valid(), f"Comment serializer errors: {comment_serializer.errors}"
        print("✓ Comment serializer validation successful")
        
        # Test invalid comment (empty content)
        invalid_comment_data = {
            'content': ''
        }
        invalid_comment_serializer = CommentSerializer(data=invalid_comment_data)
        assert not invalid_comment_serializer.is_valid()
        print("✓ Comment serializer properly rejects empty content")
        
    except Exception as e:
        print(f"✗ Serializer test failed: {e}")
        return False
    
    return True

def test_imports():
    """Test that all imports work correctly"""
    print("\nTesting imports...")
    
    try:
        # Test view imports
        from project_management_tool.views import UserRegistrationView, UserLoginView, UserViewSet
        from projects.views import ProjectViewSet
        from task.views import TaskViewSet
        from comments.views import CommentViewSet
        print("✓ All view imports successful")
        
        # Test serializer imports
        from project_management_tool.serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer
        from projects.serializers import ProjectSerializer, ProjectMemberSerializer
        from task.serializers import TaskSerializer
        from comments.serializers import CommentSerializer
        print("✓ All serializer imports successful")
        
        # Test model imports
        from projects.models import Project, ProjectMember
        from task.models import Task
        from comments.models import Comment
        print("✓ All model imports successful")
        
    except Exception as e:
        print(f"✗ Import test failed: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("Starting project management tool tests...\n")
    
    tests = [
        test_imports,
        test_models,
        test_serializers
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n{'='*50}")
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! The project appears to be working correctly.")
    else:
        print("✗ Some tests failed. Please review the issues above.")
    
    return passed == total

if __name__ == '__main__':
    main()