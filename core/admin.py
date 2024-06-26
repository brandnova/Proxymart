from django.contrib import admin
from .models import SiteSettings, Slider

class SliderInline(admin.TabularInline):
    model = SiteSettings.sliders.through
    extra = 1

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('topic', 'description', 'button_text', 'button_url')

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'contact_email')
    inlines = [SliderInline]

    fieldsets = (
        (None, {
            'fields': ('title', 'site_name', 'description', 'favicon', 'logo', 'banner_img', 'footer_text', 'contact_email')
        }),
        ('Slider Content', {
            'classes': ('collapse',),
            'fields': ('sliders',),
        }),
    )
