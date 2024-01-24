from django.db import connection

class DoltBranchMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        with connection.cursor() as cursor:
            branch_name = self.get_branch(request)
            cursor.execute("CALL DOLT_CHECKOUT('" + branch_name + "')")

        response = self.get_response(request)

        return response

    def get_branch(self, request, *view_args, **view_kwargs):
        if "active_branch" in request.session:
            return request.session.get("active_branch")
        return "main"
