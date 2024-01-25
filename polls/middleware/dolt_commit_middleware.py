from django.db.models.signals import m2m_changed, post_save, pre_delete
from django.db import connection

class AutoDoltCommit:
    def __init__(self, request):
        self.request = request
        self.commit = False

    def __enter__(self):
        # Connect our receivers to the post_save and post_delete signals.
        post_save.connect(self._handle_update, dispatch_uid="dolt_commit_update")
        m2m_changed.connect(self._handle_update, dispatch_uid="dolt_commit_update")
        pre_delete.connect(self._handle_delete, dispatch_uid="dolt_commit_delete")

    def __exit__(self, type, value, traceback):
        if self.commit:
            self._commit()

        # Disconnect change logging signals. This is necessary to avoid recording any errant
        # changes during test cleanup.
        post_save.disconnect(self._handle_update, dispatch_uid="dolt_commit_update")
        m2m_changed.disconnect(self._handle_update, dispatch_uid="dolt_commit_update")
        pre_delete.disconnect(self._handle_delete, dispatch_uid="dolt_commit_delete")

    def _handle_update(self, sender, instance, **kwargs):
        """
        Fires when an object is created or updated.
        """
        self.commit = True

    def _handle_delete(self, sender, instance, **kwargs):
        """
        Fires when an object is deleted.
        """
        self.commit = True

    def _commit(self):
        message = "Modified database in Django. Creating Dolt Commit."
        with connection.cursor() as cursor:
            cursor.execute("CALL DOLT_COMMIT('-Am', '" + message + "')")

class DoltAutoCommitMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process the request with auto-dolt-commit enabled
        with AutoDoltCommit(request):
            return self.get_response(request)

