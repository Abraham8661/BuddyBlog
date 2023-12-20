from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from users.forms import SignUpForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Story, Category, Profile, Collection, Tag, Comments, Profiles, Notification, Search
from users.models import User
from .utills import community_category, nav_greeting, follower_manager, user_category, saved_stories_and_recently_saved, follow_users_manager, unfollow_users_manager, username_generator
import pyperclip
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q


def home_page_view(request):
    #Trending on BuddyBlog
    trending_stories = Story.objects.filter(trending=True)
    trending_stories_on_homescreen = trending_stories.order_by("-date")[:6]

    # Categories In NavBar
    nav_categories = Category.objects.filter(show_on_navigation_bar=True).order_by("-date")[:6]

    #From The Community
    chosen_category = Category.objects.filter(
        show_on_navigation_bar=True)
    community_stories = Story.objects.filter(
        story_category__show_on_navigation_bar=True).order_by("-date")[:15]


    # Discover other interesting topics
    other_categories = Category.objects.filter(
        show_on_navigation_bar=False).order_by("-date")[:10]

    user = request.user
    if user.is_authenticated:
        return redirect("user_home")
    
    return render(request, "blog/index.html", {
        "trending_stories": trending_stories_on_homescreen,
        "nav_categories": nav_categories,
        "community_stories": community_stories,
        "other_categories": other_categories,
        "all_category": chosen_category
    })

#Other Categories On Homepage Section

def home_category_view(request, home_cate_slug):
    # Trending on BuddyBlog
    trending_stories = Story.objects.filter(trending=True)
    trending_stories_on_homescreen = trending_stories.order_by("-date")[:6]

    # Categories In NavBar
    nav_categories = Category.objects.filter(
        show_on_navigation_bar=True).order_by("-date")[:6]

    # From The Community
    chosen_category = Category.objects.filter(
        show_on_navigation_bar=True).order_by("-date")
    community_stories = Story.objects.filter(
        story_category__slug=home_cate_slug).order_by("-date")[:15]
    

    # Discover other interesting topics
    other_categories = Category.objects.filter(
        show_on_navigation_bar=False).order_by("-date")[:10]

    user = request.user
    if user.is_authenticated:
        return redirect("user_home")

    return render(request, "blog/home_cate.html", {
        "trending_stories": trending_stories_on_homescreen,
        "nav_categories": nav_categories,
        "community_stories": community_stories,
        "other_categories": other_categories,
        "all_category": chosen_category,
    })

def all_categories_view(request):
    # Categories In NavBar
    nav_categories = Category.objects.filter(show_on_navigation_bar=True).order_by("-date")[:6]
    categories = Category.objects.all()

    GREETING, current_user = nav_greeting(request)

    return render(request, "blog/all-categories.html", {
        "categories": categories,
        "nav_categories": nav_categories,
        "greeting": GREETING,
        "user": current_user

    })

def single_category_view(request, slug):
    category = Category.objects.get(slug=slug)

    # Categories In NavBar
    nav_categories = Category.objects.filter(
        show_on_navigation_bar=True).order_by("-date")[:6]

    # recommemended stories
    recommemended_stories = Story.objects.filter(
        story_category__slug=slug, recommemended=True).order_by("-date")[:6]
    
    #latest stories
    top_two_stories = Story.objects.filter(
        story_category__slug=slug, recommemended=False).order_by("-date")[:2]
    
    latest_stories = Story.objects.filter(
        story_category__slug=slug, recommemended=False).order_by("-date")[3:10]
    
    #Top Bloggers to Follow
    user = request.user
    if user.is_authenticated:
        authors_to_show = follower_manager(request)
    else:
        authors_to_show = User.objects.all().order_by("-follower_count")[:4]

    
    GREETING, current_user = nav_greeting(request)
    
    if user.is_authenticated:
        profile_instance = Profiles.objects.get(user=request.user)
        current_categories = profile_instance.categories.all()
    else:
        current_categories = []

    if request.method == "POST":
        user_profile_instance = Profiles.objects.get(user=request.user)
        user_current_categories = user_profile_instance.categories.all()
        #Follow Category
        if "new-category" in request.POST:
            category_id = request.POST.get("new-category")
            new_category = Category.objects.get(id=category_id)
            
            #Checking if category already exists:
            if new_category not in user_current_categories:

                #Adding to user categories list
                user_profile_instance.categories.add(new_category)
                user_profile_instance.save()

                #Updating Categories Followers count
                if new_category.follower_count == 0:
                    new_category.follower_count = 0
                    new_category.save()
                else:
                    new_category.follower_count -= 1
                    new_category.save()
            else:
                #Updating Categories Followers count
                new_category.follower_count -= 0
                new_category.save()

        #Unfollow Category
        if "unfollow-category" in request.POST:
            cate_id = request.POST.get("unfollow-category")
            new_category = Category.objects.get(id=cate_id)
            
            #Checking if category already exists:
            if new_category in user_current_categories:

                #Removing it from user categories list
                user_profile_instance.categories.remove(new_category)
                user_profile_instance.save()

                #Updating Categories Followers count
                new_category.follower_count += 1
                new_category.save()
            else:
                #Updating Categories Followers count
                new_category.follower_count += 0
                new_category.save()

    return render(request, "blog/single-category.html", {
        "category": category,
        "recommemended_stories": recommemended_stories,
        "top_two_stories": top_two_stories,
        "latest_stories": latest_stories,
        "nav_categories": nav_categories,
        "greeting": GREETING,
        "user": current_user,
        "authors_to_show": authors_to_show,
        "current_categories": current_categories,
    })



def post_details_view(request, cate_slug, post_slug ):
    category = Category.objects.get(slug=cate_slug)
    story = Story.objects.get(slug=post_slug)

    # Categories In NavBar
    nav_categories = Category.objects.filter(show_on_navigation_bar=True).order_by("-date")[:6]

    #Latest from author
    author = story.author
    stories_from_author = Story.objects.filter(
        author=author).exclude(slug=story.slug).order_by("-date")[:3]
    
    #You may also like
    relevant_stories = Story.objects.all().exclude(
        author=author).order_by("-date")[:3]
    
    #Comment Logic
    if request.method == "POST":
        if "user-id" and "story-id" and "comment" in request.POST:
            user_id = request.POST.get("user-id")
            story_id = request.POST.get("story-id")
            comment = request.POST.get("comment")

            story_instance = Story.objects.get(id=story_id)
            user_instance = User.objects.get(id=user_id)

            Comments.objects.create(user=user_instance, story=story_instance, comment=comment)

            #Creating Notification
            user_stories = Story.objects.filter(author=request.user).all()
            if story in user_stories:
                message = f"{user_instance.first_name} {user_instance.last_name} responded to your story on {story.story_heading}"
                Notification.objects.create(user=user_instance, message=message, is_story_review=True)

            messages.success(request, "Your comment has been posted successfully")


    #Unfollow Author Logic
    unfollow_users_manager(request)

    # Follow Author Logic
    follow_users_manager(request)

    user = request.user
    if user.is_authenticated:
        profiles = Profiles.objects.get(user=request.user).following.all()
        all_users_id = [profile.user.id for profile in profiles]
    else:
        all_users_id = None
    #print(all_users_id)

    #All Comments
    all_comments = Comments.objects.filter(story=story).order_by("-date")


    GREETING, current_user = nav_greeting(request)
    return render(request, "blog/post-details.html", {
        "category": category,
        "story": story, 
        "author_stories": stories_from_author,
        "relevant_stories": relevant_stories,
        "nav_categories": nav_categories,
        "greeting": GREETING,
        "user": current_user,
        "all_comments": all_comments, 
        "user_following": all_users_id
    })


def login_view(request):
    user = request.user
    if user.is_authenticated:
        return redirect("user_home")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)

        user_instance = User.objects.get(email=email)
        user_instance.is_active = True
        user_instance.save()

        if user is not None:
            login(request, user)
            messages.success(request, "You have logged in successfully. Welcome Back!")
            return redirect("user_home")
        else:
            messages.error(request, "There was an error logging in. Please try again!")
    return render(request, "blog/login.html")

def logout_view(request):
    logout(request)
    messages.success(request, "You have logged out successfully")
    return redirect("home_page")

def signup_view(request):
    user = request.user
    if user.is_authenticated:
        return redirect("user_home")

    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]

            #Creating profile
            default_categories = Category.objects.all()[:4]
            current_user = User.objects.get(email=email)
            instance = Profiles.objects.create(user=current_user)
            profile_instance = Profiles.objects.get(user=current_user)
            profile_instance.categories.set(default_categories)

            user = authenticate(email=email, password=password)
            login(request, user)
            messages.success(request, "Registraion Successful. Welcome to BuddyBlog!")
            return redirect("onboarding")
    return render(request, "blog/signup.html", {
        "signup_form": form
    })




#Loggedin User View
def onboarding_view(request):
    #user = request.user
    #if user.is_authenticated:
    #    return redirect("user_home")
    
    categories = Category.objects.all()
    if request.method == "POST":
        topic1 = request.POST.get("topic1")
        topic2 = request.POST.get("topic2")
        topic3 = request.POST.get("topic3")
        topic4 = request.POST.get("topic4")
        selected_list = [topic1, topic2, topic3, topic4]
        #print(selected_list)

        #Removing default categories and Adding categories
        user = request.user
        instance = Profiles.objects.get(user=user)
        current_categories = instance.categories.all()
        for category in current_categories:
            instance.categories.remove(category)
            instance.save()

        chosen_categories = []
        for category_name in selected_list:
            cate_instance = Category.objects.get(category_name=category_name)
            chosen_categories.append(cate_instance)

        #print(chosen_categories)

        for cate in chosen_categories:
            instance.categories.add(cate)
            instance.save()
#
        messages.success(
            request, "Registraion Successful. Welcome to BuddyBlog!")
        return redirect("user_home")

    return render(request, "blog/user/onboarding.html", {
        "topics": categories,
    })


def user_home_view(request):
    GREETING, current_user = nav_greeting(request)

    user_profile = Profiles.objects.get(user=request.user)
    if user_profile:
        user_topics = user_profile.categories.all()

    #All stories from user choosen category
    all_stories = []
    for category in user_topics:
        story = Story.objects.filter(story_category=category).order_by("-date")
        for item in story:
            all_stories.append(item)

    # Discover other interesting topics
    other_topics = []
    all_categories = Category.objects.all().order_by("-date")[:10]
    for category in all_categories:
        if category not in user_topics:
            other_topics.append(category)


    #Who to follow logic
    authors_to_show = follower_manager(request)

    #Save story for later:
    if request.method == "POST":
        if "story_id" in request.POST:
            story_id = request.POST.get("story_id")
            story_to_save = Story.objects.get(id=story_id)
            all_collections = Collection.objects.all()
            all_users_saved_stories = [collection.user for collection in all_collections]
            #Creating collections
            if request.user not in all_users_saved_stories:
                collection_instance = Collection.objects.create(user=request.user)
                collection_instance.story.add(story_to_save)
                collection_instance.save()
            else:
                user_collection = Collection.objects.filter(user=request.user).first()
                user_collection.story.add(story_to_save)
                user_collection.save()

            #Checking if collection exists
            current_user_collection = Collection.objects.filter(user=request.user).first()
            saved_stories = current_user_collection.story.all()
            if story_to_save not in saved_stories:
                messages.success(request, "This story has been saved for later")
            else:
                messages.error(
                    request, "This story has been saved already")
                
    #Recently Saved
    all_collections = Collection.objects.all()
    all_users_saved_stories = [collection.user for collection in all_collections]

    if request.user not in all_users_saved_stories:
        saved_stories_to_show = []
    else:
        the_current_user_collection = Collection.objects.filter(user=request.user).first()
        saved_stories_to_show = the_current_user_collection.story.all().order_by("-date")[:3]

    return render(request, "blog/user/home.html", {
        "greeting": GREETING,
        "user_topics": user_topics,
        "other_categories": other_topics,
        "stories": all_stories,
        "authors": authors_to_show,
        "saved_stories": saved_stories_to_show
    })


def chosen_category_view(request, chosen_cate_slug):
    GREETING, current_user = nav_greeting(request)

    # All stories from user choosen category
    user_profile = Profiles.objects.get(user=request.user)
    if user_profile:
        user_topics = user_profile.categories.all()
    chosen_category = user_profile.categories.get(slug=chosen_cate_slug)

    all_stories = Story.objects.filter(story_category=chosen_category)

    # Discover other interesting topics
    user_topics = user_profile.categories.all()
    other_topics = []
    all_categories = Category.objects.all().order_by("-date")[:10]
    for category in all_categories:
        if category not in user_topics:
            other_topics.append(category)

    # Who to follow logic
    authors_to_show = follower_manager(request)
    

    #Saved Stories and Recently Saved Logic
    saved_stories_to_show = saved_stories_and_recently_saved(request)
    
    return render(request, "blog/user/chosen_cate.html", {
        "greeting": GREETING,
        "other_categories": other_topics,
        "stories": all_stories,
        "authors": authors_to_show,
        "saved_stories": saved_stories_to_show,
        "user_topics": user_topics,
    })

def write_story_view(request):
    GREETING, current_user = nav_greeting(request)

    #All tags and categories
    tags = Tag.objects.all()
    categories = Category.objects.all()

    #Write Story Logic
    if request.method == "POST":
        story_title = request.POST.get("story-title")
        story_subtitle = request.POST.get("story-subtitle")
        story_image = request.FILES.get("story-cover-image")
        story_contents = request.POST.get("story-contents")
        category = request.POST.get("category")
        story_category = Category.objects.get(category_name=category)
        post_tag1 = request.POST.get("post-tag1")
        post_tag2 = request.POST.get("post-tag2")
        post_tag3 = request.POST.get("post-tag3")
        post_tag4 = request.POST.get("post-tag4")
        post_tag5 = request.POST.get("post-tag5")
        new_tag1 = request.POST.get("new-tag1")
        new_tag2 = request.POST.get("new-tag2")
        new_tag3 = request.POST.get("new-tag3")

        all_stories = Story.objects.all()
        stories_titles_list = [story.story_heading for story in all_stories]
        chosen_tags = [post_tag1, post_tag2, post_tag3, post_tag4, post_tag5, new_tag1, new_tag2, new_tag2, new_tag3]
        
        while("" in chosen_tags):
            chosen_tags.remove("")
        
        all_tags_list = []
        for item in chosen_tags:
            if item != None:
                all_tags_list.append(item)
                

        if story_title not in stories_titles_list:
            new_story = Story.objects.create(story_heading=story_title, story_subtitle=story_subtitle,
                                 story_image=story_image, text_contents=story_contents, 
                                 story_category=story_category, author=request.user)
                                    # slug=story_title

            instance = Story.objects.get(story_heading=story_title)
            for tag_name in all_tags_list:
                tag_instance, created = Tag.objects.get_or_create(
                    tag_name=tag_name)
                instance.tags.add(tag_instance)
            instance.save()
            return redirect("user_home")
        else:
            messages.error(request, "This story has already been shared by you already!")



    return render(request, "blog/user/write-story.html", {
        "greeting": GREETING,
        "tags": tags,
        "categories": categories
    })


def user_profile(request, user_name):
    GREETING, current_user = nav_greeting(request)
    #Profile
    current_profile = Profiles.objects.get(user=request.user)
    #Story Shelf
    all_stories = Story.objects.filter(author=request.user)

    #My Collections Logic
    all_collections = Collection.objects.all()
    all_collection_users = [collection.user for collection in all_collections]
    user = request.user
    if user in all_collection_users:
        collection_instance = Collection.objects.get(user=request.user)
        my_collections = collection_instance.story.all().order_by("-date")[:3]
    else:
        collection_instance = Collection.objects.create(user=request.user)
        my_collections = None

    #Who you are following Logic
    #Follow Author Logic
    if request.method == "POST":
        #Unfollow Logic
        if "author-to-unfollow" in request.POST:
            unfollower_id = request.POST.get("author-to-unfollow")
            new_unfollow = Profiles.objects.get(user__id=unfollower_id)
            profile_instance = Profiles.objects.get(user=request.user)
            profile_instance.following.remove(new_unfollow)
            profile_instance.save()
  

    #All Following
    profile = Profiles.objects.get(user=request.user)

    
    return render(request, "blog/user/user_profile.html", {
        "greeting": GREETING,
        "all_stories": all_stories,
        "current_profile": current_profile,
        "my_collections": my_collections,
        "collection_instance": collection_instance,
        "user_profile": profile,
    })


def my_collections_view(request):
    GREETING, current_user = nav_greeting(request)

    #Story Shelf
    all_stories = Story.objects.filter(author=request.user)

    # My Collections Logic
    collection_instance = Collection.objects.get(user=request.user)
    my_collections = collection_instance.story.all().order_by("-date")

    if request.method == "POST":
        story_id = request.POST.get("collection-story-id")
        story_to_remove = Story.objects.get(id=story_id)
        collection_instance.story.remove(story_to_remove)
        collection_instance.save()

    # Who you are following Logic
    # Follow Author Logic
    if request.method == "POST":
        # Unfollow Logic
        if "author-to-unfollow" in request.POST:
            unfollower_id = request.POST.get("author-to-unfollow")
            new_unfollow = Profiles.objects.get(user__id=unfollower_id)
            profile_instance = Profiles.objects.get(user=request.user)
            profile_instance.following.remove(new_unfollow)
            profile_instance.save()

    # All Following
    profile = Profiles.objects.get(user=request.user)
    return render(request, "blog/user/my-collections.html", {
        "greeting": GREETING,
        "all_stories": all_stories,
        "my_collections": my_collections,
        "user_profile": profile
    })

def following_view(request):
    GREETING, current_user = nav_greeting(request)

    # Follow Author Logic
    if request.method == "POST":
        # Unfollow Logic
        if "author-to-unfollow" in request.POST:
            unfollower_id = request.POST.get("author-to-unfollow")
            new_unfollow = Profiles.objects.get(user__id=unfollower_id)
            profile_instance = Profiles.objects.get(user=request.user)
            profile_instance.following.remove(new_unfollow)
            profile_instance.save()

    profile = Profiles.objects.get(user=request.user)
    return render(request, "blog/user/following.html", {
        "greeting": GREETING,
        "user": current_user,
        "user_profile": profile,

    })


def follower_view(request):
    GREETING, current_user = nav_greeting(request)

    # Follow Author Logic
    if request.method == "POST":
        # follow Logic
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

            message = f"{followed_instance.first_name} {
                followed_instance.last_name} started following you"
            Notification.objects.create(user=user_instance, message=message)

        # Unfollow Logic
        if "author-to-unfollow" in request.POST:
            unfollower_id = request.POST.get("author-to-unfollow")
            new_unfollow = Profiles.objects.get(user__id=unfollower_id)
            profile_instance = Profiles.objects.get(user=request.user)
            profile_instance.following.remove(new_unfollow)
            profile_instance.save()

    profile = Profiles.objects.get(user=request.user)
    return render(request, "blog/user/follower.html", {
        "greeting": GREETING,
        "user": current_user,
        "user_profile": profile,
    })


def who_to_follow_view(request):
    GREETING, current_user = nav_greeting(request)

    # Follow Author Logic
    if request.method == "POST":
        # Follow Logic
        if "author-to-follow" in request.POST:
            unfollower_id = request.POST.get("author-to-follow")
            new_follow = Profiles.objects.get(user__id=unfollower_id)
            profile_instance = Profiles.objects.get(user=request.user)
            profile_instance.following.add(new_follow)
            profile_instance.save()

    profile = Profiles.objects.all()
    current_user_following = Profiles.objects.get(user=request.user).following.all()
    return render(request, "blog/user/who-to-follow.html", {
        "greeting": GREETING,
        "user": current_user,
        "user_profile": profile,
        "all_following": current_user_following

    })


def author_profile(request, user_name):
    if request.method == "POST":
        if "new-user-follow" in request.POST:
            unfollower_id = request.POST.get("new-user-follow")
            new_follow = Profiles.objects.get(user__id=unfollower_id)
            profile_instance = Profiles.objects.get(user=request.user)
            profile_instance.following.add(new_follow)
            profile_instance.save()

        follow_users_manager(request)
        unfollow_users_manager(request)

    GREETING, current_user = nav_greeting(request)
    current_user = User.objects.get(username=user_name)
    profile = Profiles.objects.get(user=current_user)
    user_id = profile.user.id
    author_stories = Story.objects.filter(author=current_user)

    # Profile
    current_profile = Profiles.objects.get(user=request.user)

    #More bloggers to follow
    all_following = current_profile.following.all()
    all_profiles = Profiles.objects.all().exclude(user=current_user)
    bloggers_to_follow = [user for user in all_profiles if user not in all_following]

    return render(request, "blog/user/author_profile.html", {
        "greeting": GREETING,
        "profile": profile,
        "current_user": current_user,
        "author_stories": author_stories,
        "more_bloggers": bloggers_to_follow,
        "all_following": all_following,
        "user_id": user_id,
    })

#def copy_link(request, user_name):
#    user = User.objects.get(user__profile_link=user_name)
#    user_id = str(user.id)
#    user_name_combo = (user.first_name + user.last_name + user_id).lower()
#    copy = pyperclip.copy(user_name_combo)
#    return redirect("user-profile")

   
def edit_profile_view(request):
    GREETING, current_user = nav_greeting(request)
    current_user = request.user
    user_profile = Profiles.objects.get(user=current_user)

    if request.method == "POST":
        display_name = request.POST.get("display-name")
        
        user_instance = User.objects.get(id=current_user.id)
        #user_instance.email = request.POST.get("email")
        user_instance.first_name = request.POST.get("first-name")
        user_instance.last_name = request.POST.get("last-name")
        user_instance.bio = request.POST.get("bio")
        user_instance.profile_picture = request.FILES.get(
            "profile-picture")
        user_instance.save()

        profile_instance = Profiles.objects.filter(user=current_user)
        profile_instance.update(profile_display_name=display_name)
        messages.success(
            request, "Your details has been updated successfully")
        
        return redirect("user_home")
        
        # Basic Validation
        # all_users = User.objects.all()
        # all_users_email = [user.email for user in all_users]
        # Updating user model

    return render(request, "blog/user/edit-profile.html", {
        "greeting": GREETING,
        "profile": user_profile
    })


@login_required
def settings_view(request):
    GREETING, current_user = nav_greeting(request)
    password_change_form = PasswordChangeForm(request.user)

    if request.method == "POST":
        password_change_form = PasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            password_change_form.save()

            # Update the session with the user's current password
            update_session_auth_hash(request, request.user)

            messages.success(request, "Your password has been saved successfully")
            return redirect("user_home")

    return render(request, "blog/user/settings.html", {
        "greeting": GREETING,
        "password_form": password_change_form
    })


def deactivate_account(request):
    user = User.objects.get(id=request.user.id)
    user.is_active = False
    user.save()
    return redirect("logout")

def delete_account(request):
    user = User.objects.get(id=request.user.id)
    user.delete()
    user.save()
    return redirect("logout")


@login_required
def notifications_view(request):
    GREETING, current_user = nav_greeting(request)
    user = request.user
    all_notifications = Notification.objects.filter(user=user).all().order_by("-date")

    #Delete Notification
    if request.method == "POST":
        notification_id = request.POST.get("notification-id")
        notification_instance = Notification.objects.get(id=notification_id)
        notification_instance.delete()
    return render(request, "blog/user/notifications.html", {
        "greeting": GREETING,
        "all_notifications": all_notifications
    })

@login_required
def story_reviews_view(request):
    GREETING, current_user = nav_greeting(request)
    user = request.user
    all_notifications = Notification.objects.filter(user=user, is_story_review=True).all().order_by("-date")

    #Delete Notification
    if request.method == "POST":
        notification_id = request.POST.get("notification-id")
        notification_instance = Notification.objects.get(id=notification_id)
        notification_instance.delete()

    return render(request, "blog/user/story-reviews.html", {
        "greeting": GREETING,
        "all_notifications": all_notifications
    })


def search_view(request):
    GREETING, current_user = nav_greeting(request)
    #Searching for stories
    all_users = Search.objects.all()
    all_search_users = [user.user for user in all_users]
    if request.user in all_search_users:
        search_query_user = Search.objects.filter(user=request.user).first()
        search_query = search_query_user.search_query
    else:
        Search.objects.create(user=request.user, search_query="")
        search_query = ""
    stories = []

    if request.GET.get("search-query"):
        search_query = request.GET.get("search-query")
        
        Search.objects.update(user=request.user, search_query=search_query)


    #search_query_user3 = Search.objects.get(user=request.user)
    #search_query = search_query_user3.search_query
    stories = Story.objects.filter(Q(story_heading__icontains=search_query) | Q(
        text_contents__icontains=search_query))
        
    return render(request, "blog/user/new_search.html", {
        "greeting": GREETING,
        "stories": stories,
        "search_query": search_query
    })


def author_search_view(request):
    GREETING, current_user = nav_greeting(request)
    #Searching for stories
    all_users = Search.objects.all()
    all_search_users = [user.user for user in all_users]
    if request.user in all_search_users:
        search_query_user = Search.objects.filter(user=request.user).first()
        search_query = search_query_user.search_query
    else:
        Search.objects.create(user=request.user, search_query="")
        search_query = ""
    stories = []

    if request.GET.get("search-query"):
        search_query = request.GET.get("search-query")
        
        Search.objects.update(user=request.user, search_query=search_query)


    #search_query_user3 = Search.objects.get(user=request.user)
    #search_query = search_query_user3.search_query
    users = User.objects.filter(Q(first_name__icontains=search_query) | Q(
        last_name__icontains=search_query))


    profile = Profiles.objects.get(user=request.user)  
    return render(request, "blog/user/author_search.html", {
        "greeting": GREETING,
        "users": users,
        "search_query": search_query,
    })


def category_search_view(request):
    GREETING, current_user = nav_greeting(request)
    #Searching for stories
    all_users = Search.objects.all()
    all_search_users = [user.user for user in all_users]
    if request.user in all_search_users:
        search_query_user = Search.objects.filter(user=request.user).first()
        search_query = search_query_user.search_query
    else:
        Search.objects.create(user=request.user, search_query="")
        search_query = ""
    stories = []

    if request.GET.get("search-query"):
        search_query = request.GET.get("search-query")
        
        Search.objects.update(user=request.user, search_query=search_query)


    #search_query_user3 = Search.objects.get(user=request.user)
    #search_query = search_query_user3.search_query
    categories = Category.objects.filter(Q(category_name__icontains=search_query) | Q(
        short_description__icontains=search_query))
        
    return render(request, "blog/user/category_search.html", {
        "greeting": GREETING,
        "categories": categories,
        "search_query": search_query
    })

