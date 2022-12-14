from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name = 'index'),
    path('main/', views.main, name = 'main'),
    path('login_student/', views.login_student, name = 'login_student'),
    path('login_startup/', views.login_startup, name = 'login_startup'),
    path('register_student/', views.register_student, name = 'register_student'),
    path('register_startup/', views.register_startup, name = 'register_startup'),
    path('profile/<int:profileId>', views.profile, name = 'profile'),
    path('profileEdit/<int:profileId>', views.profileEdit, name = 'profile-edit'),
    path('jobPosting/<int:jobPostingId>', views.jobPosting, name = 'jobPosting'),
    path('createJobPosting/', views.createJobPosting, name = 'create-jobPosting'),
    path('editJobPosting/<int:jobPostingId>', views.editJobPosting, name = 'edit-jobPosting'),
    path('accept/<int:userId>/<int:jobPostingId>/', views.accept, name = 'accept'),
    path('reject/<int:userId>/<int:jobPostingId>/', views.reject, name = 'reject'),
    path('rateUser/<int:userId>/<int:rating>/<str:feedbackField>', views.rateUser, name = 'rate-user'),
    path('upskill/', views.upskill, name = 'upskill'),
    path('shell/', views.shell),
]
