from rest_framework import viewsets

from ._mixins import (
    CreateMixin,
    ListMixin,
    RetrieveMixin,
    DestroyMixin,
    UpdateMixin,
)
from ..models import (
    DateTimeValue,
    NumberValue,
    TextValue,
    BooleanValue,
    ChoicesValue,
    Choice,
    Image,
    File,
    ImagesValue,
    FileValue,
    ItemValue
)
from ..serializers import (
    DateTimeValueSerializer,
    NumberValueSerializer,
    TextValueSerializer,
    BooleanValueSerializer,
    ChoicesValueSerializer,
    ChoiceSerializer,
    ImagesValueSerializer,
    FileValueSerializer,
    ImageSerializer,
    FileSerializer,
    ItemValueSerializer
)


class ValueView(
    CreateMixin,
    ListMixin,
    RetrieveMixin,
    DestroyMixin,
    UpdateMixin,
    viewsets.GenericViewSet
):

    lookup_field = 'pk'

    def get_queryset(self):
        return self.queryset


class DateTimeValueView(ValueView):
    model_name = 'DateTimeValue'
    queryset = DateTimeValue.objects.all()
    serializer_class = DateTimeValueSerializer


class NumberValueView(ValueView):
    model_name = 'NumberValue'
    queryset = NumberValue.objects.all()
    serializer_class = NumberValueSerializer


class TextValueView(ValueView):
    model_name = 'TextValue'
    queryset = TextValue.objects.all()
    serializer_class = TextValueSerializer


class BooleanValueView(ValueView):
    model_name = 'BooleanValue'
    queryset = BooleanValue.objects.all()
    serializer_class = BooleanValueSerializer


class ChoicesValueView(ValueView):
    model_name = 'ChoicesValue'
    queryset = ChoicesValue.objects.all()
    serializer_class = ChoicesValueSerializer
    
    
class ChoiceView(ValueView):
    model_name = 'Choice'
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


class ImageView(ValueView):
    model_name = 'Image'
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    
    
class ImagesValueView(ValueView):
    model_name = 'ImagesValue'
    queryset = ImagesValue.objects.all()
    serializer_class = ImagesValueSerializer


class FileView(ValueView):
    model_name = 'File'
    queryset = File.objects.all()
    serializer_class = FileSerializer


class FileValueView(ValueView):
    model_name = 'FileValue'
    queryset = FileValue.objects.all()
    serializer_class = FileValueSerializer


class ItemValueView(ValueView):
    model_name = 'ItemValue'
    queryset = ItemValue.objects.all()
    serializer_class = ItemValueSerializer
