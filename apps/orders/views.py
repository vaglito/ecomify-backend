from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderCreateSerializer
from apps.products.models import Product

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Users can only see their own orders
        return Order.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        items_data = serializer.validated_data['items']
        shipping_address = serializer.validated_data['shipping_address']
        phone = serializer.validated_data['phone']
        
        try:
            with transaction.atomic():
                # Calculate total and verify stock
                total_amount = 0
                order_items = []
                
                # Create Order first
                order = Order.objects.create(
                    user=request.user,
                    shipping_address=shipping_address,
                    phone=phone,
                    total_amount=0 # Will update later
                )

                for item in items_data:
                    product_id = item['product_id']
                    quantity = item['quantity']
                    
                    try:
                        product = Product.objects.select_for_update().get(id=product_id)
                    except Product.DoesNotExist:
                        raise ValueError(f"Producto con ID {product_id} no existe.")
                    
                    if product.stock < quantity:
                        raise ValueError(f"Stock insuficiente para {product.name}. Stock actual: {product.stock}")
                    
                    # Deduct stock
                    product.stock -= quantity
                    product.save()
                    
                    price = product.price
                    total_amount += price * quantity
                    
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        price=price
                    )

                # Update Order Total
                order.total_amount = total_amount
                order.save()
                
                # Return the full order representation
                result_serializer = OrderSerializer(order)
                
                # Send order success email
                from apps.core.utils.emails import send_html_email
                send_html_email(
                    subject=f"Confirmación de Pedido #{order.id} - Ecomify",
                    template_name="emails/order_success.html",
                    context={"order": order},
                    to_email=request.user.email
                )
                
                return Response(result_serializer.data, status=status.HTTP_201_CREATED)
                
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Error al procesar la orden."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        
        if order.status in ['shipped', 'delivered', 'cancelled']:
            return Response(
                {"error": f"No se puede cancelar una orden en estado '{order.get_status_display()}'."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            with transaction.atomic():
                # Restore stock for each item
                for item in order.items.all():
                    product = item.product
                    # Use select_for_update inside transaction if possible, but strict locking 
                    # might be overkill here unless high concurrency. 
                    # Simpler to just increment.
                    product.stock += item.quantity
                    product.save()

                order.status = 'cancelled'
                order.save()
        except Exception as e:
            return Response(
                {"error": f"Error al cancelar la orden: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        return Response({"message": "Orden cancelada exitosamente y stock restaurado."}, status=status.HTTP_200_OK)
