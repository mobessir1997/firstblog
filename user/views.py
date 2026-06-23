from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, ProfileSerializer, UseInfoSerializer

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'অ্যাকাউন্ট তৈরি হয়েছে, {username}! এখন লগইন করুন।')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'user/register.html', {'form':form})
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'আপনার প্রোফাইল সফলভাবে আপডেট করা হয়েছে!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        context = {
            'u_form' : u_form,
            'p_form' : p_form
        }
        return render(request, 'user/profile.html', context )
    

class RegisterApi(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = AllowAny

class ProfileApi(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsAuthenticatedOrReadOnly]
    def get_object(self):
        return self.request.user.profile
class UserApi(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UseInfoSerializer
    permission_classes = [IsAuthenticated, IsAuthenticatedOrReadOnly]
    def get_object(self):
        return self.request.user
    
