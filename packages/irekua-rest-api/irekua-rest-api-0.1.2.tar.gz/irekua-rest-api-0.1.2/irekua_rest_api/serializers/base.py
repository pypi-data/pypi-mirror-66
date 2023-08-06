from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import HyperlinkedModelSerializer
from irekua_rest_api.utils.urls import get_detail_view_name


class IrekuaModelSerializer(ModelSerializer):
    def build_url_field(self, field_name, model_class):
        field_class = self.serializer_url_field
        field_kwargs = {'view_name': get_detail_view_name(model_class)}
        return field_class, field_kwargs


class IrekuaHyperlinkedModelSerializer(HyperlinkedModelSerializer):
    def build_url_field(self, field_name, model_class):
        field_class = self.serializer_url_field
        field_kwargs = {'view_name': get_detail_view_name(model_class)}
        return field_class, field_kwargs
