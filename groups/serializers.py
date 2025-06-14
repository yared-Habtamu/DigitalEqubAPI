from rest_framework import serializers
from .models import EqubGroup, Membership, Payout
from users.serializers import UserSerializer


class MembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Membership
        fields = ['id', 'user', 'joined_at', 'has_received_payout', 'payout_order']


class PayoutSerializer(serializers.ModelSerializer):
    recipient = UserSerializer(read_only=True)

    class Meta:
        model = Payout
        fields = ['id', 'recipient', 'amount', 'round_number', 'payout_date']


class EqubGroupSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    members = MembershipSerializer(many=True, read_only=True)
    payouts = PayoutSerializer(many=True, read_only=True)

    class Meta:
        model = EqubGroup
        fields = [
            'id', 'name', 'owner', 'amount', 'cycle_duration',
            'created_at', 'current_round', 'is_active',
            'next_payout_date', 'members', 'payouts'
        ]


class CreateEqubGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = EqubGroup
        fields = ['name', 'amount', 'cycle_duration']


class JoinGroupSerializer(serializers.Serializer):
    group_id = serializers.IntegerField()


class MakePaymentSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)