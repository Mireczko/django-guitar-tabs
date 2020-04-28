from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework import filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from accounts.models import User
from accounts.tokens import account_activation_token
from guitar_tabs.models import GuitarTabDetails, Comment, GuitarTab
from rest.serializers import UserSerializer, GuitarTabDetailsSerializer, CommentSerializer, GuitarTabSerializer
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


class GuitarTabDetailsView(ListCreateAPIView):
    filter_backends = [filters.SearchFilter]
    search_fields = ['band', 'song', 'user__nick']
    queryset = GuitarTabDetails.objects.all()
    serializer_class = GuitarTabDetailsSerializer


class GuitarTabCreate(CreateAPIView):
    queryset = GuitarTabDetails.objects.all()
    serializer_class = GuitarTabSerializer
    parser_classes = (MultiPartParser, JSONParser)


class GuitarTabView(APIView):
    def get(self, request, pk):
        tab = GuitarTab.objects.get(pk=pk)
        return Response(tab)


class CommentsView(ListCreateAPIView):
    filter_backends = [filters.SearchFilter]
    search_fields = ['tab__user']
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
