from rest_framework import fields, serializers
from projects.models import Project, Tag, Review
from users.models import Profiles

# to get the child model, we use the serializer method field.
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profiles
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)
    tags = TagSerializer(many=True)

    # to get the child model, we use the serializer method field.
    reviews = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = '__all__'

    # every method should start with the get
    # the self refers to ProjectSerializer
    # the obj refers to the model which is Project here
    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        # now we have to serialize the review mode
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data