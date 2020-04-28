from wsgiref.util import FileWrapper

from django.http import HttpResponse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework import filters, generics, viewsets
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.generics import ListCreateAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from accounts.models import User
from accounts.tokens import account_activation_token
from guitar_tabs.models import Comment, GuitarTab
from rest.serializers import UserSerializer, CommentSerializer, GuitarTabSerializer, GuitarTabFullSerializer, \
    GuitarTabDetailsSerializer
from rest_framework.parsers import MultiPartParser, JSONParser

'''
Register user
'''


@api_view(['POST'])
@permission_classes((AllowAny,))
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''
Activate registered
'''


@api_view(['GET'])
@permission_classes((AllowAny,))
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        return Response({"success": "true"}, status=status.HTTP_200_OK)
    else:
        return Response({"success": "false"}, status=status.HTTP_400_BAD_REQUEST)


'''
CREATE NEW TAB
'''


class GuitarTabCreate(CreateAPIView):
    serializer_class = GuitarTabFullSerializer
    parser_classes = (MultiPartParser, JSONParser)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


'''
GET LIST OF TABS ( DETAILS )
'''


class GuitarTabListView(ListAPIView):
    filter_backends = [filters.SearchFilter]
    search_fields = ['band', 'song', 'user__nick']
    queryset = GuitarTab.objects.all()
    serializer_class = GuitarTabDetailsSerializer


'''
GET/UPDATE/DELETE SPECIFIC TAB
'''


@api_view(['GET', 'POST', 'DELETE'])
@parser_classes([MultiPartParser, JSONParser])
def guitar_tab(request, pk):
    user = request.user
    try:
        guitar_tab = GuitarTab.objects.get(pk=pk)
    except GuitarTab.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = GuitarTabFullSerializer(guitar_tab)
        return Response(serializer.data)
    if request.method == 'POST':
        if guitar_tab.user != user:
            return Response({"You cannot edit someone else's tab!"}, status=status.HTTP_403_FORBIDDEN)
        else:
            serializer = GuitarTabFullSerializer(guitar_tab, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        if guitar_tab.user != user:
            return Response({"You cannot delete someone else's tab!"}, status=status.HTTP_403_FORBIDDEN)
        else:
            guitar_tab.delete()
            return Response(status=status.HTTP_200_OK)


'''
CREATE NEW COMMENT
'''


class CommentsView(CreateAPIView):
    filter_backends = [filters.SearchFilter]
    search_fields = ['tab__user']
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


'''
GET/UPDATE/DELETE SPECIFIC COMMENT
'''


@api_view(['GET', 'POST', 'DELETE'])
def comment(request, pk):
    user = request.user
    try:
        if request.method == 'GET':
            tab=GuitarTab.objects.get(pk=pk)
            comment = Comment.objects.filter(tab=tab)
            serializer = CommentSerializer(comment, many=True)
            return Response(serializer.data)
        if request.method == 'POST':
            comment = Comment.objects.get(pk=pk)
            if comment.user != user:
                return Response({"You cannot edit someone else's comment!"}, status=status.HTTP_403_FORBIDDEN)
            else:
                serializer = CommentSerializer(comment, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'DELETE':
            comment = Comment.objects.get(pk=pk)
            if comment.user != user:
                return Response({"You cannot delete someone else's comment!"}, status=status.HTTP_403_FORBIDDEN)
            else:
                comment.delete()
                return Response(status=status.HTTP_200_OK)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
