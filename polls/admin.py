from django.contrib import admin

from .models import Choice, Question, Branch


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

class BranchAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj: # obj is not None, so this is an edit
            return ['name', 'hash', 'latest_committer', 'latest_committer_email', 'latest_commit_date', 'latest_commit_message']
        else: # This is an addition
            return ['hash', 'latest_committer', 'latest_committer_email', 'latest_commit_date', 'latest_commit_message']
    
admin.site.register(Branch, BranchAdmin)
