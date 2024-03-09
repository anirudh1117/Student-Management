from rest_framework import serializers
from .models import Leave, LeaveType

from utils.commonFunction import common_error_message, convert_unix_time_millis_to_date_time
from utils import constants


class LeaveTypeSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['session'] = request.user.school.current_session

        return super().create(validated_data)

    class Meta:
        model = LeaveType
        fields = '__all__'


class LeaveReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Leave
        fields = '__all__'


class LeaveWriteSerializer(serializers.ModelSerializer):
    leave_Type = serializers.CharField()
    start_date = serializers.CharField()
    end_date = serializers.CharField()

    def check_manager(self, account):
        if account and account.role == constants.STAFF:
            if account.staff:
                if account.staff.manager:
                    if account.staff.manager.account:
                        pass
                    else:
                        raise serializers.ValidationError(common_error_message(
                            "Manager doesn't exist for the Employee!"))
                else:
                    raise serializers.ValidationError(common_error_message(
                        "Employee is not tagged with any Manager!"))
            else:
                raise serializers.ValidationError(common_error_message(
                    "Staff account doesn't exist for the   Employee!"))
        elif account and account.role == constants.STUDENT:
            pass
        else:
            raise serializers.ValidationError(common_error_message(
                "User doesn't exit or user need to have role of STAFF or STUDENT!"))

    def check_leave_available(self, request, account, leave_type):
        if account and leave_type:
            total_leave = LeaveType.objects.filter(
                name_slug=leave_type, session=request.user.school.current_session,  session__school=request.user.school)
            if total_leave and len(total_leave) > 0:
                print(total_leave)
                self.leave_type = total_leave[0]
                taken_leave = Leave.objects.filter(
                    account=account, leave_Type=self.leave_type, session=request.user.school.current_session,  session__school=request.user.school)
                print(taken_leave)
                taken_leave_count = 0
                for items in taken_leave:
                    taken_leave_count += items.get_total_leave_days()
                leave_left = total_leave[0].total - taken_leave_count
                if leave_left > 0:
                    return leave_left
                else:
                    raise serializers.ValidationError(common_error_message(
                        "No more leaves left for the Employee."))
                
    def check_leave_already_applied(self, request, start_date, account):
        leave_obj = Leave.objects.filter(account=account, session=request.user.school.current_session,  session__school=request.user.school)
        leave_obj = leave_obj.filter(start_date__gte = start_date, end_date__lte = start_date)
        if leave_obj.first():
            raise serializers.ValidationError(common_error_message("User has already applied leave for these dates!."))

    def __init__(self, instance=None, data=..., **kwargs):
        self.leave_type = None
        super().__init__(instance, data, **kwargs)

    def create(self, validated_data):
        request = self.context.get('request')

        account = validated_data.get('account', None)
        leave_type = validated_data.get('leave_Type', None)
        start_date = validated_data.get('start_date', None)
        end_date = validated_data.get('end_date', None)

        validated_data['start_date'] = convert_unix_time_millis_to_date_time(start_date)
        validated_data['end_date'] = convert_unix_time_millis_to_date_time(end_date)
        self.check_leave_already_applied(request, validated_data['start_date'], account)
        self.check_leave_available(request, account, leave_type)
        self.check_manager(account)

        validated_data['leave_Type'] = self.leave_type
        validated_data['session'] = request.user.school.current_session


        return super().create(validated_data)

    class Meta:
        model = Leave
        exclude = ('status',)
