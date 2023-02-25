# Generated by Django 3.2.6 on 2023-02-10 12:35

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0005_auto_20230210_1528'),
    ]

    operations = [
        migrations.CreateModel(
            name='DrugItemsSales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('drug', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sold', to='pharmacy.stock')),
            ],
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('customer_name', models.CharField(default='anonymous', max_length=55)),
                ('sub_total', models.FloatField(default=0)),
                ('grand_total', models.FloatField(default=0)),
                ('tendered_amount', models.FloatField(default=0)),
                ('amount_change', models.FloatField(default=0)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Sales',
                'verbose_name_plural': 'Sales',
            },
        ),
        migrations.DeleteModel(
            name='DrugSales',
        ),
        migrations.AddField(
            model_name='drugitemssales',
            name='sale_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pharmacy.sales'),
        ),
    ]