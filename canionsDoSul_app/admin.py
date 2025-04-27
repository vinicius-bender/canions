from django.contrib import admin

# Register your models here.
from .models import (
    User,
    Specialist,
    Scientist,
    Family,
    Genus,
    Species,
    Localization,
    Media,
    Observation,
    ObservationMedia
)

admin.site.register(User)
admin.site.register(Specialist)
admin.site.register(Scientist)
admin.site.register(Family)
admin.site.register(Genus)
admin.site.register(Species)
admin.site.register(Localization)
admin.site.register(Media)
admin.site.register(Observation)
admin.site.register(ObservationMedia)