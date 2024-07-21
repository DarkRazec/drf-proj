from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from users.models import User, Payment
from users.serializer import UserSerializer, PaymentSerializer
from users.services import create_stripe_price, create_stripe_session


class UserViewSet(viewsets.ModelViewSet):
    """
        ViewSet for User models
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = []


@extend_schema_view(
    list=extend_schema(
        summary="Get payment list",
    ),
    update=extend_schema(
        summary="Update for existing payment",
    ),
    partial_update=extend_schema(
        summary="Partial update for existing payment",
    ),
    create=extend_schema(
        summary="Creating new payment",
    ),
    retrieve=extend_schema(
        summary="Course detail info",
    ),
    destroy=extend_schema(
        summary="Delete existing course",
    ),
)
class PaymentViewSet(viewsets.ModelViewSet):
    """
        ViewSet for Payment models
    """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    filter_backends = DjangoFilterBackend, OrderingFilter
    filterset_fields = ('course', 'lesson', 'is_card')
    ordering_fields = ('date',)

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        price = create_stripe_price(payment.payment_sum)
        payment.session_id, payment.link = create_stripe_session(price)
        payment.save()
