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
    """
    Class to handle like and unlike actions for a video by a specific user.

    Attributes:
        user (accounts_models.User): The user performing the action.
        video (videos_models.Video): The video on which the action is performed.
    """
    def __init__(self, user: accounts_models.User, video: videos_models.Video):
        self.user = user
        self.video = video

    def like(self) -> LikeResult:
        """
        Initialize the VideoLikeManager with a user and a video.

        Args:
            accounts_models.User: The user performing the like/unlike action.
            videos_models.Video: The video to be liked or unliked.
        """
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
        """
        Like the video on behalf of the user.

        Creates a Like object if it does not exist. Increments the video's
        total_likes counter atomically to avoid race conditions.

        Returns:
            dict: {
                "obj": Like object if created, None otherwise,
                "created": True if a new Like was created, False otherwise
            }
        """
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
    """
    Computes aggregate statistics of videos grouped by their owners.

    Attributes:
        videos (QuerySet[videos_models.Video]): QuerySet of video objects to
            calculate statistics for.
    """

    def __init__(self, videos: QuerySet[videos_models.Video]):
        self.videos = videos

    def get_stats(self) -> UserQuerySet:
        """
        Get aggregated statistics of total likes grouped by video owners.

        Returns:
            UserQuerySet: Annotated queryset of users with their total likes
            sum, ordered by likes_sum descending.
        """
        return (
                self.videos
                .values(username=F("owner__username"))
                .annotate(likes_sum=Coalesce(Sum("total_likes"), Value(0)))
                .order_by("-likes_sum")
            )


class StatisticsSubquery:
    """
    Computes aggregate statistics of users using a subquery approach.

    Attributes:
        QuerySet[accounts_models.User]: QuerySet of users.
        QuerySet[videos_models.Video]: QuerySet of videos for aggregation.
    """

    def __init__(
        self,
        users: QuerySet[accounts_models.User],
        videos: QuerySet[videos_models.Video],
    ):
        self.users = users
        self.videos = videos


    def get_stats(self) -> UserQuerySet:
        """
        Annotate users with total likes across their videos using a subquery.

        Returns:
            UserQuerySet: Annotated queryset of users with likes_sum, ordered
            descending.
        """
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
