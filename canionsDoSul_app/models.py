from django.db import models

class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username


class Specialist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'specialist'

    def __str__(self):
        return f"Specialist: {self.user.username}"


class Scientist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'scientist'

    def __str__(self):
        return f"Scientist: {self.user.username}"


class Family(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'family'

    def __str__(self):
        return self.name


class Genus(models.Model):
    name = models.CharField(max_length=255)
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'genus'

    def __str__(self):
        return self.name


class Species(models.Model):
    scientific_name = models.CharField(max_length=255)
    popular_name = models.CharField(max_length=255)
    habitat = models.CharField(max_length=255)
    genus = models.ForeignKey(Genus, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'species'

    def __str__(self):
        return self.popular_name


class Localization(models.Model):
    city_name = models.CharField(max_length=255)
    state_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'localization'

    def __str__(self):
        return f"{self.city_name}, {self.state_name}"


class Media(models.Model):
    name = models.CharField(max_length=255)
    path = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'media'

    def __str__(self):
        return self.name


class Observation(models.Model):
    longitude = models.DecimalField(max_digits=10, decimal_places=8)
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    species = models.ForeignKey(Species, on_delete=models.CASCADE)
    localization = models.ForeignKey(Localization, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)

    class Meta:
        db_table = 'observation'

    def __str__(self):
        return f"Observation {self.id} - {self.species.popular_name}"


class ObservationMedia(models.Model):
    observation = models.ForeignKey(Observation, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)

    class Meta:
        db_table = 'observation_media'

    def __str__(self):
        return f"Observation {self.observation.id} - Media {self.media.name}"
