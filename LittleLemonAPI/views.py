from rest_framework import generics
from .models import MenuItem
from .serializers import MenuItemSerializer

# class MenuItemsView(generics.ListCreateAPIView):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price', 'inventory']
    filterset_fields = ['price', 'inventory']
    search_fields = ['title']

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

