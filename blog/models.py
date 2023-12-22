from django.db import models
from users.models import User
from django.utils.text import slugify
from django.utils import text

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=20, null=True, blank=False)
    short_description = models.CharField(max_length=150, null=True, blank=False)
    category_image = models.ImageField(null=True, blank=False, upload_to="images")
    show_on_navigation_bar = models.BooleanField(default=False, help_text="No=Don't show, Yes=Show", null=True)
    follower_count = models.IntegerField(default=0, null=True)
    date = models.DateField(auto_now_add=True, null=True)
    slug = models.SlugField(blank=False, null=False, default="", db_index=True)

    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return str(self.category_name)

class Tag(models.Model):
    tag_name = models.CharField(max_length=20, null=True, blank=False)
    date = models.DateField(auto_now_add=True, null=True)

    class Meta:
        ordering = ["-date"]
    
    def __str__(self):
        return str(self.tag_name)

class Story(models.Model):
    story_heading = models.CharField(max_length=100, null=False, blank=False)
    story_subtitle = models.CharField(max_length=100, null=False, blank=True)
    story_image = models.ImageField(null=False, blank=False, upload_to="images")
    text_contents = models.TextField(max_length=20000, null=False, blank=False)
    story_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    trending = models.BooleanField(default=False, help_text="No=Not Trending, Yes=Trending")
    recommemended = models.BooleanField(
        default=False, help_text="No=Not Recommemended, Yes=Recommemended", null=True)
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True, null=False)
    slug = models.SlugField(blank=False, null=False,
                            default="", db_index=True, max_length=500)

    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Stories"

    def save(self, **args):
        self.slug = slugify(self.story_heading)
        super().save(**args)
    
    def __str__(self):
        return str(self.story_heading)
    
    #custom function to use in view
    def wpm(self):
       self.contents_lenth = len(self.text_contents)
       words_per_minute = 1700
       number_words_per_minute = round(self.contents_lenth/words_per_minute)
       return number_words_per_minute
        
    
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chosen_categories = models.ManyToManyField(Category)
    display_name = models.CharField(max_length=100, null=True, blank=False)
    author_followers = models.ManyToManyField(User, related_name="author_followers")
    author_following = models.ManyToManyField(User, related_name="author_following")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    profile_display_name = models.CharField(max_length=100, null=True, blank=False)
    follows = models.ManyToManyField(
        "self", related_name="followed_by", symmetrical=False, blank=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
class Profiles(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    profile_display_name = models.CharField(max_length=100, null=True, blank=False)
    following = models.ManyToManyField(
        "self", related_name="followers", symmetrical=False, blank=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    
    
class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ManyToManyField(Story)
    date = models.DateField(auto_now_add=True, null=True)
    
    class Meta:
        ordering = ["-date"]
    
    def __str__(self):
        return str(self.user.first_name)
    

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    comment = models.TextField(max_length=500, null=True, blank=False)
    date = models.DateField(auto_now_add=True, null=False)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return str(self.user.first_name)
    

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=300, null=True, blank=False)
    is_story_review = models.BooleanField(
        default=False, help_text="No=Not story review, Yes=Story Review")
    date = models.DateField(auto_now_add=True, null=False)


class Search(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    search_query = models.TextField(max_length=500, null=True, blank=True) 

