from django.contrib import admin
from .models import Choice, Question

# Inline for Choices in the Question admin
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

# Admin customization for Question model
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]

# Register the admin class with the Question model
admin.site.register(Question, QuestionAdmin)
