import pytest
from authentication.models import User


class TestModelUser:

    @classmethod
    def setup(cls):
        cls.user_test = {'username': 'user_test',
                         'role': 'Sailor team'}
        cls.user_test1 = User.objects.create_user(username="user_test1",
                                                  role='Sailor team'
                                                  )
        cls.user_test2 = User.objects.create_user(username='user_test2',
                                                  email='user2@test.fr',
                                                  role='Support team')
        cls.user_test3 = User.objects.create_user(username='user_test3',
                                                  email=None,
                                                  role='Management team')

    @pytest.mark.django_db
    def test_user_count(self):
        user = User.objects.create_user(**self.user_test)
        assert User.objects.count() == 4

    @pytest.mark.django_db
    def test_user_has_role(self):
        assert self.user_test1.role

    @pytest.mark.django_db
    def test_display_user(self):
        assert str(self.user_test1) == 'user_test1 Sailor team'
