from django.http import Http404
from rest_framework import status, generics, permissions
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project, Pledge
from .serializers import ProjectSerializer, PledgeSerializer, ProjectDetailSerializer
from .permissions import IsOwnerOrReadOnly


class ProjectList(APIView):


    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data,
        status = status.HTTP_201_CREATED)
        return Response( serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectDetail(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
        ]

    def get_object(self, pk):
        try:
            project = Project.objects.get(pk=pk)
            self.check_object_permissions(self.request,project)
            return project
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)

    def put(self,request,pk):
        project = self.get.object(pk)
        data = request.data
        serializer = ProjectDetailSerializer(
            instance=project,
            data=data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()

class PledgeList(generics.ListCreateAPIView):
    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer
    
    def perform_create(self, serializer):
        serializer.save(supporter=self.request.user)

class PledgeDetail (generics.RetrieveUpdateDestroyAPIView):
    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer


# class LikePostView(APIView):
    """Api view for liking a post if logged in."""
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    # def put(self, request, id, format=None):
    #     user = request.user
    #     try:
    #         post = ImagePost.objects.get(pk=id)
    #     except ImagePost.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     if post.likes.filter(pk=request.user.pk).exists():
    #         post.likes.remove(request.user)
    #     else:
    #         post.likes.add(request.user)
    # #         if user != post.user:
    #             notify.send(user, recipient=post.user,
    #                         verb=f"{user.username} liked your post.")
    #     return Response(status=status.HTTP_200_OK)