from django import template
from blog.models import Story

register = template.Library()

#def wpm(text_contents):
#   contents_lenth = len(text_contents)
#   words_per_minute = 238
#   number_words_per_minute = round(contents_lenth/words_per_minute)
#   return number_words_per_minute 


#@register.tag
@register.simple_tag
def total_stories(cate_name):
   stories = Story.objects.filter(story_category__category_name=cate_name)
   total_story = len(stories)
   return total_story

