from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserRegistrationSerializer, RoleSerializer
from .models import Role, UserRole, TokenBlacklist
from .permissions import IsAdminUser

User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    """User registration endpoint"""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        # Assign default role
        default_role, created = Role.objects.get_or_create(
            name='user',
            defaults={'description': 'Default user role'}
        )
        UserRole.objects.create(user=user, role=default_role)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)

class UserProfileView(generics.RetrieveUpdateAPIView):
    """User profile management"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """Logout endpoint - blacklist token"""
    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            # Add to our blacklist table
            TokenBlacklist.objects.create(
                token=str(token),
                expires_at=token.access_token.payload['exp'],
                user=request.user
            )
            
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_permissions_view(request):
    """Get user permissions and roles"""
    user_roles = UserRole.objects.filter(user=request.user).select_related('role')
    roles_data = []
    all_permissions = set()
    
    for user_role in user_roles:
        role_data = {
            'name': user_role.role.name,
            'description': user_role.role.description,
            'assigned_at': user_role.assigned_at
        }
        roles_data.append(role_data)
        all_permissions.update(user_role.role.permissions.get('permissions', []))
    
    return Response({
        'user_id': request.user.id,
        'username': request.user.username,
        'email': request.user.email,
        'roles': roles_data,
        'permissions': list(all_permissions),
        'is_staff': request.user.is_staff,
        'is_superuser': request.user.is_superuser
    })

class RoleManagementView(generics.ListCreateAPIView):
    """Role management (admin only)"""
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdminUser]

@api_view(['POST'])
@permission_classes([IsAdminUser])
def assign_role_view(request):
    """Assign role to user (admin only)"""
    user_id = request.data.get('user_id')
    role_name = request.data.get('role_name')
    
    try:
        user = User.objects.get(id=user_id)
        role = Role.objects.get(name=role_name)
        
        user_role, created = UserRole.objects.get_or_create(
            user=user,
            role=role,
            assigned_by=request.user
        )
        
        if created:
            return Response({
                'message': f'Role {role_name} assigned to user {user.username}'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'message': f'User {user.username} already has role {role_name}'
            }, status=status.HTTP_200_OK)
            
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Role.DoesNotExist:
        return Response({'error': 'Role not found'}, status=status.HTTP_404_NOT_FOUND)
