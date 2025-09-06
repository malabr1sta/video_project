from rest_framework import serializers
from videos import models as videos_models


class VideoFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = videos_models.VideoFile
        fields = ['id', 'file', 'quality']


class VideoSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)
    files = VideoFileSerializer(many=True, read_only=True)

    class Meta:
        model = videos_models.Video
        fields = ['id', 'owner', 'name', 'total_likes', 'created_at', 'files']


class LikeResultSerializer(serializers.Serializer):
    obj = serializers.PrimaryKeyRelatedField(
        queryset=videos_models.Like.objects.all(),
        required=False, allow_null=True
    )
    created = serializers.BooleanField()


class VideoIDSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = videos_models.Video
        fields = ['id', 'username']


class StatisticsSerializer(serializers.Serializer):
    username = serializers.CharField()
    likes_sum = serializers.IntegerField()
