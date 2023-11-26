from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterForm, LoginForm, PaymentForm
from .models import Clients, Invoices, Payments
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            login = form.cleaned_data['login']
            hash_password = form.cleaned_data['password']

            clients_count = Clients.objects.filter(login=login, hash_password=hash_password).count()
            if clients_count == 0:
                new_client = Clients.objects.create(name=name, login=login, hash_password=hash_password)
                return redirect('/')
            else:
                raise Exception('Логин и пароль уже существуют')
        else:
            raise Exception('Данные некорректны')

    else:
        form = RegisterForm()
        return render(request, 'main/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            login = form.cleaned_data['login']
            password = form.cleaned_data['password']

            try:
                client = Clients.objects.get(login=login, hash_password=password)

                response = redirect('/')
                response.set_cookie('auth', client.id)

                return response

            except ObjectDoesNotExist:
                return HttpResponse('Логин или пароль введены неверно')
    else:
        form = LoginForm()
        return render(request, 'main/login.html', {'form': form})


def index(request):
    if request.method == 'POST':
        response = HttpResponse('Войдите в аккаунт')
        response.delete_cookie('auth')

        return response

    client_id = request.COOKIES.get('auth')
    if client_id is None:
        return HttpResponse('Войдите в аккаунт')
    else:
        client = Clients.objects.get(id=client_id)
        invoices = list(Invoices.objects.filter(client_id__id=client_id))

        return render(request, 'main/index.html', {'name': client.name, 'invoices': invoices})


def invoice(request, pk):
    invoice = Invoices.objects.get(id=pk)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment_sum = form.cleaned_data['payment_sum']

            if payment_sum < invoice.amount:
                invoice.amount -= payment_sum
            else:
                invoice.amount = 0
                invoice.full_payment_date = timezone.now()

            invoice.save()

            payment = Payments.objects.create(
                description='Платёж за газ',
                invoice_id=invoice,
                amount=payment_sum,
                payment_date=timezone.now()
            )
        else:
            raise Exception('Ошибка при заполнении формы')
    else:
        form = PaymentForm()

    all_payments = list(Payments.objects.filter(invoice_id__id=invoice.id).order_by('-payment_date'))

    return render(
        request,
        'main/invoice.html',
        {
            'invoice': invoice,
            'form': form,
            'all_payments': all_payments
        }
    )
