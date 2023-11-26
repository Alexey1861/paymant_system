from django.db import models


class Clients(models.Model):
    name = models.CharField(max_length=100)
    login = models.CharField(max_length=100)
    hash_password = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Клиенты'
        ordering = ['name']
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        unique_together = ['login', 'hash_password']


class Invoices(models.Model):
    description = models.CharField(max_length=100)
    client_id = models.ForeignKey(Clients, on_delete=models.CASCADE)
    amount = models.IntegerField()
    creation_date = models.DateTimeField()
    full_payment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.description

    class Meta:
        db_table = 'Счета на оплату'
        ordering = ['creation_date']
        verbose_name = 'Счёт на оплату'
        verbose_name_plural = 'Счета на оплату'


class Payments(models.Model):
    description = models.CharField(max_length=100)
    invoice_id = models.ForeignKey(Invoices, on_delete=models.CASCADE)
    amount = models.IntegerField()
    payment_date = models.DateTimeField()

    def __str__(self):
        return self.description

    class Meta:
        db_table = 'Платежи'
        ordering = ['-payment_date']
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'
