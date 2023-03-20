from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import  ProfileForm,PostForm,UserForm,CommentForm,ReplyForm
from .models import Profile, Post,Comment,Reply
from django.contrib.auth.models import User
from datetime import datetime

# -----------------Home---------------------------

@login_required
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    form = PostForm()
    # print(form,'pppppppppppppppppppppppppppppppp')
    # comments=Comment.objects.all().count()
    # print(comments,"iuggggggggggggggggggg")
    # comment_count = Comment.objects.filter(active=True).count()
    # print(comment_count,"dddddddddddddddddddddd")
    if request.user.id is not None:
        user_id=request.user.id

        liked_list=[]
        like_post=Post.objects.filter(likes=user_id)
        for i in like_post:
            liked_list.append(i.title)
        # print(like_post)
        # print("lnkjanjknjknkjsbahjbjkbsakj-----------------")
        comment_form = CommentForm()
        form = ReplyForm()

        context = {'posts': posts,'user_id':user_id,'liked_list':liked_list,'comment_form':comment_form ,'form':form}
    else:
        comment_form = CommentForm()
        context = {'posts': posts}
    # print("bhjasbhjbkjsha",posts)
    return render(request, 'home.html', context)




# -----------------Register---------------------------


def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            login(request, user)
            return redirect('login')
    else:
        user_form = UserForm()
        profile_form = ProfileForm()

    return render(request, 'registration.html', {'user_form': user_form,'profile_form': profile_form})





# -----------------Login--------------------------

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            # if user.is_staff and not user.is_superuser:
            #     messages.error(request, 'Admin login not allowed')
            # else:   
                login(request, user)
                return redirect('profile')

        else:
            messages.error(request, 'Invalid login credentials')
    return render(request, 'login.html')



# -----------------update profile---------------------------

@login_required
def update(request):
    profile = get_object_or_404(Profile, user=request.user)
    user_name=request.user
    # user=get_object_or_404(User)
    # print(user,"slknldslknskllkdn")
    if request.method == 'POST':
        # print(request.POST,"-----------------------------------")
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
    else:
        # user_form = UserForm(instance=user)
        form = ProfileForm(instance=profile)
        # messages.success(request, 'Username and password is incorrect')
    context = {'form': form,'name':user_name}
    return render(request, 'update.html', context)




# -----------------Profile---------------------------

@login_required
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    profile_details=Profile.objects.filter(user=request.user)
    user = User.objects.filter(username=request.user)
    print(profile)
    context = {'details':profile_details,'user_details':user}
    return render(request,'profile.html',context)





# -----------------Create post---------------------------


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.profile
            post.save()
            messages.success(request, 'Post created successfully')
            return redirect('home')
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, 'create_post.html', context)




# -----------------Like post---------------------------

@login_required
def like_post(request, id):
    # print(id,"idddddddddddddddd")
    post = get_object_or_404(Post, id=id)
    # print('pooooooooooossstttttttt',post)
    if request.method == 'POST':
        # print(request.method,"----------------------")
        if request.user in post.likes.all():
            # user has already liked the post, remove their like
            post.likes.remove(request.user)
        else:
            # user has not liked the post yet, add their like and remove dislike
            post.likes.add(request.user)
            # post.dislikes.remove(request.user)
    # print("loginnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")
    return redirect('home')




# -----------------Delete Post--------------------------


@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully')
        return redirect('home')

    context = {'post': post}
    return render(request, 'delete_post.html', context)




# -----------------Logout---------------------------


def user_logout(request):
    logout(request)
    return redirect('login')




# -----------------Comment_creation--------------------------

@login_required
def comment_view(request, id):
    print("xsh xs xshgsxnhzsxgnhzamsxnzhAM")
    post=get_object_or_404(Post,id=id)
    
    # post=Post.objects.filter(id=id).first()
    
    # List of active comments for this post
    comment = Comment.objects.filter(post=post)
    print(comment,"comment---------------------")
    total_comments = comment.count()
    print(total_comments,"total_comments")
     
    # comments = post.comments.filter(active=True)
    # print(comments,'cccccccccccccccccccccccccccccccccccc')
    new_comment = None
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
            print(new_comment,'newwwwwwwwwwwwwwwwwwwwwww')
            # redirect to same page and focus on that comment
            return redirect('home')
  
    else:
            
            comment_form = CommentForm()
    return redirect('home')
    # return render(request,"home.html",{'total_comments':total_comments})





# -----------------For Reply---------------------------

@login_required
def reply(request,id):
    comment=get_object_or_404(Comment,id=id)
    print(comment,'commmmmmmmmmmmmmmmmmmmmeeennnttttttttt')
    reply= Comment.objects.all()
    print(reply,'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy')
    if request.method == "POST":

        form = ReplyForm(request.POST)
        print(form,'ffffffffffffffffffffffffffffffffffffff')

        if form.is_valid():
            reply = form.save(commit=False)
            print(reply,'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr')
            reply.author = request.user
            # reply.post = Post(id=post_id)
            reply.comment = Comment(id=id)
            reply.save()
            return redirect('home')
    else:
            form = ReplyForm()
    return redirect('home')




# -----------------Like comment--------------------------

@login_required
def like_comment(request, id):
    comment = Comment.objects.get(pk=id)
    user = request.user
    if user in comment.likes.all():
        comment.likes.remove(user)
    else:
        comment.likes.add(user)
    return redirect('home')



# -----------------like reply---------------------------

@login_required
def like_reply(request, id):
    reply = Reply.objects.get(pk=id)
    user = request.user
    if user in reply.likes.all():
        reply.likes.remove(user)
    else:
        reply.likes.add(user)
    return redirect('home')



#----------------Delete comment----------
@login_required
def delete_comment(request, id):
    comment= get_object_or_404(Comment, id=id)

    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Post deleted successfully')
        return redirect('home')

    context = {'post': comment}
    return render(request, 'delete_post.html', context)



#----------------Delete reply----------
@login_required
def delete_reply(request, id):
    reply= get_object_or_404(Reply, id=id)

    if request.method == 'POST':
        reply.delete()
        messages.success(request, 'Post deleted successfully')
        return redirect('home')

    context = {'post': reply}
    return render(request, 'delete_post.html', context)



@login_required
def post_view(request, id):
    post = get_object_or_404(Post, id=id)
    print(post,"&&&&&&&&&&&&&&&&&&&&&&")
    post.views += 1
    post.save()
    comment_form = CommentForm()
    form = ReplyForm()
    return render(request, 'post_view.html', {'post': post,'comment_form':comment_form ,'form':form})