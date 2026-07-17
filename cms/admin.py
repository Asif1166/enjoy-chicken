from django.contrib import admin
from .models import *
# Register your models here.
class SubMenuInline(admin.TabularInline):
    model = SubMenu
    extra = 1

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('title', 'position', 'link')
    inlines = [SubMenuInline]

@admin.register(SiteSettings)
class SiteSettings(admin.ModelAdmin):
     list_display = [field.name for field in SiteSettings._meta.fields]
      
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Contact._meta.fields]
      

admin.site.register(AboutSection)
admin.site.register(AboutSectionBody)
admin.site.register(Counter)
admin.site.register(TeamMember)
admin.site.register(Service)
admin.site.register(Feedback)
admin.site.register(PhotoGallery)
admin.site.register(Slider)
admin.site.register(Reservation)
admin.site.register(Brand)
admin.site.register(Chef)
admin.site.register(Testimonial)
admin.site.register(VideoGallery)
admin.site.register(SiteInfo)



class OperatingHourInline(admin.TabularInline):
    model = OperatingHour
    extra = 1  # Number of extra empty rows to display
    fields = ['day', 'hours']  # Fields to display
    max_num = 7  # Maximum number of rows to display

@admin.register(OpeningHours)
class OpeningHoursAdmin(admin.ModelAdmin):
    list_display = ['description', 'contact_number']  # Customize list display for OpeningHours
    inlines = [OperatingHourInline]
