from rest_framework import generics
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from django.shortcuts import get_object_or_404
from django.utils.html import escape
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Payment
from .services import MockChapa
from groups.models import Membership, EqubGroup


# Custom throttle class
class PaymentThrottle(UserRateThrottle):
    scope = 'payment'


class PaymentView(generics.CreateAPIView):
    throttle_classes = [PaymentThrottle]

    def post(self, request, group_id):
        # Sanitize and validate group_id
        group_id = escape(str(group_id))
        try:
            group_id = int(group_id)
        except ValueError:
            return Response({"error": "Invalid group ID"}, status=400)

        user = request.user
        group = get_object_or_404(EqubGroup, id=group_id)

        # Validate membership
        if not Membership.objects.filter(user=user, group=group).exists():
            return Response({"error": "Not a group member"}, status=400)

        # Check if already paid
        if Payment.objects.filter(user=user, group=group, round_number=group.current_round).exists():
            return Response({"error": "Already paid this round"}, status=400)

        # Simulate payment via Chapa
        result = MockChapa.process_payment(group.amount)
        status_str = 'success' if result['success'] else 'failed'

        # Save payment record
        Payment.objects.create(
            user=user,
            group=group,
            amount=group.amount,
            status=status_str,
            round_number=group.current_round
        )

        # WebSocket notification (non-blocking)
        if result['success']:
            try:
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f'payouts_{group_id}',
                    {
                        'type': 'payout_notification',
                        'data': {
                            'type': 'payment',
                            'user': user.email,
                            'amount': group.amount,
                            'status': status_str,
                            'round': group.current_round
                        }
                    }
                )
            except Exception as e:
                print("WebSocket notification failed:", str(e))  # Log, don't break flow

        return Response({
            "status": status_str,
            "message": result['message']
        }, status=201 if result['success'] else 400)
