from django.db import models

class Slider(models.Model):
    topic = models.CharField(max_length=255, verbose_name="Topic")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    button_text = models.CharField(max_length=50, blank=True, null=True, verbose_name="Button Text")
    button_url = models.URLField(blank=True, null=True, verbose_name="Button URL")

    def __str__(self):
        return self.topic

    class Meta:
        verbose_name = "Slider"
        verbose_name_plural = "Sliders"

class SiteSettings(models.Model):
    title = models.CharField(max_length=255, verbose_name="Site Title")
    site_name = models.CharField(max_length=255, verbose_name="Site Name")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    favicon = models.ImageField(upload_to='images/favicons/', blank=True, null=True, verbose_name="Favicon")
    logo = models.ImageField(upload_to='images/logos/', blank=True, null=True, verbose_name="Logo")
    banner_img = models.ImageField(upload_to='images/banner', verbose_name="Banner Image")
    footer_text = models.TextField(blank=True, null=True, verbose_name="Footer Text")
    contact_email = models.EmailField(blank=True, null=True, verbose_name="Contact Email")
    sliders = models.ManyToManyField(Slider, blank=True, verbose_name="Slider Content")

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

