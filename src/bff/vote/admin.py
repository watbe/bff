from django.contrib import admin
from bff.vote.models import Vote, Meal, Menu, Category, VoteEvent

class InlineMealAdmin(admin.StackedInline):
    model = Meal

class MenuAdmin(admin.ModelAdmin):
    inlines = [
        InlineMealAdmin,
    ]
    list_filter = ('date',)

class MealAdmin(admin.ModelAdmin):

    search_fields = ('name',)
    list_filter = ('categories__name',)

admin.site.register(Menu, MenuAdmin)
admin.site.register(Meal, MealAdmin)
admin.site.register(Vote)
admin.site.register(Category)
admin.site.register(VoteEvent)
