from rest_framework.metadata import SimpleMetadata


class CustomMetadata(SimpleMetadata):
    def determine_actions(self, request, view):
        actions = {}
        for method, action in view.action_map.items():
            if method.lower() == "delete":
                continue

            view.action = action
            serializer = view.get_serializer()
            actions[method.upper()] = self.get_serializer_info(serializer)

        return actions
