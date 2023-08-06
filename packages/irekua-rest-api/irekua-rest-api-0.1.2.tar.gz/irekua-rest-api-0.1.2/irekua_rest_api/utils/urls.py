from irekua_rest_api.apps import IrekuaRestApiConfig


def get_detail_view_name(model_class):
    return '{app_name}:{model_name}-detail'.format(
        app_name=IrekuaRestApiConfig.name,
        model_name=model_class._meta.object_name.lower())
