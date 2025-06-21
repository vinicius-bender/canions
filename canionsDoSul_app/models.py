from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import os

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, role="default"):
        if not email:
            raise ValueError("O email é obrigatório")
        if not username:
            raise ValueError("O nome de usuário é obrigatório")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username=username, email=email, password=password, role="admin")
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

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
    habitat = models.CharField(max_length=2000)
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
    country_name = models.CharField(max_length=255, default='Brasil')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'localization'

    def __str__(self):
        return f"{self.city_name}, {self.state_name}"


class Media(models.Model):
    name = models.CharField(max_length=255)
    # image = models.ImageField(upload_to='observations/')  # Usar ImageField para imagens
    files = models.FileField(upload_to='observations/', default='default.jpg')  # Suporta imagens e vídeos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_image(self):
        ext = os.path.splitext(self.files.name)[1].lower()
        # return self.files.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.jfif', '.webp'))
        return ext in  ['.png', '.jpg', '.jpeg', '.gif', '.jfif', '.webp']

    def is_video(self):
        ext = os.path.splitext(self.files.name)[1].lower()
        # return self.files.name.lower().endswith(('.mp4', '.mov', '.webm', '.mkv'))
        return ext in ['.mp4', '.mov', '.webm', '.mkv']
    
    class Meta:
        db_table = 'media'
    
    def __str__(self):
        return self.name

class Observation(models.Model):
    longitude = models.DecimalField(max_digits=10, decimal_places=8)
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    species = models.ForeignKey(Species, on_delete=models.CASCADE, null=True, blank=True)  # <- permite null
    localization = models.ForeignKey(Localization, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, default="pendente")  # <- default
    medias = models.ManyToManyField(Media, through='ObservationMedia')

    class Meta:
        db_table = 'observation'

    def __str__(self):
        return f"Observation {self.id} - {self.species.popular_name if self.species else 'Sem espécie'}"

class ObservationMedia(models.Model):
    observation = models.ForeignKey(Observation, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'observation_media'
    
    def __str__(self):
        return f"Observation {self.observation.id} - Media {self.media.name}"
