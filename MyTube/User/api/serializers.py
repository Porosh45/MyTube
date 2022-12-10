from rest_framework import serializers
from User.models import User
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.exceptions import AuthenticationFailed
from django.contrib import auth
from videos.models import Video

#user serializer
class UserSerializer(serializers.ModelSerializer):
    videos = serializers.PrimaryKeyRelatedField(many = True, queryset = Video.objects.all())
    class Meta:
        model = User
        fields = ['id', 'email', 'videos']

#User register serializer
class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(min_length=6, write_only=True)
    class Meta:
        model = User
        fields = ['username',  'email', 'password']

    default_message = {
        'username' : 'the username should only contain alphanumeric character'
    }
    def validate(self, attrs):
        username = attrs.get('username', '')
        email = attrs.get('email', '')

        if not username.isalnum():
            raise serializers.ValidationError(self.default_message)
        return attrs

    def create(self, validated_data):
        return User.objects.user_create(**validated_data)


#user login serializer
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=5)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    tokens = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id','email', 'password', 'tokens']

    def get_tokens(self, obj):
        user = User.objects.get(email = obj['email'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access'],
        }

    def validate(self, attrs):
        password = attrs.get('password', '')
        email = attrs.get('email','')
        user = auth.authenticate(email = email, password = password)

        if not user:
            raise AuthenticationFailed('Invalid User')

        return {
            'email' : user.email,
            'tokens' : user.tokens,
        }
        return super().validate(attrs)
#user logout serializer
class LogoutSerializer(serializers.ModelSerializer):
    Refresh = serializers.CharField()
    token_message = {
        'bad_token' : "Invalid Token or expired!!!!!!"
    }

    def validate(self, attrs):
        self.token = attrs['Refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
