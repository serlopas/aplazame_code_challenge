# Generated by Django 4.0.3 on 2022-03-19 19:49

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wallets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Operations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('operation_type', models.CharField(choices=[('Top-up', 'Top-up'), ('Charge', 'Charge')], db_index=True, max_length=16)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('success', models.BooleanField()),
                ('error_reason', models.CharField(max_length=256)),
                ('wallet_from', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='operations_from', to='wallets.wallet')),
                ('wallet_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='operations_to', to='wallets.wallet')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]