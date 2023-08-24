from django.contrib.auth import get_user_model
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveDestroyAPIView,
                                     RetrieveUpdateAPIView)
from rest_framework.viewsets import ModelViewSet

from api.serializers import (BrandSerializer, CustomerSerializer,
                             OrderCreateSerializer, OrderSerializer,
                             ProductSerializer)
from shop.models import Brand, Order, Product


class CustomerViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = CustomerSerializer


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductOrdersListView(ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        product_pk = self.kwargs.get("product_pk")
        return Order.objects.filter(products__pk=product_pk)


class ProductOrderDetailView(ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        product_pk = self.kwargs.get("product_pk")
        order_pk = self.kwargs.get("order_pk")
        return Order.objects.filter(products__pk=product_pk, id=order_pk)


class ProductDeleteView(RetrieveDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductUpdateView(RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductCreateView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrdersListView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderDeleteView(RetrieveDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderUpdateView(RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer


class OrderCreateView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer

    def perform_create(self, serializer):
        status = self.request.data.get("status")
        customer_id = self.request.data.get("customer")
        products_id = self.request.data.get("products")

        order = Order.objects.create(
            status=status, customer_id=customer_id, delivery_address=self.request.data.get("delivery_address")
        )

        order.products.set(products_id)


class BrandsListView(ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class BrandDeleteView(RetrieveDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class BrandUpdateView(RetrieveUpdateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class BrandCreateView(CreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
