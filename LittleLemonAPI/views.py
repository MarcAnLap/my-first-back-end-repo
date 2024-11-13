from rest_framework import generics
from .models import MenuItem, Category, Order, Cart
from .serializers import MenuItemSerializer, CategorySerializer, OrderSerializer, CartSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import UserRateThrottle
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, throttle_classes
from rest_framework.permissions import AllowAny


# class MenuItemsView(generics.ListCreateAPIView):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price', 'inventory']
    filterset_fields = ['price', 'inventory']
    search_fields = ['category__title']
    # permission_classes = [AllowAny]
    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [AllowAny()]
    #     return [IsAuthenticated()]

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
# from rest_framework import generics
# from .models import MenuItem, Category
# from .serializers import MenuItemSerializer, CategorySerializer

# class CategoriesView(generics.ListCreateAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer

# class MenuItemsView(generics.ListCreateAPIView):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer
#     ordering_fields = ['price', 'inventory']
#     filterset_fields = ['price', 'inventory']
#     search_fields = ['category__title']

# Function-based view with @api_view decorator
@api_view(['GET'])
@permission_classes({IsAuthenticated})
def secret(request):
    return Response({"message": "Some secret message"})

@api_view(['GET'])
@permission_classes({IsAuthenticated})
def manager_view(request):
    if request.user.groups.filter(name='Manager').exists():
        return Response({"message": "Only manager should see this"})
    else:
        return Response({"message": "You are not authorized"},403)
    
@api_view(['GET'])
@permission_classes([AllowAny]) 
@throttle_classes([AnonRateThrottle])
def throttle_check_anon(request):
    return Response({"message":"successful"})

@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
@throttle_classes([UserRateThrottle])
def throttle_check_user(request):
    return Response({"message":"message for the logged in users only"})

# Function-based view for the api coursera activity

from django.contrib.auth.models import Group, Permission
from rest_framework.permissions import BasePermission

def setup_groups():
    admin_group, _ = Group.objects.get_or_create(name='Admin')
    manager_group, _ = Group.objects.get_or_create(name='Manager')
    delivery_group, _ = Group.objects.get_or_create(name='DeliveryTeam')
    customer_group, _ = Group.objects.get_or_create(name='Customer')
    
    # Assign permissions as required (adjust this based on your model permissions)
    # Example: Assign 'add_menuitem' permission to Admin group
    add_menuitem_permission = Permission.objects.get(codename='add_menuitem')
    admin_group.permissions.add(add_menuitem_permission)
    # Add other necessary permissions similarly

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Admin").exists()

class IsManagerUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Manager").exists()

class IsDeliveryUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="DeliveryTeam").exists()
    
# from rest_framework import generics
# from .models import MenuItem, Category, Order, Cart
# from .serializers import MenuItemSerializer, CategorySerializer, OrderSerializer, CartSerializer
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.decorators import api_view, permission_classes

# 3. Admin - Add Menu Items
class MenuItemCreateView(generics.CreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

# 4. Admin - Add Categories
class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

# 5. Managers - Login (handled via Django default authentication)

# 6. Managers - Update 'featured' item of the day
class UpdateFeaturedItemView(generics.UpdateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated, IsManagerUser]
    
    def perform_update(self, serializer):
        serializer.save(featured=True)

# 8. Managers - Assign Orders to Delivery Team
class AssignOrderToDeliveryView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsManagerUser]

    def perform_update(self, serializer):
        delivery_user_id = self.request.data.get('delivery_crew_id')
        serializer.save(delivery_crew_id=delivery_user_id)

# 9. Delivery Team - View Assigned Orders
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsDeliveryUser])
def delivery_team_orders(request):
    orders = Order.objects.filter(delivery_crew=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

# 10. Delivery Team - Update Delivered Orders
class UpdateOrderStatusView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsDeliveryUser]

    def perform_update(self, serializer):
        serializer.save(status=True)  # Assuming status=True means delivered

from rest_framework import viewsets

# 13. Customers - View all Categories
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

# 14. Customers - View all Menu Items
class MenuItemListView(generics.ListAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]
    ordering_fields = ['price']  # 17. Allow sorting by price
    filterset_fields = ['category']  # 15. Filter by category
    pagination_class = None  # 16. Pagination could be added here

# 18. Customers - Add items to Cart

class AddToCartView(generics.CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# 20. Customers - Place Order
class PlaceOrderView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


