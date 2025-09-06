from django.urls import include, path
from rest_framework.routers import DefaultRouter

from videos import views as videos_views


router = DefaultRouter()
router.register(r'', videos_views.VideoView, basename='video')

urlpatterns = [
    path(
        "ids/",
        videos_views.VideoIDsView.as_view(),
        name="video-ids"
    ),
    path(
        "statistics-subquery/",
        videos_views.StatisticsSubqueryView.as_view(),
        name="video-statistics-subquery"
    ),
    path(
        "statistics-group-by/",
        videos_views.StatisticsGroupByView.as_view(),
        name="video-statistics-group-by"
    ),
    path(
        "",
        include(router.urls)
    ),
    path(
        "<int:video_id>/likes/",
        videos_views.VideoLikeView.as_view(),
        name="video-likes"
    ),
]

