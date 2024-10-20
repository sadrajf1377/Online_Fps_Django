from django.db import models
from user_moudle.models import custom_user
# Create your models here.
class Post_Model(models.Model):
    caption=models.TextField(max_length=2000,verbose_name='post caption',null=False,blank=False)
    title=models.CharField(verbose_name='post title',max_length=30,blank=False,null=False)
    creation_date=models.DateTimeField(auto_now_add=True,verbose_name='date of creation',null=False,blank=False)
    author=models.ForeignKey(custom_user,on_delete=models.CASCADE,null=False,blank=False,verbose_name='creator of this post')
    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        has_hashtags=self.caption.__contains__('#')
        if self.id == None:
            super().save()
        my_tags = Hash_Tag.objects.filter(posts=self)
        if   has_hashtags:

            index=self.caption.find('#')
            hash_tags=list(self.caption[index+1::].split('#'))

            for tag in my_tags:
                if not tag.title in hash_tags:
                    tag.posts.remove(self)
            for tag in hash_tags:
                tg=''.join([x for x in tag if x!=' '])
                obj,o=Hash_Tag.objects.get_or_create(title=tg)
                print(obj,tag)
                obj.posts.add(self)
        else:
            for tag in my_tags:
                    tag.posts.remove(self)
        super().save()
    def get_thumbnail(self):
        try:
            url=self.post_images_set.first().picture.url
        except:
            url=''
        return url
    def get_preview_comments(self):
        comments=self.post_comment_set.all()[:20:]
        return comments



    def __str__(self):
        return self.title
    class Meta:
        verbose_name='post'
        verbose_name_plural='posts'
    def get_my_comments(self):
        return self.post_comment_set.filter(parent_comment__isnull=True).all()

class Post_Images(models.Model):
    picture=models.ImageField(upload_to='post_images',null=False,blank=False,verbose_name='picture of a post')
    parent_post=models.ForeignKey(Post_Model,verbose_name='parent post',on_delete=models.CASCADE,null=False,blank=False,db_index=True)

class Post_Comment(models.Model):
    written_by=models.ForeignKey(custom_user,on_delete=models.CASCADE,verbose_name='author',null=False,blank=False)
    parent_post=models.ForeignKey(Post_Model,on_delete=models.CASCADE,null=False,blank=False,verbose_name='parent post',db_index=True)
    date=models.DateTimeField(auto_now_add=True,verbose_name='date of creation',null=False,blank=False)
    comment_text=models.TextField(max_length=1000,verbose_name='main text of comment',null=False,blank=False)
    parent_comment=models.ForeignKey('Post_Comment',on_delete=models.CASCADE,null=True,blank=True,verbose_name='parent comment')


class Post_Like_List(models.Model):
    post=models.OneToOneField(Post_Model,on_delete=models.CASCADE,verbose_name='parent post of list',null=False,blank=False)
    users=models.ManyToManyField(custom_user,null=True,blank=True,verbose_name='users that liked this post')
    def __str__(self):
        return f'this list belongs to post with {self.post.title} title'
    class Meta:
        verbose_name='like_list'
        verbose_name_plural='like_lists'

class Hash_Tag(models.Model):
    title=models.CharField(null=False,blank=False,max_length=100,verbose_name='hashtag title',unique=True)
    posts=models.ManyToManyField(Post_Model,verbose_name='related posts',null=True,blank=True)
    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super().save()
    def __str__(self):
        return f'#{self.title} //{self.id}'