from .models import Category, Profile, Story, Collection, Profiles, Notification
from django.contrib import messages
from datetime import datetime
from users.models import User

#from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def community_category(request):
    # First Category Name
    chosen_category1 = Category.objects.filter(
        show_on_navigation_bar=True).order_by("-date")[0]
    category_name1 = chosen_category1.category_name

    # Second Category Name
    chosen_category2 = Category.objects.filter(
        show_on_navigation_bar=True).order_by("-date")[2]
    category_name2 = chosen_category2.category_name

    # Third Category Name
    chosen_category3 = Category.objects.filter(
        show_on_navigation_bar=True).order_by("-date")[3]
    category_name3 = chosen_category3.category_name

    # Fourth Category Name
    chosen_category4 = Category.objects.filter(
        show_on_navigation_bar=True).order_by("-date")[4]
    category_name4 = chosen_category4.category_name

    # Fourth Category Name
    chosen_category5 = Category.objects.filter(
        show_on_navigation_bar=True).order_by("-date")[5]
    category_name5 = chosen_category5.category_name

    return category_name1, category_name2, category_name3, category_name4, category_name5


def nav_greeting(request):
    current_user = request.user
    current_time = datetime.today()
    hour = current_time.hour
    morning = range(0, 12)
    afternoon = range(12, 17)
    evening = range(17, 24)
    global GREETING
    for num in morning:
        if num == hour:
            GREETING = "Good Morning"
    for num in afternoon:
        if num == hour:
            GREETING = "Good Afternoon"
    for num in evening:
        if num == hour:
            GREETING = "Good Evening"
    return GREETING, current_user


#def following_manager(request):
#    if request.method == "POST":
#        if "author-to-follow" in request.POST:
#            follower_id = request.POST.get("author-to-follow")
#            new_following = User.objects.get(id=follower_id)
#            user_profile = Profile.objects.filter(user=request.user).first().author_following.all()
#            user_following = [following for following in user_profile]
#            #Creating Follower
#            if new_following not in user_following:
#                profile_instance = Profile.objects.filter(user=request.user).first()
#                profile_instance.author_followers.add(new_following)
#                profile_instance.save()
#
#    # Authors to show
#    all_authors = User.objects.all().exclude(id=request.user.id)[:4]
#    profile_model = Profile.objects.filter(user__id=request.user.id).first()
#    all_following = profile_model.author_following.all()
#    authors_to_show = []
#    for author in all_authors:
#        if author not in all_following:
#            authors_to_show.append(author)
#
#    return authors_to_show
    
def follower_manager(request):
    if request.method == "POST":
        if "author-to-follow" in request.POST:
            follower_id = request.POST.get("author-to-follow")
            new_follower = Profiles.objects.get(user__id=follower_id)
            user_profile = Profiles.objects.get(user=request.user)
            user_followers = [follower for follower in user_profile.following.all()]
            #Creating Follower
            if new_follower not in user_followers:
                profile_instance = Profiles.objects.get(user=request.user)
                profile_instance.following.add(new_follower)
                profile_instance.save()

                # Creating Notification
                user_id = new_follower.user.id
                user_instance = User.objects.get(id=user_id)
                followed_user = user_profile.user.id
                followed_instance = User.objects.get(id=followed_user)

                message = f"{followed_instance.first_name} {followed_instance.last_name} started following you"
                Notification.objects.create(user=user_instance, message=message)

    # Authors to show
    all_authors = Profiles.objects.all().exclude(user=request.user)
    profile_model = Profiles.objects.get(user=request.user)
    all_following = profile_model.following.all()
    authors_to_show = []
    for author in all_authors:
        if author not in all_following:
            authors_to_show.append(author)

    return authors_to_show


def follow_users_manager(request):
    if "author-to-follow" in request.POST:
        unfollower_id = request.POST.get("author-to-follow")
        new_follow = Profiles.objects.get(user__id=unfollower_id)
        profile_instance = Profiles.objects.get(user=request.user)
        profile_instance.following.add(new_follow)
        profile_instance.save()

        # Creating Notification
        user_id = new_follow.user.id
        user_instance = User.objects.get(id=user_id)
        followed_user = profile_instance.user.id
        followed_instance = User.objects.get(id=followed_user)

        message = f"{followed_instance.first_name} {followed_instance.last_name} started following you"
        Notification.objects.create(user=user_instance, message=message)

def unfollow_users_manager(request):
    if "author-to-unfollow" in request.POST:
        unfollower_id = request.POST.get("author-to-unfollow")
        new_unfollow = Profiles.objects.get(user__id=unfollower_id)
        profile_instance = Profiles.objects.get(user=request.user)
        profile_instance.following.remove(new_unfollow)
        profile_instance.save()

def user_category(request):
    user_profile = Profiles.objects.get(user=request.user)
    if user_profile:

        # First Category Name
        user_topics1 = user_profile.categories.all()[0]
        category_name1 = user_topics1.category_name

        # Second Category Name
        user_topics2 = user_profile.categories.all()[1]
        category_name2 = user_topics2.category_name

        # Third Category Name
        user_topics3 = user_profile.categories.all()[2]
        category_name3 = user_topics3.category_name

        # Fourth Category Name
        user_topics4 = user_profile.categories.all()[3]
        category_name4 = user_topics4.category_name

    return category_name1, category_name2, category_name3, category_name4


def saved_stories_and_recently_saved(request):
    # Save story for later:
    if request.method == "POST":
        if "story_id" in request.POST:
            story_id = request.POST.get("story_id")
            story_to_save = Story.objects.get(id=story_id)
            all_collections = Collection.objects.all()
            all_users_saved_stories = [
                collection.user for collection in all_collections]
            # Creating collections
            if request.user not in all_users_saved_stories:
                collection_instance = Collection.objects.create(
                    user=request.user)
                collection_instance.story.add(story_to_save)
                collection_instance.save()
            else:
                user_collection = Collection.objects.filter(
                    user=request.user).first()
                user_collection.story.add(story_to_save)
                user_collection.save()

            # Checking if collection exists
            current_user_collection = Collection.objects.filter(
                user=request.user).first()
            saved_stories = current_user_collection.story.all()
            if story_to_save not in saved_stories:
                messages.success(
                    request, "This story has been saved for later")
            else:
                messages.error(
                    request, "This story has been saved already")

    # Recently Saved
    all_collections = Collection.objects.all()
    all_users_saved_stories = [
        collection.user for collection in all_collections]

    if request.user not in all_users_saved_stories:
        saved_stories_to_show = []
    else:
        the_current_user_collection = Collection.objects.filter(
            user=request.user).first()
        saved_stories_to_show = the_current_user_collection.story.all().order_by(
            "-date")[:3]
        
    return saved_stories_to_show

def username_generator(request):
    current_user = request.user
    user_id = str(current_user.id)
    user_name_combo = (current_user.first_name + current_user.last_name + user_id).lower()
    return user_name_combo













# def search_products(request):
#    # Search Functionality#
#    search_query = ""
#    if request.GET.get("search-product"):
#        search_query = request.GET.get("search-product")
#    products = Product.objects.distinct().filter(
#        product_name__icontains=search_query)
#    return products, search_query


# Working With Paginator


#def paginate_pages(request, products, results):
#    page = request.GET.get("page")
#    paginator = Paginator(products, results)
#    try:
#        products = paginator.page(page)
#    except PageNotAnInteger:
#        page = 1
#        products = paginator.page(page)
#    except EmptyPage:
#        page = paginator.num_pages
#        products = paginator.page(page)
#
#    left_index = (int(page) - 4)
#    if left_index < 1:
#        left_index = 1
#    right_index = (int(page) + 5)
#    if right_index > paginator.num_pages:
#        right_index = paginator.num_pages + 1
#    custom_range = range(left_index, right_index)
#
#    return custom_range, products
#
#
## Working With Paginator
#def paginate_home_pages(request, vegetables_on_homescreen, results):
#    page = request.GET.get("page")
#    paginator = Paginator(vegetables_on_homescreen, results)
#    try:
#        vegetables_on_homescreen = paginator.page(page)
#    except PageNotAnInteger:
#        page = 1
#        vegetables_on_homescreen = paginator.page(page)
#    except EmptyPage:
#        page = paginator.num_pages
#        vegetables_on_homescreen = paginator.page(page)
#
#    left_index = (int(page) - 4)
#    if left_index < 1:
#        left_index = 1
#    right_index = (int(page) + 5)
#    if right_index > paginator.num_pages:
#        right_index = paginator.num_pages + 1
#    custom_range = range(left_index, right_index)
#
#    return custom_range, vegetables_on_homescreen





#products, search_query = search_products(request)
