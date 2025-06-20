from rest_framework import serializers
from .models import Pwd, Infrastructure, SeniorCitizen, Households, HouseholdMember, Feedback

class PwdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pwd
        fields = ['id', 'people', 'age', 'gender', 'location']

class InfrastructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Infrastructure
        fields = '__all__'
        

class SeniorCitizenSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeniorCitizen
        fields = '__all__'
        

class HouseholdMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseholdMember
        fields = ['id', 'name', 'age', 'role']

class HouseholdsSerializer(serializers.ModelSerializer):
    members = HouseholdMemberSerializer(many=True)

    class Meta:
        model = Households
        fields = ['id', 'family_name', 'members', 'location']

    def create(self, validated_data):
        members_data = validated_data.pop('members')
        household = Households.objects.create(**validated_data)
        for member_data in members_data:
            HouseholdMember.objects.create(household=household, **member_data)
        return household
    


class StatsSerializer(serializers.Serializer):
    total_pwds = serializers.IntegerField()
    total_seniors = serializers.IntegerField()
    total_households = serializers.IntegerField()
    
class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'    