# Generated by Django 4.2.8 on 2023-12-23 00:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone_no', models.CharField(max_length=15)),
                ('email_id', models.EmailField(max_length=254, unique=True)),
                ('address', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_no', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('brokerage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agents', to='listings.agency')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_no', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('credit_score', models.IntegerField()),
                ('income', models.DecimalField(decimal_places=2, max_digits=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Guarantor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_no', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('income', models.DecimalField(decimal_places=2, max_digits=10)),
                ('credit_score', models.IntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HouseOwner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_no', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_for_rent', models.BooleanField(default=False)),
                ('is_sold', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('agent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='listings', to='listings.agent')),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.agent')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.customer')),
                ('guarantor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.guarantor')),
                ('house_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.houseowner')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.listing')),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region_name', models.CharField(max_length=100)),
                ('region_type', models.CharField(max_length=100)),
                ('state_name', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('metro', models.CharField(max_length=100)),
                ('county_name', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
                ('size', models.DecimalField(decimal_places=2, max_digits=6)),
                ('bedrooms', models.IntegerField()),
                ('bathrooms', models.DecimalField(decimal_places=1, max_digits=3)),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to='listings.houseowner')),
            ],
        ),
        migrations.AddField(
            model_name='listing',
            name='property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings', to='listings.property'),
        ),
    ]
