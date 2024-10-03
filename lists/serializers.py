from django.contrib.auth.models import User
from rest_framework import serializers
from users.serializers import UserSerializer
from .models import List
from ai_agent.models import AgentRole
from ai_agent.serializers import AgentRoleSerializer


class ListCreationSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    agent_role_description = serializers.CharField(required=True)
    owner = serializers.IntegerField(required=True)

    def create(self, validated_data):
        # Create the AgentRole instance
        agent_role = AgentRole.objects.create(
            name=validated_data['name'],
            description=validated_data['agent_role_description']
        )
        
        # Create the List instance
        owner = validated_data['owner']
        list_owner = User.objects.get(id=owner)
        list_instance = List.objects.create(
            name=validated_data['name'],
            description=validated_data['description'],
            agent_role=agent_role,
            owner=list_owner  # Assuming owner is a foreign key to a User model
        )
        
        return list_instance


class ListSerializer(serializers.ModelSerializer):
    agent_role = AgentRoleSerializer(read_only=True) # to view the agent when querying a List
    owner = UserSerializer(read_only=True)
    updated_at = serializers.SerializerMethodField(
        method_name='get_formatted_date')

    class Meta:
        model = List
        fields = ['id', 'name', 'description', 'agent_role', 'is_closed', 'owner', 'updated_at', 'slug', 'meta_description']

    # Provide a more simple date information for the front end
    def get_formatted_date(self, list: List):
        return list.updated_at.strftime('%Y-%m-%d')