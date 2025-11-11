import pytest
from pydantic import ValidationError
from app.schemas.base import UserBase, PasswordMixin, UserCreate, UserLogin


def test_user_base_valid():
    """Test UserBase with valid data."""
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "username": "johndoe",
    }
    user = UserBase(**data)
    assert user.first_name == "John"
    assert user.email == "john.doe@example.com"


def test_user_base_invalid_email():
    """Test UserBase with invalid email."""
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "invalid-email",
        "username": "johndoe",
    }
    with pytest.raises(ValidationError):
        UserBase(**data)


def test_password_mixin_valid():
    """Test PasswordMixin with valid password."""
    data = {"password": "SecurePass123"}
    password_mixin = PasswordMixin(**data)
    assert password_mixin.password == "SecurePass123"


def test_password_mixin_invalid_short_password():
    """Test PasswordMixin with short password."""
    data = {"password": "short"}
    with pytest.raises(ValidationError):
        PasswordMixin(**data)


def test_password_mixin_no_uppercase():
    """Test PasswordMixin with no uppercase letter."""
    data = {"password": "lowercase1"}
    with pytest.raises(ValidationError, match="Password must contain at least one uppercase letter"):
        PasswordMixin(**data)


def test_password_mixin_no_lowercase():
    """Test PasswordMixin with no lowercase letter."""
    data = {"password": "UPPERCASE1"}
    with pytest.raises(ValidationError, match="Password must contain at least one lowercase letter"):
        PasswordMixin(**data)


def test_password_mixin_no_digit():
    """Test PasswordMixin with no digit."""
    data = {"password": "NoDigitsHere"}
    with pytest.raises(ValidationError, match="Password must contain at least one digit"):
        PasswordMixin(**data)


def test_user_create_valid():
    """Test UserCreate with valid data."""
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "username": "johndoe",
        "password": "SecurePass123",
    }
    user_create = UserCreate(**data)
    assert user_create.username == "johndoe"
    assert user_create.password == "SecurePass123"


def test_user_create_invalid_password():
    """Test UserCreate with invalid password."""
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "username": "johndoe",
        "password": "short",
    }
    with pytest.raises(ValidationError):
        UserCreate(**data)


def test_user_login_valid():
    """Test UserLogin with valid data."""
    data = {"username": "johndoe", "password": "SecurePass123"}
    user_login = UserLogin(**data)
    assert user_login.username == "johndoe"


def test_user_login_invalid_username():
    """Test UserLogin with short username."""
    data = {"username": "jd", "password": "SecurePass123"}
    with pytest.raises(ValidationError):
        UserLogin(**data)


def test_user_login_invalid_password():
    """Test UserLogin with invalid password."""
    data = {"username": "johndoe", "password": "short"}
    with pytest.raises(ValidationError):
        UserLogin(**data)


def test_password_mixin_five_characters():
    """Test PasswordMixin with 5 characters (just under minimum)."""
    data = {"password": "Pas12"}
    with pytest.raises(ValueError, match="Password must be at least 6 characters long"):
        PasswordMixin(**data)


def test_password_mixin_six_characters_all_requirements():
    """Test PasswordMixin with exactly 6 characters meeting all requirements."""
    data = {"password": "Pass12"}
    password_mixin = PasswordMixin(**data)
    assert password_mixin.password == "Pass12"


def test_password_mixin_only_lowercase_and_digits():
    """Test PasswordMixin with lowercase and digits but no uppercase."""
    data = {"password": "password123"}
    with pytest.raises(ValueError, match="Password must contain at least one uppercase letter"):
        PasswordMixin(**data)


def test_password_mixin_only_uppercase_and_digits():
    """Test PasswordMixin with uppercase and digits but no lowercase."""
    data = {"password": "PASSWORD123"}
    with pytest.raises(ValueError, match="Password must contain at least one lowercase letter"):
        PasswordMixin(**data)


def test_password_mixin_only_letters():
    """Test PasswordMixin with only letters (no digits)."""
    data = {"password": "PasswordOnly"}
    with pytest.raises(ValueError, match="Password must contain at least one digit"):
        PasswordMixin(**data)


def test_password_mixin_max_length():
    """Test PasswordMixin with maximum allowed length (128 characters)."""
    long_password = "A" * 64 + "a" * 63 + "1"  # 128 chars with uppercase, lowercase, digit
    data = {"password": long_password}
    password_mixin = PasswordMixin(**data)
    assert len(password_mixin.password) == 128


def test_password_mixin_exceeds_max_length():
    """Test PasswordMixin with password exceeding max length."""
    too_long_password = "A" * 129
    data = {"password": too_long_password}
    with pytest.raises(ValidationError):
        PasswordMixin(**data)