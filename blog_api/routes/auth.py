from ninja import Router
from ninja.errors import ValidationError
from blog_api.schemas.auth import (
    UserLoginSchema,
    UserSchema,
    UserRegistrationSchema
)

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# python-slugify

router = Router(tags=['Auth'])

@router.post('/auth/login/', response=UserSchema)
def login_user(request, login_data: UserLoginSchema):
    user = authenticate(
        username=login_data.username,
        password=login_data.password
    )
    if user is None:
        raise ValidationError('user not found')
    
    login(request, user)
    
    return user


@router.post('/auth/register/', response=UserSchema)
def register_user(request, register_data: UserRegistrationSchema):
    if User.objects.filter(username=register_data.username).exists():
        raise ValidationError('User with this username already registered')
    
    if "@" not in register_data.email and '.' not in register_data.email:
        raise ValidationError('email is incorrect')
        
    data = register_data.dict()  # получаем словарь отправленных данных
    
    password1 = data.pop('password1')
    password2 = data.pop('password2')
    
    if password1 != password2:
        raise ValidationError('passwords are not same')
    
    user = User.objects.create(**data)
    user.set_password(password1)
    user.save()
    return user
    
@router.post('/auth/logout/')
def user_logout(request):
    logout(request)
    return {'is_authenticated': request.user.is_authenticated}

# pip uninstall ninja

# сделать получение всех статей пользователя

# user_id
# 
# list[ArticleSchema]