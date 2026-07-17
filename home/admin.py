from django.contrib import admin

from home.models import CV, Category
# Register your models here.


admin.site.register(Category)

@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    list_display = ('name', 'category',)
    list_filter = ('category',)