from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from accounts.models import User
from accounts.tokens import account_activation_token
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from guitar_tabs.models import GuitarTabDetails, GuitarTab, Comment


class GuitarTabSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuitarTab
        fields = ('tab_text', 'tab_file', 'details')


class GuitarTabDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuitarTabDetails
        fields = ('band', 'song', 'link', 'user')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('tab', 'message')


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
