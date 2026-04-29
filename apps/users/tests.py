import pytest
from django.contrib.auth import get_user_model
from apps.users.models import NonTeachingStaff, ActivityLog

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    def test_user_creation(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="testpass123"
        )
        assert user.username == "testuser"
        assert user.check_password("testpass123")
        assert user.role == User.Role.STUDENT

    def test_user_str(self):
        user = User.objects.create_user(
            username="testuser2",
            email="test2@test.com",
            password="testpass123",
            first_name="John",
            last_name="Doe"
        )
        user.role = User.Role.TEACHER
        assert "John Doe" in str(user)

    def test_is_admin_property(self):
        user = User.objects.create_user(
            username="adminuser",
            email="admin@test.com",
            password="testpass123"
        )
        user.role = User.Role.ADMIN
        assert user.is_admin_user is True
        assert user.is_teacher is False

    def test_is_teacher_property(self):
        user = User.objects.create_user(
            username="teacheruser",
            email="teacher@test.com",
            password="testpass123"
        )
        user.role = User.Role.TEACHER
        assert user.is_teacher is True
        assert user.is_student is False


@pytest.mark.django_db
class TestNonTeachingStaffModel:
    def test_staff_id_auto_generation(self):
        user = User.objects.create_user(
            username="staff1",
            email="staff1@test.com",
            password="testpass123"
        )
        staff = NonTeachingStaff.objects.create(
            user=user,
            staff_id=""
        )
        assert staff.staff_id == "STAFF00001"

    def test_staff_id_increments(self):
        user1 = User.objects.create_user(
            username="staffuser1",
            email="staff1@test.com",
            password="testpass123"
        )
        user2 = User.objects.create_user(
            username="staffuser2",
            email="staff2@test.com",
            password="testpass123"
        )
        staff1 = NonTeachingStaff.objects.create(user=user1, staff_id="")
        staff2 = NonTeachingStaff.objects.create(user=user2, staff_id="")
        assert staff1.staff_id == "STAFF00001"
        assert staff2.staff_id == "STAFF00002"

    def test_staff_id_first_staff_with_invalid_format(self):
        user = User.objects.create_user(
            username="staffuser3",
            email="staff3@test.com",
            password="testpass123"
        )
        staff = NonTeachingStaff.objects.create(user=user, staff_id="")
        assert staff.staff_id == "STAFF00001"


@pytest.mark.django_db
class TestActivityLogModel:
    def test_activity_log_creation(self):
        user = User.objects.create_user(
            username="loguser",
            email="log@test.com",
            password="testpass123"
        )
        log = ActivityLog.log(
            user=user,
            action=ActivityLog.ActionType.CREATE,
            description="Test log entry",
            category="test"
        )
        assert log.action == ActivityLog.ActionType.CREATE
        assert "Test log entry" in log.description

    def test_activity_log_str(self):
        user = User.objects.create_user(
            username="loguser2",
            email="log2@test.com",
            password="testpass123",
            first_name="Jane",
            last_name="Smith"
        )
        log = ActivityLog.objects.create(
            user=user,
            action=ActivityLog.ActionType.LOGIN,
            description="User logged in successfully"
        )
        assert "Jane Smith" in str(log)