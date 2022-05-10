from django.urls import path
from .views import *

app_name = 'api'

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/admin/login/', AdminLoginView.as_view(), name='admin-login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/sign-up/', SignupView.as_view(), name='auth-sign-up'),
    
    #OTP
    path('user/verify-otp/', VarifyOtpView.as_view(), name="verify-otp"),
    path('user/send-otp-to-old-user/', SendOtpForOldUser.as_view(), name="send-otp-to-old-user"),
    path('user/set-password/', SetUserPasswordView.as_view(), name="set-password"),
    path('user/add-user-details/', AddUserDetialsView.as_view(), name="add-user-details"),
    
    #Forgot-password
    path('user/forgot-password/',ForgotPasswordView.as_view(), name="forgot-password"),
    path('user/forgot-verify-otp/',ForgotVerifyOtpView.as_view(), name="forgot-password-verify-otp"),
    path('user/update-password/', ChangePasswordView.as_view(), name="change-password"),
    path('user/change-password/',UpdatePasswordView.as_view(), name="update-password"),

    #Profile
    path('user/get-user-details-by-token/',GetUserDetialsByTokenView.as_view(), name="get-user-details-by-token"),
    path('user/update-user-details/<int:user_id>/',UpdateUsersDetailsView.as_view(), name="update-user-details"),
    path('user/get-all-teacher-classes-by-token/',GetAllTeacherClassDetails.as_view(), name="update-user-details"),

    # #organisation
    # path('branch/create-branch/', CreateGetBranchView.as_view(), name="create-branch"),
    # path('branch/get-all-branches/', CreateGetBranchView.as_view(), name="get-all-branches"),
    # path('class/create-classes/', CreateGetClassesView.as_view(), name="create-classes"),
    # path('class/get-all-classes-by-branch-id/<int:branch_id>/', CreateGetClassesView.as_view(), name="get-all-classes-by-branch-id"),
    # path('class/create-sections/', CreateGetSectionsView.as_view(), name="create-sections"),
    # path('class/get-all-sections-by-class-id/<int:class_id>/', CreateGetSectionsView.as_view(), name="get-all-sections-by-class-id"),
    
    #role
    path('role/get-all-roles/', RoleListView.as_view(), name="get-all-role"),
    path('role/create-role/', RoleCreateView.as_view(), name="create-role"),

    #education-history
    path("education-history/create", CreateEducationView.as_view(), name="create-education-history"),
    
    #uploadMedia
    path('upload/media/', UploadMediaView.as_view(), name="upload-media"),
    path('delete-media/<int:pk>/', DeleteMediaView.as_view(), name="delete-media"),

    # Bitgo 
]
