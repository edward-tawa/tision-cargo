from phonenumber_field.serializerfields import PhoneNumberField as PhoneSerializerField
from rest_framework import serializers

from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration/creation.
    """

    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    age = serializers.IntegerField(required=True)
    role = serializers.ChoiceField(choices=CustomUser.ROLE.choices, required=True)
    status = serializers.ChoiceField(choices=CustomUser.STATUS.choices, required=True)

    # Use the specialized phone number serializer field
    phone_number = PhoneSerializerField(required=True)

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
            "age",
            "phone_number",
            "role",
            "status",
        ]
