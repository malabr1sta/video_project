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
    permission_classes = [IsAuthenticated]

    def get_video(self, video_id: int) -> videos_models.Video | None:
        return videos_models.Video.objects.filter(
            id=video_id, is_published=True
        ).first()

    def post(self, request: Request, video_id: int) -> Response:
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
    permission_classes = [videos_permissions.IsStaff]
    serializer_class = videos_serializers.VideoIDSerializer
    queryset = videos_models.Video.objects.filter(is_published=True)
    pagination_class = None


class StatisticsSubqueryView(APIView):
    permission_classes = [videos_permissions.IsStaff]

    def get(self, request: Request) -> Response:
        videos = videos_models.Video.objects.filter(is_published=True)
        users = accounts_models.User.objects.all()
        qs = videos_services.StatisticsSubquery(users, videos).get_stats()
        data = videos_serializers.StatisticsSerializer(qs, many=True).data
        return Response(data)


class StatisticsGroupByView(APIView):
    permission_classes = [videos_permissions.IsStaff]

    def get(self, request: Request) -> Response:
        videos = videos_models.Video.objects.filter(is_published=True)
        qs = videos_services.StatisticsGroupBy(videos).get_stats()
        data = videos_serializers.StatisticsSerializer(qs, many=True).data
        return Response(data)
