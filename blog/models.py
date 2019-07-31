from django.db import models
from django.contrib.auth.models import User
#User라는 모델을 구분하여 주기 위해서 import 하여줌

# Create your models here.
class Blog(models.Model): # Blog 라는 `이름의` 객체 틀(Model) 생성
    title = models.CharField(max_length=200) # title 라는 최대 200 글자의 문자 데이터 저장
    pub_date = models.DateTimeField('date published') # pub_date 라는 날짜 시간 데이터 저장
    body = models.TextField() # body 라는 줄글 문자 저장
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True)
    likes = models.ManyToManyField(
        User,
        through ='Like',
        through_fields = ('blog','user'),
        related_name = 'likes',
    )

    # 이 객체를 가르키는 말을 title로 정하겠다
    def __str__(self):
        return self.title

    def like_count(self):
        return self.likes.count()

class Comment(models.Model):
    body = models.TextField()
    #Blog 모델과 관계를 맺어 준다. 1:N에서 N의 속성으로 들어간다.
    #on_delete는 관계를 맺고 있는 Blog 객체가 삭제되면 관련된 Comment도 삭제 하여준다.
    blog = models.ForeignKey(Blog, on_delete = models.CASCADE, null=True)
    
    def __str__(self):
        return self.body

class Like(models.Model):
    #Blog의 through_fields와 순서가 같아야 한다.
    blog = models.ForeignKey(Blog, on_delete = models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True)
    #*글이 삭제 되면은 그 글에 해당하는 객체도 없애주겠다. => on_delete
