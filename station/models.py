from django.db import models
from django.utils import timezone
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class Station(models.Model):
    name = models.CharField(max_length=100, verbose_name='駐點')
    address = models.TextField(max_length=200, verbose_name='地址')

    def __str__(self):
        return self.name

class Checkpoint(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE, verbose_name='駐點')
    name = models.CharField(max_length=100, verbose_name='檢查點名稱')
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True)

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)

        # 如果是新對象且沒有 QR Code，則生成 QR Code
        if is_new or not self.qr_code:
            qrcode_data = f'http://127.0.0.1:8000/scan/{self.pk}'
            qrcode_img = qrcode.make(qrcode_data)
            canvas = Image.new('RGB', (290, 290), 'white')
            draw = ImageDraw.Draw(canvas)
            canvas.paste(qrcode_img)
            fname = f'qr_code-{self.name}-{self.pk}.png'
            buffer = BytesIO()
            canvas.save(buffer, 'PNG')
            self.qr_code.save(fname, File(buffer), save=False)
            canvas.close()
            super().save(*args, **kwargs)  # 再次保存以更新 qr_code 字段

    def __str__(self):
        return self.name

class Checkin(models.Model):
    checkpoint = models.ForeignKey(Checkpoint, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.checkpoint.name} - {self.timestamp}'


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_normal', False)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_normal = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
