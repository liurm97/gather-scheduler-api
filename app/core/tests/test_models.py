"""
Tests for models
"""

# import TestCase test suite
from django.test import TestCase

# import get_user_model to reference the currently active user model
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Test creating a user with email is successful"""
        # define test email and test password
        email = "test@example.com"
        password = "testpass123"
        # create a test user
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        # Test if test user's email is the same as the test email
        self.assertEqual(user.email, email)
        # Test if test user's password is the same as the hashed test password
        self.assertTrue(user.check_password(password), True)

    def test_user_email_unsuccessful_due_to_no_email(self):
        """Test creating a user without an email is unsuccessful"""
        email = ""
        self.assertRaises(
            ValidationError, validate_email, email
        )

    def test_user_email_unsuccessful_due_to_incorrect_email_format(self):
        """Test creating a user with incorrect email format is unsuccessful"""
        email = "apple@"
        self.assertRaises(
            ValidationError, validate_email, email
        )

    def test_user_email_is_normalized(self):
        """Test creating a user email is normalized and successful"""
        # List of unnormalized and normalized email addresses
        test_emails: list[list[str]] = [
            ["TEST1@EXAMPLE.COM", "TEST1@example.com"],
            ["TEST2@example.COM", "TEST2@example.com"],
            ["TEST3@EXAMPLE.com", "TEST3@example.com"],
            ["Test4@example.COM", "Test4@example.com"],
            ["Test5@Example.com", "Test5@example.com"],
        ]
        # Check that test email is normalized
        for raw_email, normalized_email in test_emails:
            user = get_user_model().objects.create_user(email=raw_email,
                                                        password="temp")
            self.assertEqual(user.email, normalized_email)

    def test_user_email_raises_ValueError_if_not_provided(self):
        """Test email address must be provided when creating a user"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email="", password="temp")

    def test_create_superuser_with_email_successful(self):
        """Test creating a superuser with email is successful"""
        superuser = get_user_model().objects.create_superuser(
            email="test@example.com", password="temp")
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
