from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from core.models import Group, UserGroup, Expense
from core.serializers import GroupSerializer, UserGroupSerializer, ExpenseSerializer
from core.settlements import get_settlements_for_group
from user.models import User


# Create your views here.


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def post(self, request, *args, **kwargs):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'],url_name='delete')
    def delete_group(self,request,pk=None):
        delete_group = Group.objects.get(pk=pk)
        if delete_group:
            delete_group.delete()
        return Response({"detail": "Group and its associate records have been deleted."},status=status.HTTP_204_NO_CONTENT)


class UserGroupViewSet(viewsets.ModelViewSet):
    queryset = UserGroup.objects.all()
    serializer_class = UserGroupSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path="users")
    def get_group_users(self, request, pk=None):
        user_groups = UserGroup.objects.filter(group_id=pk).values('user_id')

        if not user_groups.exists():
            return Response({"detail": "No users found for this group."}, status=status.HTTP_404_NOT_FOUND)

        user_ids = [ug['user_id'] for ug in user_groups]
        users = User.objects.filter(id__in=user_ids).values()

        return Response(users, status=status.HTTP_200_OK)



class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path="settlements")
    def get_settlements(self, request, pk=None):
        expenses = Expense.objects.filter(group_id=pk).values().all()
        if not expenses.exists():
            return Response({"detail": "No expense found for this group."}, status=status.HTTP_404_NOT_FOUND)
        settlements = get_settlements_for_group(expenses, request.user.id)
        return Response(settlements,status.HTTP_200_OK)