# Generated by Django 4.1.1 on 2022-11-02 12:24

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('AID', models.CharField(help_text='Address id', max_length=150, primary_key=True, serialize=False, verbose_name='Address')),
                ('UID', models.CharField(help_text='User id', max_length=150, verbose_name='UID')),
                ('address_line_one', models.TextField(blank=True, verbose_name='address line one')),
                ('address_line_two', models.TextField(blank=True, verbose_name='address line two')),
                ('address_line_three', models.TextField(blank=True, verbose_name='address line three')),
                ('address_line_four', models.TextField(blank=True, verbose_name='address line four')),
                ('district', models.CharField(max_length=50, verbose_name='district')),
                ('state', models.CharField(max_length=50, verbose_name='state')),
                ('is_home', models.BooleanField(default=True, verbose_name='is home')),
                ('PCID', models.CharField(help_text='pincode id', max_length=150, verbose_name='pincode id')),
                ('PHID', models.CharField(help_text='phoneno id', max_length=150, verbose_name='Phone no id ')),
                ('created_on', models.DateField(auto_now=True, verbose_name='created on')),
                ('updated_on', models.DateField(null=True, verbose_name='updated on')),
                ('pincode_number', models.CharField(default=None, help_text='Enter a Pincode', max_length=17, verbose_name='Pincode')),
                ('address', models.CharField(default=None, max_length=300, verbose_name='address')),
            ],
        ),
        migrations.CreateModel(
            name='EmailToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UID', models.CharField(help_text='User id', max_length=150, unique=True, verbose_name='UID')),
                ('email', models.CharField(max_length=100, unique=True, verbose_name='email')),
                ('Conf_token', models.CharField(max_length=100, unique=True, verbose_name='Token')),
                ('created_on', models.DateTimeField(auto_now=True, verbose_name='created')),
                ('expiration', models.DateTimeField(default=datetime.datetime(2022, 11, 2, 12, 33, 18, 381963, tzinfo=datetime.timezone.utc), verbose_name='expiration')),
            ],
        ),
        migrations.CreateModel(
            name='fmctoken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UID', models.CharField(help_text='User id', max_length=150, unique=True, verbose_name='UID')),
                ('pin', models.CharField(default='', max_length=50, verbose_name='pin')),
                ('token', models.CharField(max_length=500, verbose_name='conf token')),
                ('created_on', models.DateTimeField(auto_now=True, verbose_name='created on')),
                ('expiration', models.DateTimeField(default=datetime.datetime(2022, 11, 2, 12, 39, 18, 396470, tzinfo=datetime.timezone.utc), verbose_name='expiration')),
            ],
        ),
        migrations.CreateModel(
            name='img',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/user')),
            ],
        ),
        migrations.CreateModel(
            name='PasswordChangeRequestModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UID', models.CharField(help_text='User id', max_length=150, unique=True, verbose_name='UID')),
                ('password', models.CharField(max_length=50, verbose_name='password')),
                ('token', models.CharField(max_length=100, verbose_name='conf token')),
                ('created_on', models.DateTimeField(auto_now=True, verbose_name='created on')),
                ('expiration', models.DateTimeField(default=datetime.datetime(2022, 11, 2, 12, 39, 18, 381963, tzinfo=datetime.timezone.utc), verbose_name='expiration')),
            ],
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('PHID', models.CharField(max_length=150, primary_key=True, serialize=False, verbose_name='phone number id')),
                ('phone_number', models.CharField(help_text='Enter a Phone number', max_length=15, validators=[django.core.validators.RegexValidator(message='Please enter a valid Phone number', regex='^(?:(?:\\+|0{0,2})91(\\s*[\\-]\\s*)?|[0]?)?[789]\\d{9}$')], verbose_name='phone')),
                ('UID', models.CharField(help_text='User id', max_length=150, verbose_name='UID')),
            ],
        ),
        migrations.CreateModel(
            name='Pincode',
            fields=[
                ('PCID', models.CharField(max_length=150, primary_key=True, serialize=False, verbose_name='pincode id')),
                ('pincode_number', models.CharField(default=None, help_text='Enter a Pincode', max_length=17, verbose_name='Pincode')),
                ('UID', models.CharField(help_text='User id', max_length=150, verbose_name='UID')),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('UID', models.CharField(max_length=150, unique=True, verbose_name='UID')),
                ('phone_number', models.CharField(error_messages={'unique': 'a user with that Phone Number already exists.'}, help_text='Enter a Phone number', max_length=17, unique=True, validators=[django.core.validators.RegexValidator(message='Please enter a valid Phone number', regex='^(\\+91[\\-\\s]?)?[0]?(91)?[789]\\d{9}$')], verbose_name='phone')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, default=' ', max_length=254, verbose_name='email address')),
                ('email_confirmed', models.BooleanField(default=False, help_text='Designates whether this user has confirmed his email ', verbose_name='email active')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(auto_now=True, verbose_name='date joined')),
                ('gender', models.CharField(blank=True, choices=[('m', 'male'), ('f', 'female'), ('o', 'other')], max_length=10, verbose_name='gender')),
                ('age', models.IntegerField(null=True, verbose_name='age')),
                ('address', models.CharField(blank=True, max_length=300, verbose_name='address')),
                ('pin', models.CharField(blank=True, max_length=17, verbose_name='pin')),
                ('is_doctor', models.BooleanField(default=False, help_text='Designates whether this user is a doctor or not', verbose_name='Doctor active')),
                ('user_Type', models.CharField(default='u', max_length=2)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
