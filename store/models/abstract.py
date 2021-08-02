from django.db import models 


class DateTimeTracker(models.Model):
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    created_time = models.TimeField(auto_now_add=True)
    updated_time = models.TimeField(auto_now=True)

    class Meta:
        abstract = True

color_choices = (
    ('red','Red'),
    ('green','Green'),
    ('yellow','Yellow'),
    ('blue','Blue'),
    ('white','White'),
    ('black','Black'),
    ('maroon','Maroon'),
    ('cyan','Cyan')
)

gender_choices = (
    ('male','Male'),
    ('female','Female')
)
size_type_choices = (
        ('int','Int'),
        ('string','String'),
        ('eu','EU'),
        ('Chest','Chest')
    )