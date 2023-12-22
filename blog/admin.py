from django.contrib import admin
from users.models import User
from .models import Story, Category, Tag, Profile,Collection, Comments, Profiles

# Register your models here.

class StoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("story_heading",)}
    list_filter = ("story_heading", "story_category", "date")
    list_display = ("story_heading", "author")

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("category_name",)}
    list_filter = ("category_name", "date")
    list_display = ("category_name", )

#class ProfileInline(admin.StackedInline):
#    model = UserProfile
#
#class UserAdmin(admin.ModelAdmin):
#    model = User
#    inlines = [ProfileInline]

#admin.site.unregister(User)


admin.site.register(Story, StoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag)
admin.site.register(Profile)
#admin.site.register(User, UserAdmin)
admin.site.register(Profiles)
admin.site.register(Collection)
admin.site.register(Comments)