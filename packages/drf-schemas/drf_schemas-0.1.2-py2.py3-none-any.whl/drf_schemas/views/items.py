from rest_framework import viewsets

from ._mixins import (
    CreateMixin,
    ListMixin,
    RetrieveMixin,
    DestroyMixin,
    UpdateMixin,
)
from ..models import (
    Item,
    ItemSchema,
    Category
)
from ..serializers import (
    ItemSerializer,
    ItemSchemaSerializer,
    CategorySerializer,
    ItemFilterSerializer
)


class ItemView(
    CreateMixin,
    ListMixin,
    RetrieveMixin,
    DestroyMixin,
    UpdateMixin,
    viewsets.GenericViewSet
):

    lookup_field = 'pk'
    model_name = 'Item'
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_queryset(self):
        queryset = self.queryset
        params = self.request.query_params

        if len(params):
            serializer = ItemFilterSerializer(
                data=params.dict(),
                context={'request': self.request}
            )
            serializer.is_valid(raise_exception=True)

            params = serializer.data
            order_by = params.pop('order_by', '')
            queryset = queryset.filter(**params)

            if order_by:
                queryset = queryset.order_by(order_by)

        return queryset


class CategoryView(
    CreateMixin,
    ListMixin,
    RetrieveMixin,
    DestroyMixin,
    UpdateMixin,
    viewsets.GenericViewSet
):

    lookup_field = 'pk'
    model_name = 'Category'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = self.queryset

        name = self.request.query_params.get('name', '')
        if name:
            queryset = queryset.filter(name__icontains=name)

        order_by = self.request.query_params.get('order_by', '')
        if order_by in ['name', 'created_at', 'updated_at']:
            queryset = queryset.order_by(order_by)

        return queryset


class ItemSchemaView(ItemView):

    model_name = 'ItemSchema'
    queryset = ItemSchema.objects.all()
    serializer_class = ItemSchemaSerializer

    def get_queryset(self):
        queryset = self.queryset

        name = self.request.query_params.get('name', '')
        if name:
            queryset = queryset.filter(name__icontains=name)

        order_by = self.request.query_params.get('order_by', '')
        if order_by in ['name', 'created_at', 'updated_at']:
            queryset = queryset.order_by(order_by)

        return queryset

