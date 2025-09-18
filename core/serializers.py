from rest_framework import serializers

from core.models import Group, UserGroup, Expense


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

        def create(self, validated_data):
            return Group.objects.create(**validated_data)

class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = '__all__'
        def create(self, validated_data):
            return UserGroup.objects.create(**validated_data)


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

        def create(self, validated_data):
            return Expense.objects.create(**validated_data)