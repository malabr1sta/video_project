from django.db import models
from django.core.exceptions import ValidationError


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    class Meta:
        abstract = True


class Video(BaseModel):
    owner = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="videos"
    )
    is_published = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    total_likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class VideoFile(BaseModel):
    QUALITY_CHOICES = (
        ('HD', '720p'),
        ('FHD', '1080p'),
        ('UHD', '4K'),
    )
    video = models.ForeignKey(
        "videos.Video",
        on_delete=models.CASCADE,
        related_name='files'
    )
    file = models.FileField(upload_to='videos/')
    quality = models.CharField(max_length=3, choices=QUALITY_CHOICES)

    def __str__(self):
        return f"{self.video.name} [{self.quality}]"


class Like(BaseModel):
    video = models.ForeignKey(
        "videos.Video",
        on_delete=models.CASCADE,
        related_name='likes'
    )
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name='likes'
    )

    class Meta:
        unique_together = ('video', 'user')

    def clean(self):
        if not self.video.is_published:
            raise ValidationError(
                "Cannot add or remove likes for unpublished videos."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

