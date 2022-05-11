import pytest
from authentication.models import User


class TestModelUser:

    @classmethod
    def setup(cls):
        pass

    @pytest.mark.django_db
    def test_user_count(self):
        assert User.objects.count() == 0
