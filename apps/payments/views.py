from rest_framework import viewsets, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import Payment
from .serializers import PaymentSerializer, PaymentCreateSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser) # Allow file uploads
    
    def get_queryset(self):
        # Users see their own payments
        return Payment.objects.filter(order__user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PaymentCreateSerializer
        return PaymentSerializer

    def perform_create(self, serializer):
        payment = serializer.save()
        
        # Send payment pending email
        from apps.core.utils.emails import send_html_email
        send_html_email(
            subject=f"Comprobante recibido - Orden #{payment.order.id}",
            template_name="emails/payment_pending.html",
            context={"payment": payment},
            to_email=self.request.user.email
        )
