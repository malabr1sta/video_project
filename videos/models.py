from django.db import models
from django.core.exceptions import ValidationError


class BaseModel(models.Model):
    """
    Abstract base model that provides timestamp fields for creation and update.

    Attributes:
        created_at (DateTimeField): Timestamp when the object was created,
            automatically set on creation and not editable.
        updated_at (DateTimeField): Timestamp when the object was last updated,
            automatically updated on save and not editable.
    """
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
    """
    Model representing a video uploaded by a user.

    Attributes:
        owner (ForeignKey): Reference to the user who owns the video.
        is_published (BooleanField): Indicates if the video is published.
        name (CharField): Name/title of the video.
        total_likes: Total number of likes the video has received.
    """
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
    """
    Model representing individual video files with different quality options.

    Attributes:
        QUALITY_CHOICES (tuple): Available quality options for the video file.
        video (ForeignKey): Reference to the parent Video object.
        file (FileField): Uploaded video file.
        quality (CharField): Quality of the video file (HD, FHD, UHD).
    """
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
    """
    Model representing a like by a user on a video.

    Attributes:
        video (ForeignKey): Reference to the liked Video object.
        user (ForeignKey): Reference to the User who liked the video.

    Meta:
        unique_together: Ensures a user can like a video only once.
    """
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
        """
        Validate that likes can only be added to published videos.

        Raises:
            ValidationError: If the video is not published.
        """
        if not self.video.is_published:
            raise ValidationError(
                "Cannot add or remove likes for unpublished videos."
            )

    def save(self, *args, **kwargs):
        """
        Validate and save the Like instance.

        Calls full_clean() before saving to enforce validation rules.
        """
        self.full_clean()
        super().save(*args, **kwargs)

