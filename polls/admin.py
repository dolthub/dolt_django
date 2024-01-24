from django.contrib import admin

from .models import Choice, Question, Branch, Commit


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]

    list_display = ["question_text", "pub_date", "was_published_recently"]

    list_filter = ["pub_date"]


admin.site.register(Question, QuestionAdmin)

class CommitAdmin(admin.ModelAdmin):
    list_display = ['commit_hash', 'committer', 'date', 'message']
    
    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    readonly = ['commit_hash', 'committer', 'email', 'date', 'message']

admin.site.register(Commit, CommitAdmin)
    
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def get_readonly_fields(self, request, obj=None):
        if obj: # obj is not None, so this is an edit
            return ['name', 'hash', 'latest_committer', 'latest_committer_email', 'latest_commit_date', 'latest_commit_message']
        else: # This is an addition
            return ['hash', 'latest_committer', 'latest_committer_email', 'latest_commit_date', 'latest_commit_message']
    
admin.site.register(Branch, BranchAdmin)
