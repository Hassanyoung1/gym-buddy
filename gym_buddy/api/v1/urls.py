from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, FriendshipViewSet, WorkoutViewSet, ExerciseViewSet, GroupViewSet, GroupMembershipViewSet, RewardViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'friendships', FriendshipViewSet)
router.register(r'workouts', WorkoutViewSet)
router.register(r'exercises', ExerciseViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'group_memberships', GroupMembershipViewSet)
router.register(r'rewards', RewardViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
