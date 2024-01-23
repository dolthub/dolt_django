from django.db import connection

class DoltBranchMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        with connection.cursor() as cursor:
            cursor.execute("CALL DOLT_CHECKOUT('test_branch')")

        response = self.get_response(request)

        return response
