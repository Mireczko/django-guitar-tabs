from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from accounts.models import User
from accounts.tokens import account_activation_token
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from guitar_tabs.models import GuitarTab, Comment


class GuitarTabFullSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = GuitarTab
        fields = '__all__'


class GuitarTabSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = GuitarTab
        fields = ('tab_text', 'tab_file', 'link', 'user')





# class GuitarTabDetailsSerializer(serializers.ModelSerializer):


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Comment
        fields = ('tab', 'message', 'user')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'nick', 'password']

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            nick=validated_data['nick'],
            is_active=False
        )
        user.set_password(validated_data['password'])
        current_site = "http://localhost:8000"
        mail_subject = _('Activate your account.')
        message = render_to_string('accounts/account_confirmation.html', {
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = validated_data['email']
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.content_subtype = "html"
        email.send()
        user.save()
        return user

class GuitarTabDetailsSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = GuitarTab
        fields = ('band', 'song', 'user', 'id')