from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Post(models.Model):
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    author = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    resume = models.TextField(max_length=255)
    content = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='posts')
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    number_of_comments = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def like_count(self):
        return self.likes
    
    def dislike_count(self):
        return self.dislikes
    
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    content = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    def __str__(self):
        return f'Comment by {self.name} on {self.post.title}'
    
class Category(models.Model):
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('Email is required'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'administrator')

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)
        
class User(AbstractUser):
    image = models.ImageField(upload_to='users/', blank=True, null=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    birth_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='store_user_groups',
        blank=True,
        verbose_name=_('groups'),
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='store_user_permissions',
        blank=True,
        verbose_name=_('user permissions'),
        help_text=_('Specific permissions for this user.'),
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'birth_date']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['name']

    def __str__(self):
        return self.name
    
class Phone(models.Model):
    PHONE_TYPES = [
        ('mobile', _('Mobile')),
        ('home', _('Home')),
        ('work', _('Work')),
    ]

    DDD_TYPES = [
        ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'),
        ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('21', '21'),
        ('22', '22'), ('24', '24'), ('27', '27'), ('28', '28'), ('31', '31'),
        ('32', '32'), ('33', '33'), ('34', '34'), ('35', '35'), ('37', '37'),
        ('38', '38'), ('41', '41'), ('42', '42'), ('43', '43'), ('44', '44'),
        ('45', '45'), ('46', '46'), ('47', '47'), ('48', '48'), ('49', '49'),
        ('51', '51'), ('53', '53'), ('54', '54'), ('55', '55'), ('61', '61'),
        ('62', '62'), ('63', '63'), ('64', '64'), ('65', '65'), ('66', '66'),
        ('67', '67'), ('68', '68'), ('69', '69'), ('71', '71'), ('73', '73'),
        ('74', '74'), ('75', '75'), ('77', '77'), ('79', '79'), ('81', '81'),
        ('82', '82'), ('83', '83'), ('84', '84'), ('85', '85'), ('86', '86'),
        ('87', '87'), ('88', '88'), ('89', '89'), ('91', '91'), ('92', '92'),
        ('93', '93'), ('94', '94'), ('95', '95'), ('96', '96'), ('97', '97'),
        ('98', '98'), ('99', '99')
    ]    
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='phones')
    number = models.CharField(max_length=20)
    ddd = models.CharField(max_length=2, choices=DDD_TYPES)
    type = models.CharField(max_length=6, choices=PHONE_TYPES)

    class Meta:
        verbose_name = _('Phone')
        verbose_name_plural = _('Phones')

    def __str__(self):
        return f'{self.get_type_display()}: ({self.ddd}) {self.number}'

    def clean(self):
        if not self.number.isdigit():
            raise ValidationError(_('Phone number must contain only digits'))