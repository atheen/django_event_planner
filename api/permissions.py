from rest_framework.permissions import BasePermission

class IsPlanner(BasePermission):
    message = "This isn't your event....."

    def has_object_permission(self, request, view, obj):
        if obj.planner == request.user:
            return True
        else:
            return False
