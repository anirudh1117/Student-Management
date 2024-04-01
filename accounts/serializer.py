from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from django.contrib.auth.models import Group, update_last_login
from .models import UserAccount, Address
from utils.commonFunction import generate_password, string_to_uuid, convert_date_time_to_unix_time_millis, get_Choices, common_error_message, convert_unix_time_millis_to_date_time,convert_date_to_unix_time_millis,convert_unix_time_millis_to_date
from utils import constants
from students.serializer import StudentWriteSerializer, GuardianWriteSerializer
from staff.serializer import StaffWriteSerializer


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'


class UserAccountReadSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    date_of_birth = serializers.SerializerMethodField()
    last_login = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    gender = serializers.CharField(source='get_gender_display')
    role = serializers.CharField(source='get_role_display')

    def get_address(self, userAccount):
        address = userAccount.address_set.all()
        if address.first():
            return AddressSerializer(address, many=True).data
        else:
            return {}

    def get_profileLogo(self, userAccount):
        request = self.context.get("request")
        path = request.build_absolute_uri()
        path = path.replace('//', '/')
        path = path.split('/')
        url = path[0] + "//" + path[1]
        if userAccount.profileLogo.url is None:
            pass
        else:
            url = url + userAccount.profileLogo.url
        return url

    def get_last_login(self, userAccount):
        if userAccount.last_login is None:
            return ""
        return convert_date_time_to_unix_time_millis(userAccount.last_login)

    def get_created_at(self, userAccount):
        if userAccount.created_at is None:
            return ""
        return convert_date_time_to_unix_time_millis(userAccount.created_at)

    def get_updated_at(self, userAccount):
        if userAccount.updated_at is None:
            return ""
        return convert_date_time_to_unix_time_millis(userAccount.updated_at)

    def get_date_of_birth(self, userAccount):
        if userAccount.date_of_birth is None:
            return ""
        return convert_date_to_unix_time_millis(userAccount.date_of_birth)

    class Meta:
        model = UserAccount
        fields = ['id', 'email', 'first_name', 'middle_name', 'last_name', 'date_of_birth', 'address', 'phoneNo',
                  'bloodGroup', 'role', 'profileLogo', 'created_at', 'updated_at', 'last_login', 'gender', 'school']


class UserAccoutWriteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(read_only=True)
    groups = serializers.ListSerializer(
        child=serializers.CharField(), required=False)
    address = serializers.JSONField(write_only=True)
    role = serializers.ChoiceField(choices=get_Choices(
        constants.Role_Choices), required=True)
    gender = serializers.ChoiceField(choices=UserAccount.GENDER_CHOICES)
    others = serializers.JSONField(required=False)
    email = serializers.CharField(required=True)
    date_of_birth = serializers.CharField(required=True)

    def create(self, validated_data):
        request = self.context.get('request')
        others = validated_data.pop('others', {})
        date_of_birth = validated_data.get('date_of_birth', None)
        allowed_chars = validated_data['email'] + \
            '!@#$%' if date_of_birth is None else date_of_birth
        password = generate_password(8, allowed_chars)
        validated_data['password'] = password
        validated_data['school'] = request.user.school
        print(password)
        address_json = validated_data.get('address', '')
        groups_data = validated_data.get('groups', [])

        if date_of_birth is not None:
            validated_data['date_of_birth'] = convert_unix_time_millis_to_date(
                date_of_birth)

        account = UserAccount.objects.create_user(**validated_data)
        account.save()
        self.add_in_group(account, groups_data)

        if address_json != '':
            address_json['account'] = account.id
            serializer = AddressSerializer(data=address_json)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            else:
                raise serializers.ValidationError(serializer.errors)
            # raise serializers.ValidationError("Please Provide address field!")
        # elif groups_data == []:
            # raise serializers.ValidationError("Please provide groups list,User need to be added in one or more groups!")
        others['account'] = account.id
        others['school'] = request.user.school
        if account.role.lower() == "student":
            print(others)
            studentSerializer = StudentWriteSerializer(
                data=others, context={'request': request})
            if studentSerializer.is_valid(raise_exception=True):
                studentSerializer.save()
            else:
                raise serializers.ValidationError(studentSerializer.errors)
        elif account.role.lower() == "staf":
            print(others)
            staffSerializer = StaffWriteSerializer(
                data=others, context={'request': request})
            print(staffSerializer)
            if staffSerializer.is_valid(raise_exception=True):
                staffSerializer.save()
            else:
                raise serializers.ValidationError(staffSerializer.errors)
        elif account.role.lower() == "guardian":
            guardianSerializer = GuardianWriteSerializer(
                data=others, context={'request': request})
            if guardianSerializer.is_valid(raise_exception=True):
                guardianSerializer.save()
            else:
                raise serializers.ValidationError(guardianSerializer.errors)
        return account

    def update(self, instance, validated_data):
        id = string_to_uuid(instance.id)
        validated_data['role'] = instance.role
        address_json = validated_data.get('address', '')
        groups_data = validated_data.get('groups', [])
        if address_json != '':
            id = instance.address
            Address.objects.filter(id=id).update(**address_json)
        account = UserAccount.objects.filter(id=id).update(**validated_data)
        if groups_data != []:
            account.groups.clear()
            self.add_in_group(account, groups_data)

    def add_in_group(self, account, groups_data):
        if len(groups_data) != 0:
            user_group = Group.objects.get(name_in=groups_data)
            # if user_group.first():
            # account.groups.add(user_group)
            account.groups.set(user_group)

    class Meta:
        model = UserAccount
        exclude = ('school', 'is_superuser', )


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        superuser = self.user.is_superuser
        if not superuser:
            if not self.user.school:
                raise serializers.ValidationError(common_error_message(
                    "Sorry, You are not linked with any school!"))
            elif not self.user.school.current_session:
                raise serializers.ValidationError(common_error_message(
                    "Sorry, Your school is not registered for this Session!"))

        update_last_login(None, self.user)

        data['email'] = self.user.email
        data['role'] = self.user.role
        data['first_name'] = self.user.first_name
        data['middle_name'] = self.user.middle_name
        data['last_name'] = self.user.last_name

        return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.token_class(attrs["refresh"])
        user_id = refresh.access_token.payload['user_id']
        user_obj = UserAccount.objects.filter(id=user_id)
        if user_obj.first():
            user_obj = user_obj[0]
            superuser = user_obj.is_superuser
            school = user_obj.school
            if not superuser:
                if not school:
                    raise serializers.ValidationError(common_error_message(
                        "Sorry, You are not linked with any school!"))
                elif not school.current_session:
                    raise serializers.ValidationError(common_error_message(
                        "Sorry, Your school is not registered for this Session!"))

        return data
