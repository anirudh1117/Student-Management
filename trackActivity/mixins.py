import logging
import time

from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from django.utils.functional import SimpleLazyObject

from .models import ActivityLog, READ, CREATE, UPDATE, DELETE, SUCCESS, FAILED
from .signals import get_client_ip
from utils.commonFunction import common_error_message
from accounts.models import UserAccount


class ActivityLogMixin:
    """
    Mixin to track user actions

    :cvar log_message:
        Log message to populate remarks in LogAction

        type --> str

        set this value or override get_log_message

        If not set then, default log message is generated
    """

    log_message = None

    def _get_action_type(self, request) -> str:
        return self.action_type_mapper().get(f"{request.method.upper()}")

    def _build_log_message(self, request) -> str:
        return f"User: {self._get_user(request)} -- Action Type: {self._get_action_type(request)} -- Path: {request.path} -- Path Name: {request.resolver_match.url_name}"

    def get_log_message(self, request) -> str:
        return self.log_message or self._build_log_message(request)

    @staticmethod
    def action_type_mapper():
        return {
            "GET": READ,
            "POST": CREATE,
            "PUT": UPDATE,
            "PATCH": UPDATE,
            "DELETE": DELETE,
        }

    @staticmethod
    def _get_user(request):
        return request.user if request.user.is_authenticated else None

    def _write_log(self, request, response):
        status = SUCCESS if response.status_code < 400 else FAILED
        actor = self._get_user(request)

        if actor and not getattr(settings, "TESTING", False):
            logging.info("Started Log Entry")

            data = {
                "actor": actor,
                "action_type": self._get_action_type(request),
                "status": status,
                "remarks": self.get_log_message(request),
                "school" : request.user.school,
            }

            try:
                app, model = self.perm_slug.split(".")
                data["content_type"] = ContentType.objects.get(
                    app_label__iexact=app, model__iexact=model.lower())

                # data["content_object"] = self.get_object()
                jsonData = {
                    'client-ip': get_client_ip(request),
                    'api-response-time-ms': int((time.time() - request.start_time)*1000),
                    'path': request.path,
                    'path-name': request.resolver_match.url_name
                }

                data["data"] = jsonData
            except (AttributeError, ValidationError):
                data["content_type"] = None
            except AssertionError:
                pass

            ActivityLog.objects.create(**data)

    def finalize_response(self, request, *args, **kwargs):
        response = super().finalize_response(request, *args, **kwargs)
        self._write_log(request, response)
        return response

    def initialize_request(self, request, *args, **kwargs):
        request = super().initialize_request(request, *args, **kwargs)
        request.start_time = time.time()
        return request
