"""
Unit tests for domain value objects
"""
import pytest
import uuid

from app.domain.value_objects.common import (
    Email, Username, PersonName, EntityId, PositionName
)


class TestEmail:
    """Test Email value object"""

    def test_valid_email(self):
        """Test valid email creation"""
        email = Email("test@example.com")
        assert email.value == "test@example.com"
        assert str(email) == "test@example.com"

    def test_valid_email_with_subdomain(self):
        """Test valid email with subdomain"""
        email = Email("user@mail.example.com")
        assert email.value == "user@mail.example.com"

    def test_valid_email_with_plus(self):
        """Test valid email with plus sign"""
        email = Email("user+tag@example.com")
        assert email.value == "user+tag@example.com"

    def test_invalid_email_no_at(self):
        """Test invalid email without @ symbol"""
        with pytest.raises(ValueError, match="Invalid email format"):
            Email("testexample.com")

    def test_invalid_email_no_domain(self):
        """Test invalid email without domain"""
        with pytest.raises(ValueError, match="Invalid email format"):
            Email("test@")

    def test_invalid_email_no_tld(self):
        """Test invalid email without top-level domain"""
        with pytest.raises(ValueError, match="Invalid email format"):
            Email("test@example")

    def test_email_immutability(self):
        """Test that email is immutable"""
        email = Email("test@example.com")
        with pytest.raises(AttributeError):
            email.value = "new@example.com"


class TestUsername:
    """Test Username value object"""

    def test_valid_username(self):
        """Test valid username creation"""
        username = Username("testuser")
        assert username.value == "testuser"
        assert str(username) == "testuser"

    def test_valid_username_with_numbers(self):
        """Test valid username with numbers"""
        username = Username("user123")
        assert username.value == "user123"

    def test_valid_username_with_underscore(self):
        """Test valid username with underscore"""
        username = Username("test_user")
        assert username.value == "test_user"

    def test_valid_username_with_hyphen(self):
        """Test valid username with hyphen"""
        username = Username("test-user")
        assert username.value == "test-user"

    def test_invalid_username_too_short(self):
        """Test invalid username too short"""
        with pytest.raises(ValueError, match="Invalid username"):
            Username("ab")

    def test_invalid_username_too_long(self):
        """Test invalid username too long"""
        with pytest.raises(ValueError, match="Invalid username"):
            Username("a" * 51)

    def test_invalid_username_special_chars(self):
        """Test invalid username with special characters"""
        with pytest.raises(ValueError, match="Invalid username"):
            Username("test@user")

    def test_invalid_username_spaces(self):
        """Test invalid username with spaces"""
        with pytest.raises(ValueError, match="Invalid username"):
            Username("test user")


class TestPersonName:
    """Test PersonName value object"""

    def test_valid_name(self):
        """Test valid name creation"""
        name = PersonName("John")
        assert name.value == "John"
        assert str(name) == "John"

    def test_valid_name_with_space(self):
        """Test valid name with space"""
        name = PersonName("John Doe")
        assert name.value == "John Doe"

    def test_valid_name_with_hyphen(self):
        """Test valid name with hyphen"""
        name = PersonName("Mary-Jane")
        assert name.value == "Mary-Jane"

    def test_valid_name_with_apostrophe(self):
        """Test valid name with apostrophe"""
        name = PersonName("O'Connor")
        assert name.value == "O'Connor"

    def test_invalid_name_empty(self):
        """Test invalid empty name"""
        with pytest.raises(ValueError, match="Invalid name"):
            PersonName("")

    def test_invalid_name_too_long(self):
        """Test invalid name too long"""
        with pytest.raises(ValueError, match="Invalid name"):
            PersonName("a" * 51)

    def test_invalid_name_numbers(self):
        """Test invalid name with numbers"""
        with pytest.raises(ValueError, match="Invalid name"):
            PersonName("John123")

    def test_invalid_name_special_chars(self):
        """Test invalid name with special characters"""
        with pytest.raises(ValueError, match="Invalid name"):
            PersonName("John@Doe")


class TestEntityId:
    """Test EntityId value object"""

    def test_valid_entity_id(self):
        """Test valid entity ID creation"""
        uuid_value = uuid.uuid4()
        entity_id = EntityId(uuid_value)
        assert entity_id.value == uuid_value
        assert str(entity_id) == str(uuid_value)

    def test_generate_entity_id(self):
        """Test entity ID generation"""
        entity_id = EntityId.generate()
        assert isinstance(entity_id.value, uuid.UUID)

    def test_from_string_valid(self):
        """Test entity ID creation from valid string"""
        uuid_str = str(uuid.uuid4())
        entity_id = EntityId.from_string(uuid_str)
        assert str(entity_id) == uuid_str

    def test_from_string_invalid(self):
        """Test entity ID creation from invalid string"""
        with pytest.raises(ValueError, match="Invalid UUID string"):
            EntityId.from_string("not-a-uuid")

    def test_invalid_entity_id_type(self):
        """Test invalid entity ID with wrong type"""
        with pytest.raises(ValueError, match="ID must be a valid UUID"):
            EntityId("not-a-uuid-object")

    def test_entity_id_immutability(self):
        """Test that entity ID is immutable"""
        entity_id = EntityId(uuid.uuid4())
        with pytest.raises(AttributeError):
            entity_id.value = uuid.uuid4()


class TestPositionName:
    """Test PositionName value object"""

    def test_valid_position_name(self):
        """Test valid position name creation"""
        name = PositionName("Software Engineer")
        assert name.value == "Software Engineer"
        assert str(name) == "Software Engineer"

    def test_valid_position_name_with_numbers(self):
        """Test valid position name with numbers"""
        name = PositionName("Engineer Level 3")
        assert name.value == "Engineer Level 3"

    def test_valid_position_name_with_special_chars(self):
        """Test valid position name with allowed special characters"""
        name = PositionName("VP - Sales & Marketing (Remote)")
        assert name.value == "VP - Sales & Marketing (Remote)"

    def test_valid_position_name_with_slash(self):
        """Test valid position name with slash"""
        name = PositionName("UI/UX Designer")
        assert name.value == "UI/UX Designer"

    def test_invalid_position_name_empty(self):
        """Test invalid empty position name"""
        with pytest.raises(ValueError, match="Invalid position name"):
            PositionName("")

    def test_invalid_position_name_too_long(self):
        """Test invalid position name too long"""
        with pytest.raises(ValueError, match="Invalid position name"):
            PositionName("a" * 101)

    def test_invalid_position_name_special_chars(self):
        """Test invalid position name with forbidden special characters"""
        with pytest.raises(ValueError, match="Invalid position name"):
            PositionName("Software Engineer @ Company")

    def test_position_name_immutability(self):
        """Test that position name is immutable"""
        name = PositionName("Software Engineer")
        with pytest.raises(AttributeError):
            name.value = "New Position"