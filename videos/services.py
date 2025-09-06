from typing import TypedDict, Optional
from django.db import transaction, IntegrityError
from django.db.models import F, Value
from django.db.models import QuerySet
from django.db.models import Sum, Subquery, OuterRef
from django.db.models.functions import Coalesce

from accounts import models as accounts_models
from videos import models as videos_models


class LikeResult(TypedDict):
    obj: Optional["videos_models.Like"]
    created: bool


class UnlikeResult(TypedDict):
    obj: Optional["videos_models.Like"]
    deleted: bool


UserQuerySet = QuerySet[accounts_models.User]


class VideoLikeManager:

    def __init__(self, user: accounts_models.User, video: videos_models.Video):
        self.user = user
        self.video = video

    def like(self) -> LikeResult:
        try:
            with transaction.atomic():
                like, created = videos_models.Like.objects.get_or_create(
                    video=self.video,
                    user=self.user
                )
                if created:
                    videos_models.Video.objects.filter(
                        id=self.video.id
                    ).update(total_likes=F('total_likes') + 1)

            return {"obj": like, "created": created}

        except IntegrityError:
            return {"obj": None, "created": False}

    def unlike(self) -> UnlikeResult:
        try:
            with transaction.atomic():
                deleted, _ = videos_models.Like.objects.filter(
                    video=self.video, user=self.user
                ).delete()

                if deleted:
                    videos_models.Video.objects.filter(
                        id=self.video.id).update(
                        total_likes=F('total_likes') - 1)
            return {"obj": None, "deleted": deleted}
        except IntegrityError:
            return {"obj": None, "deleted": False}


class StatisticsGroupBy:

    def __init__(self, videos: QuerySet[videos_models.Video]):
        self.videos = videos

    def get_stats(self) -> UserQuerySet:
        return (
                self.videos
                .values(username=F("owner__username"))
                .annotate(likes_sum=Coalesce(Sum("total_likes"), Value(0)))
                .order_by("-likes_sum")
            )


class StatisticsSubquery:

    def __init__(
        self,
        users: QuerySet[accounts_models.User],
        videos: QuerySet[videos_models.Video],
    ):
        self.users = users
        self.videos = videos


    def get_stats(self) -> UserQuerySet:
        subquery = Subquery(
            self.videos
            .filter(owner_id=OuterRef('pk'))
            .values('owner_id')
            .annotate(likes_sum=Sum('total_likes'))
            .values('likes_sum')
        )
        return (
            self.users
            .annotate(likes_sum=Coalesce(subquery, 0))
            .order_by('-likes_sum')
        )
