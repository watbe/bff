from django.contrib import admin
from bff.vote.models import Vote, Meal, Menu, Category, VoteEvent

class InlineMealAdmin(admin.StackedInline):
    model = Meal

class MenuAdmin(admin.ModelAdmin):
    inlines = [
        InlineMealAdmin,
    ]

admin.site.register(Menu, MenuAdmin)
admin.site.register(Meal)
admin.site.register(Vote)
admin.site.register(Category)
admin.site.register(VoteEvent)