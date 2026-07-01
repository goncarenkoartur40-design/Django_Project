import pytest

from devboard.models import Task


@pytest.mark.django_db
class TestTaskModel:
    def test_defoult_status_is_todo(self,task):
        assert task.status == Task.Status.TODO

