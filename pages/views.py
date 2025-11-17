from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect

def login_view(request):
    return render(request, "login/login.html")

def logout_view(request):
    logout(request) # Função pronta do django, encerra a sessão do usuário autenticado
    response =  redirect("/") # resposta redirecionando para a raiz

    # Deletando os cookies criados
    response.delete_cookie("id_user")
    response.delete_cookie("name_user")
    return response


def index_view(request):
    id_user = request.COOKIES.get('id_user')
    name_user = request.COOKIES.get('name_user')  

    if not id_user or not name_user:
        return redirect("/")

    return render(request, 'index/index.html', {
        'id_user': id_user,
        'name_user': name_user,
    })

def historico_view(request):
    id_user = request.COOKIES.get('id_user')
    name_user = request.COOKIES.get('name_user')  

    if not id_user or not name_user:
        return redirect("/")

    return render(request, 'historico/historico.html', {
        'id_user': id_user,
        'name_user': name_user,
    })
