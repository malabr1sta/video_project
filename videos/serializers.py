from rest_framework import serializers
from videos import models as videos_models


class VideoFileSerializer(serializers.ModelSerializer):
    """
    Serializer for VideoFile model, representing individual video files
    with different qualities.
    """
    class Meta:
        model = videos_models.VideoFile
        fields = ['id', 'file', 'quality']


class VideoSerializer(serializers.ModelSerializer):
    """
    Serializer for the Video model, including owner username and
    associated video files.

    Attributes:
        owner: Read-only field representing the username of the video owner.
        files: Read-only nested serializer for video files.
    """
    owner = serializers.CharField(source='owner.username', read_only=True)
    files = VideoFileSerializer(many=True, read_only=True)

    class Meta:
        model = videos_models.Video
        fields = ['id', 'owner', 'name', 'total_likes', 'created_at', 'files']


class LikeResultSerializer(serializers.Serializer):
    """
    Serializer for the result of a like action.

    Attributes:
        obj: The Like object created or None if not created.
        created: Indicates whether a new Like was created.
    """
    obj = serializers.PrimaryKeyRelatedField(
        queryset=videos_models.Like.objects.all(),
        required=False, allow_null=True
    )
    created = serializers.BooleanField()


class VideoIDSerializer(serializers.ModelSerializer):
    """
    Serializer for Video model to return only the video ID and owner's username.

    Attributes:
        username: Read-only field representing the username of the video owner.
    """
    username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = videos_models.Video
        fields = ['id', 'username']


class StatisticsSerializer(serializers.Serializer):
    """
    Serializer for user statistics, including username and total likes.

    Attributes:
        username (CharField): Username of the user.
        likes_sum (IntegerField): Total number of likes for the user's videos.
    """
    username = serializers.CharField()
    likes_sum = serializers.IntegerField()
