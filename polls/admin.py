from django.contrib import admin, messages
from django.shortcuts import get_object_or_404

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

    def has_add_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

    readonly = ['commit_hash', 'committer', 'email', 'date', 'message']
     
admin.site.register(Commit, CommitAdmin)

@admin.action(description="Set selected branch as active")
def set_active(modeladmin, request, queryset):
    if queryset.count() != 1:
        messages.error(request, "Error: More than one branch selected.")
        return
    request.session['active_branch'] = queryset[0].name

@admin.action(description="Merge selected branch into active branch")
def merge(modeladmin, request, queryset):
    if queryset.count() != 1:
        messages.error(request, "Error: More than one branch selected.")
        return
    
    active_branch_name = request.session.get('active_branch')
    merge_branch_name = queryset[0].name
    if ( merge_branch_name == active_branch_name ):
        messages.error(request, "Error: Select a branch that is not active to merge.")
        return
    
    base_branch = get_object_or_404(Branch, name=active_branch_name)
    base_branch.merge(merge_branch_name)

    success_message = 'Successfully Merged ' + merge_branch_name + ' branch into ' + active_branch_name + ' branch'
    
    messages.add_message(request, messages.INFO, success_message)
    
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    actions = [set_active, merge]
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def get_readonly_fields(self, request, obj=None):
        if obj: # obj is not None, so this is an edit
            return ['name', 'hash', 'latest_committer', 'latest_committer_email', 'latest_commit_date', 'latest_commit_message']
        else: # This is an addition
            return ['hash', 'latest_committer', 'latest_committer_email', 'latest_commit_date', 'latest_commit_message']

admin.site.register(Branch, BranchAdmin)
