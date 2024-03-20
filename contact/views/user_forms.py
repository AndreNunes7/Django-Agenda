from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from contact.forms import RegisterForm, RegisterUpdateForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from contact.forms import ContactForm  # Importe o formulário ContactForm aqui



def register(request):

    form = RegisterForm()

    # messages.info(request,'Texto')
    # messages.success(request,'Texto')
    # messages.warning(request,'Texto')
    # messages.error(request,'Texto')

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Usuario registrado")
            return redirect('contact:login')

    return render(
        request,
        'contact/register.html',
        {
            'form': form

        }
    )




@login_required(login_url='contact:login')
def create(request):
    form_action = reverse('contact:create')

    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)

        if form.is_valid():
            contact = form.save(commit=False)
            contact.owner = request.user
            contact.save()

            # Adicione uma mensagem de sucesso
            messages.success(request, 'Contato adicionado com sucesso.')

            return redirect('contact:update', contact_id=contact.pk)
        else:
            messages.error(request, 'Erro ao adicionar contato. Por favor, corrija os erros abaixo.')

    context = {
        'form': ContactForm(),
        'form_action': form_action,
    }

    return render(
        request,
        'contact/create.html',
        context
    )






@login_required(login_url='contact:login')
def user_update(request):
    form = RegisterUpdateForm(instance=request.user)

    if request.method != "POST":
        return render(
            request,
            'contact/user_update.html',
            {
                'form': form
            }
        )

    form = RegisterUpdateForm(data=request.POST, instance=request.user)

    if not form.is_valid():
        return render(
            request,
            'contact/user_update.html',
            {
                'form': form
            }
        )
    
    form.save()

    return redirect('contact:user_update')



def login_view(request):

    form = AuthenticationForm(request)

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            messages.success(request, "Logado com sucesso!")
            return redirect('contact:index')

        messages.error(request, 'Login Inválido')

    return render(
        request,
        'contact/login.html',
        {
            'form': form
        }
    )


@login_required(login_url='contact:login')
def logout_view(request):
    auth.logout(request)
    return redirect('contact:login')