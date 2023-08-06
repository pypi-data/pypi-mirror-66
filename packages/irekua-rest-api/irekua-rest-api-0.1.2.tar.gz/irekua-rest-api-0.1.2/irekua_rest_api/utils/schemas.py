from rest_framework.schemas import AutoSchema


class CustomSchema(AutoSchema):
    def _allows_filters(self, path, method):
        if method.lower() != 'get':
            return False

        if getattr(self.view, 'filter_backends', None) is None:
            return False

        if hasattr(self.view, 'action'):
            if self.view.action in ["retrieve", "update", "partial_update", "destroy"]:
                return False

            if self.view.action == 'list':
                return True

            return self.view.action[-1] == 's'

        return False
