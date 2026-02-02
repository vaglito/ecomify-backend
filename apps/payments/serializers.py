from rest_framework import serializers
from .models import Payment, Order

class PaymentCreateSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Payment
        fields = ['order_id', 'transaction_code', 'payment_proof']

    def validate_order_id(self, value):
        user = self.context['request'].user
        try:
            order = Order.objects.get(id=value, user=user)
        except Order.DoesNotExist:
            raise serializers.ValidationError("Orden no encontrada o no pertenece al usuario.")
        
        if hasattr(order, 'payment'):
            raise serializers.ValidationError("Esta orden ya tiene un pago registrado.")
            
        return value

    def create(self, validated_data):
        order_id = validated_data.pop('order_id')
        order = Order.objects.get(id=order_id)
        
        # Determine amount from order total
        amount = order.total_amount
        
        payment = Payment.objects.create(order=order, amount=amount, **validated_data)
        return payment

class PaymentSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Payment
        fields = ['id', 'order', 'transaction_code', 'payment_proof', 'amount', 'status', 'status_display', 'created_at']
