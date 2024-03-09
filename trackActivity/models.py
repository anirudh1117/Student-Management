import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from school.models import School

User = get_user_model()

CREATE, READ, UPDATE, DELETE = "Create", "Read", "Update", "Delete"
LOGIN, LOGOUT, LOGIN_FAILED = "Login", "Logout", "Login Failed"
ACTION_TYPES = [
    (CREATE, CREATE),
    (READ, READ),
    (UPDATE, UPDATE),
    (DELETE, DELETE),
    (LOGIN, LOGIN),
    (LOGOUT, LOGOUT),
    (LOGIN_FAILED, LOGIN_FAILED),
]

SUCCESS, FAILED = "Success", "Failed"
ACTION_STATUS = [(SUCCESS, SUCCESS), (FAILED, FAILED)]


class ActivityLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    actor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    action_type = models.CharField(choices=ACTION_TYPES, max_length=15)
    action_time = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True, null=True)
    status = models.CharField(choices=ACTION_STATUS, max_length=7, default=SUCCESS)
    data = models.JSONField(default=dict)
    school = models.ForeignKey(School, on_delete=models.DO_NOTHING, null=True)

    # for generic relations
    content_type = models.ForeignKey(
        ContentType, models.SET_NULL, blank=True, null=True
    )

    def __str__(self) -> str:
        return f"{self.action_type} by {self.actor} on {self.action_time}"