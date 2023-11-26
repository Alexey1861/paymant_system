from django import forms


class RegisterForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label='Имя',
        widget=forms.TextInput(attrs={'placeholder': 'Введите имя'})
    )

    login = forms.CharField(
        max_length=100,
        label='Логин',
        widget=forms.TextInput(attrs={'placeholder': 'Введите логин'})
    )

    password = forms.CharField(
        max_length=200,
        label='Пароль',
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'})
    )


class LoginForm(forms.Form):
    login = forms.CharField(
        max_length=100,
        label='Логин',
        widget=forms.TextInput(attrs={'placeholder': 'Введите логин'})
    )

    password = forms.CharField(
        max_length=100,
        label='Пароль',
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'})
    )


class PaymentForm(forms.Form):
    payment_sum = forms.IntegerField(
        label='Внести денег на сумму',
        widget=forms.NumberInput(attrs={'placeholder': 'Введите сумму'})
    )
