from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import AuthUsuarios
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, JsonResponse

from django.http import HttpResponseRedirect

from django.http import HttpResponse

def health_check(request):
    return HttpResponse("OK")


class LoginView(APIView):
    def post(self, request):
        user_login = request.POST.get('user_login')
        user_password = request.POST.get('user_password')

        if not user_login or not user_password:
            return Response({'error': 'user_login e user_password são obrigatórios.'}, status=400)

        try:
            user = AuthUsuarios.objects.get(user_login=user_login)
        except AuthUsuarios.DoesNotExist:
            return Response({'error': 'Usuário ou senha inválidos.'}, status=400)

        if check_password(user_password, user.user_password):
            response = HttpResponseRedirect('/index/')
            response.set_cookie('id_user', user.id_user)
            response.set_cookie('name_user', user.user_login)
            return response
        else:
            return Response({'error': 'Usuário ou senha inválidos.'}, status=400)
 

