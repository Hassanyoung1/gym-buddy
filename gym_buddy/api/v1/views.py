from rest_framework import viewsets
from users.models import CustomUser, Friendship
from workouts.models import Workout, Exercise
from groups.models import Group, GroupMembership
from rewards.models import Reward
from .serializers import UserSerializer, FriendshipSerializer, WorkoutSerializer, ExerciseSerializer, GroupSerializer, GroupMembershipSerializer, RewardSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get', 'put'], url_path='me')
    def manage_profile(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)


class FriendshipViewSet(viewsets.ModelViewSet):
    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='send-request')
    def send_request(self, request):
        user = request.user
        friend_id = request.data.get('friend_id')
        friend = CustomUser.objects.get(id=friend_id)
        if not Friendship.objects.filter(user=user, friend=friend).exists():
            Friendship.objects.create(user=user, friend=friend)
            return Response({"status": "friend request sent"})
        return Response({"status": "friend request already sent"}, status=400)

    @action(detail=False, methods=['post'], url_path='accept-request')
    def accept_request(self, request):
        user = request.user
        friend_id = request.data.get('friend_id')
        friendship = Friendship.objects.get(user=friend_id, friend=user)
        friendship.status = 'accepted'
        friendship.save()
        return Response({"status": "friend request accepted"})

    @action(detail=False, methods=['post'], url_path='reject-request')
    def reject_request(self, request):
        user = request.user
        friend_id = request.data.get('friend_id')
        friendship = Friendship.objects.get(user=friend_id, friend=user)
        friendship.delete()
        return Response({"status": "friend request rejected"})


class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], url_path='complete')
    def complete_workout(self, request, pk=None):
        workout = self.get_object()
        workout.completed = True
        workout.save()
        # Logic for awarding points/rewards
        return Response({"status": "workout completed"})

class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='join')
    def join_group(self, request):
        user = request.user
        group_id = request.data.get('group_id')
        group = Group.objects.get(id=group_id)
        if not GroupMembership.objects.filter(user=user, group=group).exists():
            GroupMembership.objects.create(user=user, group=group)
            return Response({"status": "joined group"})
        return Response({"status": "already in group"}, status=400)

    @action(detail=False, methods=['post'], url_path='leave')
    def leave_group(self, request):
        user = request.user
        group_id = request.data.get('group_id')
        group = Group.objects.get(id=group_id)
        membership = GroupMembership.objects.get(user=user, group=group)
        membership.delete()
        return Response({"status": "left group"})

class GroupMembershipViewSet(viewsets.ModelViewSet):
    queryset = GroupMembership.objects.all()
    serializer_class = GroupMembershipSerializer

class RewardViewSet(viewsets.ModelViewSet):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='my-rewards')
    def my_rewards(self, request):
        user = request.user
        rewards = Reward.objects.filter(user=user)
        serializer = RewardSerializer(rewards, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='redeem')
    def redeem_reward(self, request):
        user = request.user
        reward_id = request.data.get('reward_id')
        reward = Reward.objects.get(id=reward_id, user=user)
        # Logic for redeeming the reward
        return Response({"status": "reward redeemed"})
