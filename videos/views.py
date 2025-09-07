from rest_framework import generics, status, mixins, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import F, Q, Sum, Subquery, OuterRef
from django.db import transaction, IntegrityError
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from accounts import models as accounts_models
from videos import (
    models as videos_models,
    permissions as videos_permissions,
    serializers as videos_serializers,
    services as videos_services
)


class VideoView(viewsets.ReadOnlyModelViewSet):
    """
    Read-only viewset for listing and retrieving videos.

    Permissions:
        - Staff users can see all videos.
        - Authenticated users can see published videos or their own videos.
        - Anonymous users can see only published videos.
    """

    queryset = videos_models.Video.objects.all()
    serializer_class = videos_serializers.VideoSerializer
    permission_classes = [videos_permissions.IsOwnerOrPublished]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return self.queryset

        if user.is_authenticated:
            return self.queryset.filter(Q(is_published=True) | Q(owner=user))

        return self.queryset.filter(is_published=True)


class VideoLikeView(APIView):
    """
    API view to handle liking and unliking of videos.

    Permissions:
        - Only authenticated users can like or unlike videos.
    """
    permission_classes = [IsAuthenticated]

    def get_video(self, video_id: int) -> videos_models.Video | None:
        """
        Retrieve a published video by its ID.

        Args:
            video_id (int): The ID of the video to retrieve.

        Returns:
            videos_models.Video | None: Video object if found and published,
            None otherwise.
        """
        return videos_models.Video.objects.filter(
            id=video_id, is_published=True
        ).first()

    def post(self, request: Request, video_id: int) -> Response:
        """
        Like a video on behalf of the authenticated user.

        Args:
            request (Request): DRF request object containing the user.
            video_id (int): ID of the video to like.

        Returns:
            Response: DRF Response with serialized LikeResult and appropriate
            HTTP status code (201 if created, 400 if already liked).
        """
        video = self.get_video(video_id)
        if not video:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        like_manager = videos_services.VideoLikeManager(
            user=request.user, video=video
        )
        result = like_manager.like()

        serializer = videos_serializers.LikeResultSerializer(result)
        status_code = (
            status.HTTP_201_CREATED
            if result.get("created")
            else status.HTTP_400_BAD_REQUEST
        )
        return Response(serializer.data, status=status_code)


    def delete(self, request: Request, video_id: int) -> Response:
        """
        Unlike a video on behalf of the authenticated user.

        Args:
            request (Request): DRF request object containing the user.
            video_id (int): ID of the video to unlike.

        Returns:
            Response: DRF Response with appropriate HTTP status code
            (204 if deleted, 400 if not deleted, 404 if video not found).
        """
        video = self.get_video(video_id)
        if not video:
            return Response(status=status.HTTP_404_NOT_FOUND)

        like_manager = videos_services.VideoLikeManager(
            user=request.user, video=video
        )
        result = like_manager.unlike()

        if result.get("deleted"):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class VideoIDsView(generics.ListAPIView):
    """
    API view to list the IDs of all published videos.

    Permissions:
        - Only staff users can access this view.

    Attributes:
        serializer_class: Serializer used to format video IDs.
        queryset: Queryset of published videos.
        pagination_class: Disabled pagination for this view.
    """
    permission_classes = [videos_permissions.IsStaff]
    serializer_class = videos_serializers.VideoIDSerializer
    queryset = videos_models.Video.objects.filter(is_published=True)
    pagination_class = None


class StatisticsSubqueryView(APIView):
    """
    API view to retrieve user statistics using a subquery approach.

    Permissions:
        - Only staff users can access this view.
    """
    permission_classes = [videos_permissions.IsStaff]

    def get(self, request: Request) -> Response:
        """
        Handle GET request to return user statistics.

        Args:
            request (Request): DRF request object.

        Returns:
            Response: DRF Response containing serialized statistics data.
        """
        videos = videos_models.Video.objects.filter(is_published=True)
        users = accounts_models.User.objects.all()
        qs = videos_services.StatisticsSubquery(users, videos).get_stats()
        data = videos_serializers.StatisticsSerializer(qs, many=True).data
        return Response(data)


class StatisticsGroupByView(APIView):
    """
    API view to retrieve user statistics grouped by video owners.

    Permissions:
        - Only staff users can access this view.
    """
    permission_classes = [videos_permissions.IsStaff]

    def get(self, request: Request) -> Response:
        """
        Handle GET request to return user statistics grouped by video owners.

        Args:
            request (Request): DRF request object.

        Returns:
            Response: DRF Response containing serialized statistics data.
        """
        videos = videos_models.Video.objects.filter(is_published=True)
        qs = videos_services.StatisticsGroupBy(videos).get_stats()
        data = videos_serializers.StatisticsSerializer(qs, many=True).data
        return Response(data)
