from rest_framework.exceptions import APIException


class InvalidUuidFormat(APIException):
    status_code = 400
    default_detail = "Not found, because of an invalid identifier UUID format"
    default_code = "invalid_uuid_format"

class InternalServerError(APIException):
    status_code = 500
    default_detail = "Processing Failure, Backend fails to execute ur request!"
    default_code = "Internal_Server_Error"

class SchoolAuthorizationError(APIException):
    status_code = 401
    default_detail = "Sorry, You are not linked with any school!"
    default_code = "School_Authorization_Error"

class SchoolSessionAuthorizationError(APIException):
    status_code = 401
    default_detail = "Sorry, Your school is not registered for this Session!"
    default_code = "School_Session_Authorization_Error"