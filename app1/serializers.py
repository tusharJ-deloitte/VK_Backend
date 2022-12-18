from rest_framework import serializers

class PostSerializer(serializers.Serializer):
    id =serializers.IntegerField()
    title = serializers.CharField(max_length=50)
    content = serializers.CharField(max_length=200)
    author = serializers.CharField(max_length=20)

class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=30)
    created_on = serializers.DateTimeField()