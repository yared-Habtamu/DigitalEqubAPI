from django.shortcuts import get_object_or_404, render
from rest_framework import generics, permissions, status
from django.shortcuts import get_object_or_404
from .models import EqubGroup, Membership, Payout
from rest_framework.permissions import IsAdminUser

from .serializers import (
    EqubGroupSerializer,
    CreateEqubGroupSerializer,
    JoinGroupSerializer,
    MakePaymentSerializer
)

from datetime import datetime, timedelta


class CreateEqubGroupView(generics.CreateAPIView):
    serializer_class = CreateEqubGroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        group = serializer.save(owner=self.request.user)
        # Auto-add owner as first member
        Membership.objects.create(
            user=self.request.user,
            group=group,
            payout_order=1
        )


from rest_framework.response import Response


class AdminGroupList(generics.ListAPIView):
    queryset = EqubGroup.objects.all()
    serializer_class = EqubGroupSerializer
    permission_classes = [IsAdminUser]


class JoinEqubGroupView(generics.CreateAPIView):
    serializer_class = JoinGroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group = get_object_or_404(EqubGroup, id=serializer.validated_data['group_id'])

        if Membership.objects.filter(user=request.user, group=group).exists():
            return Response(
                {"detail": "You are already a member of this group"},
                status=status.HTTP_400_BAD_REQUEST
            )

        last_member = Membership.objects.filter(group=group).order_by('-payout_order').first()
        payout_order = (last_member.payout_order + 1) if last_member else 1

        Membership.objects.create(
            user=request.user,
            group=group,
            payout_order=payout_order
        )

        return Response(
            {"detail": "Successfully joined the group"},
            status=status.HTTP_201_CREATED
        )


class MakePaymentView(generics.CreateAPIView):
    serializer_class = MakePaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        group = get_object_or_404(EqubGroup, id=self.kwargs['pk'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # In a real implementation this would process an actual payment but for now we only record pauments

        amount = serializer.validated_data['amount']

        # Verify payment amount matches group requirement
        if amount != group.amount:
            return Response(
                {"detail": f"Payment amount must be {group.amount}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # to check if user is a member
        membership = get_object_or_404(Membership, user=request.user, group=group
                                       )

        # Check if user has already paid for this round
        # (Implementation depends on your payment tracking system)

        return Response(
            {"detail": "Payment simulated successfully"},
            status=status.HTTP_201_CREATED
        )


class RotatePayoutView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        group = get_object_or_404(EqubGroup, id=self.kwargs['pk'])

        # Verify request user is the group owner
        if request.user != group.owner:
            return Response(
                {"detail": "Only the group owner can rotate payouts"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Get next recipient in rotation
        next_recipient = Membership.objects.filter(
            group=group,
            has_received_payout=False
        ).order_by('payout_order').first()

        if not next_recipient:
            return Response(
                {"detail": "All members have received payouts for this cycle"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create payout record
        payout = Payout.objects.create(
            group=group,
            recipient=next_recipient.user,
            amount=group.amount * (group.members.count() - 1),  # Total contributions
            round_number=group.current_round
        )

        # Update membership status
        next_recipient.has_received_payout = True
        next_recipient.save()

        # Update group round and next payout date
        if Membership.objects.filter(group=group, has_received_payout=False).count() == 0:
            # All members have been paid, start new round
            group.current_round += 1
            Membership.objects.filter(group=group).update(has_received_payout=False)

        # Set next payout date based on cycle duration
        if group.cycle_duration == 'WEEKLY':
            group.next_payout_date = datetime.now() + timedelta(weeks=1)
        elif group.cycle_duration == 'BIWEEKLY':
            group.next_payout_date = datetime.now() + timedelta(weeks=2)
        else:  # MONTHLY
            group.next_payout_date = datetime.now() + timedelta(days=30)

        group.save()

        return Response(
            {"detail": f"Payout completed for round {payout.round_number}"},
            status=status.HTTP_201_CREATED
        )


class GroupDetailView(generics.RetrieveAPIView):
    serializer_class = EqubGroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = EqubGroup.objects.all()


class GroupLedgerView(generics.RetrieveAPIView):
    serializer_class = EqubGroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = EqubGroup.objects.all()


# groups/views.py
def group_detail(request, group_id):
    group = get_object_or_404(EqubGroup, id=group_id)
    return render(request, 'groups/group_detail.html', {
        'group': group  # Critical for the template
    })
