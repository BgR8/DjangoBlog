from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=120, verbose_name='Başlık')
    content = RichTextField(verbose_name='İçerik')
    publishing_date = models.DateTimeField(verbose_name='Yayımlanma Tarihi', auto_now_add=True)
    image = models.ImageField(null=True, blank=True)
    slug = models.SlugField(unique=True, editable=False, max_length=130)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # post:detail; post uygulamasındaki detail url olarak özelleştirdik. urls.py deki app_name'dir
        return reverse("post:detail", kwargs={"slug": self.slug})
        #return "/post/{}".format(self.id)

    def get_create_url(self):
        return reverse("post:create")

    def get_update_url(self):
        return reverse("post:update", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("post:delete", kwargs={"slug": self.slug})

    # Benzersiz slug ekleme; aynı başlıklı yeni bir yazı eklendiğinde önüne sayı ekler
    def get_unique_slug(self):
        slug = slugify(self.title.replace('ı', 'i'))
        unique_slug = slug
        counter = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, counter)
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs):
        self.slug = self.get_unique_slug()
        return super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-publishing_date', 'id']


class Comment(models.Model):

    post = models.ForeignKey('post.Post', on_delete=models.CASCADE, related_name='comments', verbose_name='Gönderi')
    name = models.CharField(max_length=200, verbose_name='Gönderen İsmi')
    content = models.TextField(verbose_name='Yorum')    
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Tarih")
    
    def __str__(self):
        return self.name