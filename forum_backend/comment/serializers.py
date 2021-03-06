from rest_framework import serializers
from post.models import Post
from post.serializers import PostSerializer
from category.models import Category
from comment.models import Comment
from django.contrib.contenttypes.models import ContentType
from rest_framework.reverse import reverse
from utils.serializer_tools import CommentTargetSerializer
from notification.serializers import find_post
from drf_yasg.utils import swagger_serializer_method

class CommentSerializer(serializers.ModelSerializer):
    # commmet_user_url = serializers.HyperlinkedIdentityField(view_name='user:user-detail',
    #                                                         lookup_field='pk')
    description = serializers.SerializerMethodField(help_text='动作描述')
    user_id = serializers.ReadOnlyField(source='user.id')
    user = serializers.ReadOnlyField(source='user.username')
    content_type_id = serializers.ReadOnlyField(source='content_type.id',help_text='内容类型')
    target = serializers.SerializerMethodField(help_text='评论目标对象数据')
    relay_source = serializers.SerializerMethodField(help_text='转发源')
    # category = serializers.SlugRelatedField(queryset=Category.objects.all(),
    #                                         slug_field='name',
    #                                         allow_null=True)
    # comments = serializers.SlugRelatedField(many=True,
    #                                         slug_field='content',
    #                                         read_only=True,
    #                                         allow_null=True)
    class Meta:
        model = Comment
        read_only_fields = ('user','created','description')
        fields = '__all__'

    def target_model_class(self,obj):
        content_type = ContentType.objects.get_for_id(obj.content_type.id)
        model_class = content_type.model_class()
        return model_class

    # @swagger_serializer_method(serializer_or_field=serializers.DictField(child=PostSerializer,read_only=True))
    def get_target(self,obj):
        model_class = self.target_model_class(obj)

        target_obj = model_class.objects.get(id=obj.object_id) \
            if model_class.objects.filter(id=obj.object_id).exists() \
            else None
        if not target_obj :
            return {'message':'评论对象目标不存在','status_code':404} 
        data = CommentTargetSerializer.payload(target_obj,obj.content_type.id)
        return data

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_description(self,obj):
        model_class = self.target_model_class(obj)
        if model_class.__name__ == 'Comment':
            message='回复评论'
        if model_class.__name__ == 'Post':
            message='评论帖子'
        return message

    def get_relay_source(self,obj):
        request = self._context.get('request')
        # POST request processing below
        if request.method == 'POST':
            from_object = request.from_object # POST 请求所响应需要显示评论的转发
            if from_object:
                if from_object.__class__.__name__ == 'Post':
                    serializer = RelayPostSerializer(from_object,context={'request': request})
                    return serializer.data
                if from_object.__class__.__name__ == 'Comment':
                    serializer = RelayCommentSerializer(from_object,context={'request': request})
                    return serializer.data
                return None
        # GET request will be processing in below
        relay_data = obj.relay_source # for above use json.loads(obj.relay_source) in POST request as well 
        if relay_data:
            if isinstance(relay_data,str):
                return None
            relay_type ,relay_id = relay_data.get('type'),relay_data.get('id')
            # if the model type is no Post or Comment model return None
            if relay_type not in ['Post','Comment']:
                return None
            if relay_type == 'Post':
                post = Post.objects.filter(id=relay_id).first()
                serializer = RelayPostSerializer(post,context={'request': request})
                return serializer.data
            if relay_type == 'Comment':
                comment = Comment.objects.filter(id=relay_id).first()
                serializer = RelayCommentSerializer(comment,context={'request': request})
                return serializer.data

        return None


class RelayPostSerializer(serializers.ModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='post:post-detail')
    author = serializers.ReadOnlyField(source='author.username',allow_null=True)
    category = serializers.SlugRelatedField(queryset=Category.objects.all(),
                                            slug_field='name',
                                            allow_null=True)
    class Meta:
        model = Post
        fields = ['id','url','author','category','title','body','created']


class RelayCommentSerializer(serializers.ModelSerializer):

    # url = serializers.HyperlinkedIdentityField(view_name='post:post-detail')
    user = serializers.ReadOnlyField(source='user.username',allow_null=True)
    post = serializers.SerializerMethodField(help_text='所属帖子')

    class Meta:
        model = Comment
        fields = ['id','user','post','content','created']

    def get_post(self,obj):
        request = self._context.get('request')
        post = find_post(obj)
        data = {
            'url':reverse('post:post-detail',args=[obj.id],request=request),
            'title':post.title
        }
        return data



class ListCommentQuerySerializer(serializers.Serializer):
    '''
    List查询参数序列化类
    '''
    post_id = serializers.IntegerField(help_text='帖子的id',required=False)


class PostCommentQuerySerializer(serializers.Serializer):
    '''
    Post查询参数序列化类
    '''
    from_type = serializers.ChoiceField(('post','comment'),help_text='选择来源类型',required=False)
    from_id = serializers.IntegerField(help_text='选择来源类型ID',required=False)