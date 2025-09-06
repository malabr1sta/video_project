from django.contrib import admin
from videos import models as videos_models


@admin.register(videos_models.VideoFile)
class VideoFileAdmin(admin.ModelAdmin):
    list_display = ["id", "video", "quality", "file", "created_at"]
    list_filter = ["quality"]
    search_fields = ["video__name"]
    autocomplete_fields = ["video"]


class VideoFileInline(admin.TabularInline):
    model = videos_models.VideoFile
    extra = 1


@admin.register(videos_models.Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "owner",
                    "is_published", "total_likes", "created_at"]
    list_filter = ["is_published", "created_at"]
    search_fields = ["name", "owner__username"]
    autocomplete_fields = ["owner"]
    inlines = [VideoFileInline]


@admin.register(videos_models.Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ["id", "video", "user", "created_at"]
    search_fields = ["video__name", "user__username"]
    autocomplete_fields = ["video", "user"]
