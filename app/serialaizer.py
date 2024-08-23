from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from app.models import Category, Group, Product, Comment, Image, Attribute
from django.db.models import Avg
from django.db.models.functions import Round
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()



class CategorySerializer(ModelSerializer):
    image = serializers.ImageField(required=False)
    group_count = serializers.SerializerMethodField()
    def get_group_count(self, obj):
        return obj.groups.count()

    class Meta:
        model = Category
        fields = '__all__'


class GroupSerializer(ModelSerializer):
    #category = CategorySerializer(read_only = True)
    category_slug = serializers.SlugField(source = 'category.slug')
    category_title = serializers.CharField(source = 'category.title')
    product_count = serializers.SerializerMethodField()
    def get_product_count(self, instance):
        return instance.products.count()
    
    class Meta:
        model = Group
        fields = '__all__'

class ProductSerializer(ModelSerializer):
    category_name = serializers.CharField(source = 'group.category.title')
    group_name = serializers.CharField(source = 'group.name')
    is_liked = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    all_images = serializers.SerializerMethodField()
    comment_info = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()

    def get_attributes(self, instance):
        attrs = instance.attributes.all().values('key__name', 'value__name')
        product_attributes =[
            {
                attribute['key__name']: attribute['value__name']
            }
            for attribute in attrs
        ]
        return product_attributes

    def get_comment_info(self,obj):
        comments = [
            {
            'message': comment.message,
            'rating': comment.rating,
            'username': comment.user.username
            }   
            for comment in obj.comment.all()]
        return comments
    
    def get_all_images(self, instance):
        request = self.context.get('request', None)
        images = instance.images.all().order_by('-is_primary','-id')
        all_images = []
        for image in images:
            all_images.append(request.build_absolute_uri(image.image.url))
        return all_images

    def get_avg_rating(self, product):
        avg_rating = product.comment.all().aggregate(avg =Round(Avg('rating')))
        print(avg_rating)
        return avg_rating.get('avg')

    def get_image(self, obj):
        # image = Image.objects.filter(is_primary = True, product = obj).first()
        image = obj.images.filter(is_primary=True).first()
        if image:
            image_url = image.image.url
            request = self.context.get('request')
            return request.build_absolute_uri(image_url)

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            if user in obj.is_liked.all():
                return True
        return False
    
    
    class Meta:
        model = Product
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class AttributeSerializer(ModelSerializer):
    class Meta:
        model =  Attribute
        fields = '__all__'


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 100, required=True)
    password = serializers.CharField(max_length = 100, required=True)



class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100, required=True)
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100, write_only=True, required=True)
    password2 = serializers.CharField(max_length=100, write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password2')

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise ValidationError({"detail": "User already exists!"})
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise ValidationError({"password2": "Passwords must match!"})

        if User.objects.filter(email=data['email']).exists():
            raise ValidationError({"email": "Email already taken!"})

        return data

    def create(self, validated_data):
        # Remove the password2 field
        validated_data.pop('password2', None)
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
