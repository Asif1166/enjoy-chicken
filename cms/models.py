from django.db import models

# Create your models here.
class Menu(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    eng_title = models.CharField(max_length=100, blank=True, null=True)
    position = models.IntegerField()
    link = models.CharField(max_length=200)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title

class SubMenu(models.Model):
    menu = models.ForeignKey(Menu, related_name='submenus', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True, null=True)
    eng_title = models.CharField(max_length=100, blank=True, null=True)
    position = models.IntegerField()
    link = models.CharField(max_length=200)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title
    

class SiteSettings(models.Model):
    is_order = models.BooleanField(default=True)
    is_reservation = models.BooleanField(default=True)
    is_delivery_enabled = models.BooleanField(default=True)
    is_take_away_enabled = models.BooleanField(default=True)
    

class Contact(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.subject}'
    



class AboutSection(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    eng_title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    eng_description = models.TextField(blank=True, null=True)
    button_text = models.CharField(max_length=50, blank=True, null=True)
    eng_button_text = models.CharField(max_length=50, blank=True, null=True)
    button_link = models.CharField(max_length=50, blank=True, null=True)
    main_image = models.ImageField(upload_to='about_us/', blank=True, null=True)
    background_image_1 = models.ImageField(upload_to='about_us/', blank=True, null=True)
    background_image_2 = models.ImageField(upload_to='about_us/', blank=True, null=True)
    
    def __str__(self):
        return self.title
class AboutSectionBody(models.Model):
    title = models.CharField(max_length=255)
    eng_title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    eng_description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='about/')
    checklist = models.TextField()

class Counter(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    eng_title = models.CharField(max_length=255, blank=True, null=True)
    count = models.PositiveIntegerField(blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)

class TeamMember(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    eng_designation = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='team/',blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

class Service(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    eng_title = models.CharField(max_length=255, blank=True, null=True)

    description = models.TextField(blank=True, null=True)
    eng_description = models.TextField(blank=True, null=True)

    icon = models.ImageField(upload_to='service_icons/',blank=True, null=True)

class Feedback(models.Model):
    name = models.CharField(max_length=100,blank=True, null=True)
    eng_name = models.CharField(max_length=100,blank=True, null=True)
    position = models.CharField(max_length=100,blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='feedback/', blank=True, null=True)


class PhotoGallery(models.Model):
    title = models.CharField(max_length=100,blank=True, null=True)
    subtitle = models.CharField(max_length=100,blank=True, null=True)
    image = models.ImageField(upload_to='feedback/', blank=True, null=True)
    position = models.CharField(max_length=100,blank=True, null=True)

class VideoGallery(models.Model):

    video_url = models.TextField(blank=True, null=True)
    position = models.CharField(max_length=100,blank=True, null=True)



class Slider(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    eng_title = models.CharField(max_length=100, blank=True, null=True)
    subtitle = models.CharField(max_length=100, blank=True, null=True)
    eng_subtitle = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    eng_description = models.TextField(blank=True, null=True)
    background_image = models.ImageField(upload_to='section_images/', blank=True, null=True)
    livraison_link = models.CharField(max_length=100,blank=True, null=True)
    emporter_link = models.CharField(max_length=100,blank=True, null=True)
    sur_place_link = models.CharField(max_length=100,blank=True, null=True)
    video_url = models.CharField(max_length=1000,blank=True, null=True)

    def __str__(self):
        return self.title
    
SLOT = (
("11:00-12:00", "11:00-12:00"),
("12:00-13:00", "12:00-13:00"),
("13:00-14:00", "13:00-14:00"),
("14:00-15:00", "14:00-15:00"),
("18:00-19:00", "18:00-19:00"),
("19:00-20:00", "19:00-20:00"),
("21:00-22:00", "21:00-22:00"),
("22:00-23:30", "22:00-23:30"),

)

class Reservation(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    slot = models.CharField(choices=SLOT, max_length=100, default="10:00-11:30")
    total_person = models.IntegerField(blank=True, null=True)
    invoice_slip = models.FileField(upload_to="invoices", blank=True, null=True)
    
    order = models.OneToOneField('shop.CartOrder', on_delete=models.SET_NULL, null=True, blank=True, related_name='reservation')

    status = models.CharField(max_length=10, choices=[(
        'En attente', 'En attente'), ('Réservé', 'Réservé'), ('Rejeté', 'Rejeté')], default='En attente')

    def __str__(self):
        return self.name
    
    @classmethod
    def get_available_seats(cls, date, slot):
        max_seats = 20
        reserved_seats = cls.objects.filter(date=date, slot=slot).aggregate(
            models.Sum('total_person'))['total_person__sum'] or 0
        return max_seats - reserved_seats
    


class Brand(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='brand_logos/')
    link = models.URLField(blank=True, null=True)  # Optional link to partner site

    def __str__(self):
        return self.name
    

class Chef(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='chefs/', blank=True, null=True)

    def __str__(self):
        return self.name or "Unnamed Chef"
    

class OpeningHours(models.Model):
    description = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    image = models.ImageField(upload_to="opening_hours/",blank=True, null=True)

    def __str__(self):
        return self.description or "Opening Hours"

class OperatingHour(models.Model):
    opening_hours = models.ForeignKey(OpeningHours, on_delete=models.CASCADE, related_name="operating_hours")
    day = models.CharField(max_length=20, blank=True, null=True)
    hours = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.day}: {self.hours}"
    

class Testimonial(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    rating = models.IntegerField(default=5)
    provider_name = models.CharField(max_length=255, blank=True, null=True)
    provider_position = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title or "Testimonial"
    


class SiteInfo(models.Model):
    primary_phone = models.CharField(max_length=255, blank=True, null=True)
    secondary_phone = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to="logo/",blank=True, null=True)
    banner = models.ImageField(upload_to="banner/",blank=True, null=True)
    facebook_url = models.CharField(max_length=255, blank=True, null=True)
    youtube_url = models.CharField(max_length=255, blank=True, null=True)
    linkedin_url = models.CharField(max_length=255, blank=True, null=True)
    twitter_url = models.CharField(max_length=255, blank=True, null=True)
    instagram_url = models.CharField(max_length=255, blank=True, null=True)
    snapchat_url = models.CharField(max_length=255, blank=True, null=True)
    pdf_menu = models.FileField(upload_to="menu_pdf/", blank=True, null=True)

    map_location = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name or "SiteInfo"