
from dataclasses import field, fields
from statistics import mode
from rest_framework import serializers
from watchlist_app.models import WatchList,StreamPlataform,Review

class ReviewsSerializer(serializers.ModelSerializer):
    review_user=serializers.StringRelatedField(read_only=True)
    class Meta:
        model=Review
        #fields="__all__"
        exclude=('watchlist',)

class WatchListSerializer(serializers.ModelSerializer):
    reviews=ReviewsSerializer(many=True,read_only=True)  
    class Meta:
        model=WatchList
        fields="__all__"

      

class StreamPlatafotmSerializer(serializers.ModelSerializer):
    watchlist=WatchListSerializer(many=True, read_only=True)
    class Meta:
        model=StreamPlataform
        fields="__all__"



"""
class MovieSerializer(serializers.ModelSerializer):
    len_name=serializers.SerializerMethodField()
    tag=serializers.SerializerMethodField()
    class Meta:
        model=Movie
        fields="__all__"

    def get_len_name(self,object):
        return len(object.name)

    def get_tag(self,object):
        return object.name[0:4]

    def validate(self, data):
        if data['name']==data['description']:
            raise serializers.ValidationError("Name and description must be different")    
        return data
    def validate_name(self,data):
        if len(data)<2:
            raise serializers.ValidationError("Name is too short!")
        return data     

"""
""""
class MovieSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    name=serializers.CharField()
    description=serializers.CharField()
    activate=serializers.BooleanField()

    def  create(self,validated_data):
        return Movie.objects.create(**validated_data)
    def update(self, instance, validated_data):
        instance.name=validated_data.get('name',instance.name)
        instance.description=validated_data.get('description',instance.description)
        instance.activate=validated_data.get('activate',instance.activate)
        instance.save()
        return instance
    def validate(self, data):
        if data['name']==data['description']:
            raise serializers.ValidationError("Name and description must be different")    
        return data
    def validate_name(self,data):
        if len(data)<2:
            raise serializers.ValidationError("Name is too short!")
        return data     
"""
