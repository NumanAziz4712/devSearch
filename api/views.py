from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api import serializers
from api.serializers import ProjectSerializer
from projects.models import Project, Review
# Here in the list we can specify the methods for the view i-e. GET POST PUT
@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET':'api/projects'},
        {'GET':'api/projects/id'},
        {'POST':'api/projects/id/vote'},

        {'POST':'api/users/token'},
        {'POST':'api/users/token/refresh'},
        
    ]

    return Response(routes)

# get the serilazed data from the serialzer class.
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getProjects(request):

    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    # get the serialized data from the serializer class
    return Response(serializer.data)

@api_view(['GET'])
def getProject(request, pk):

    project = Project.objects.get(id=pk)
    serializer = ProjectSerializer(project, many=False)
    # get the serialized data from the serializer class
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ProjectVote(request, pk):
    project = Project.objects.get(id=pk)
    user = request.user.profiles
    data = request.data

    review, created = Review.objects.get_or_create(
        owner=user,
        project=project,
    )
    review.value = data['value']
    review.body = data['body']
    review.save()
    project.getVoteCount

    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)