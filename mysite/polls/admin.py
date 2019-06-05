from django.contrib import admin
from .models import Question, Choice

# Register your models here.


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):

    """group fields in fieldsets"""
    fieldsets = [
        (None,  {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]

    """add to Question add/modify form a foreignkey view and edit"""
    inlines = [ChoiceInline]

    """change default display of Question objects"""
    list_display = ('question_text', 'pub_date', 'was_published_recently')

    """add simple filter by pub_date"""
    list_filter = ['pub_date']

    """add simple search field in top of site, search in question_text"""
    search_fields = ['question_text']

    """simple pagination"""
    list_per_page = 5

admin.site.register(Question, QuestionAdmin)