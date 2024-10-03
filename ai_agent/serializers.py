from rest_framework import serializers
from .models import AgentRole, AgentResponse


class AgentRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = AgentRole
        fields = ['id', 'name', 'description', 'created_at']


class AgentResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = AgentResponse
        fields = ['id', 'video', 'transcript', 'agent_role', 'agent_response', 'created_at']