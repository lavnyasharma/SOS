# Generated by Django 4.1.1 on 2022-11-02 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='doc_specialization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DOCID', models.CharField(max_length=150, verbose_name='doctor id')),
                ('SPEID', models.CharField(max_length=150, verbose_name='specialization id')),
            ],
        ),
        migrations.CreateModel(
            name='doctor',
            fields=[
                ('DOCID', models.CharField(max_length=150, primary_key=True, serialize=False, verbose_name='DOCID')),
                ('UID', models.CharField(help_text='User id', max_length=150, unique=True, verbose_name='UID')),
                ('registration_number', models.CharField(blank=True, max_length=150, null=True)),
                ('professional_statement', models.TextField(null=True, verbose_name='professional_statement')),
                ('slug', models.CharField(max_length=100, unique=True, verbose_name='slug')),
                ('practicing_from', models.DateField(null=True, verbose_name='practicing from')),
                ('joined_at', models.DateTimeField(auto_now=True, verbose_name='joined at')),
            ],
        ),
        migrations.CreateModel(
            name='hospital',
            fields=[
                ('HOID', models.CharField(max_length=150, primary_key=True, serialize=False, verbose_name='hospital id')),
                ('DOCID', models.CharField(max_length=150, unique=True, verbose_name='doctor id')),
                ('name', models.CharField(max_length=150, verbose_name='hospital name')),
                ('city', models.CharField(max_length=150, verbose_name='city')),
                ('start', models.DateField(verbose_name='start date')),
                ('currently_working', models.BooleanField(default=False)),
                ('end', models.DateField(null=True, verbose_name='end date')),
            ],
        ),
        migrations.CreateModel(
            name='office',
            fields=[
                ('OFID', models.CharField(max_length=150, primary_key=True, serialize=False, verbose_name='hospital id')),
                ('DOCID', models.CharField(max_length=150, unique=True, verbose_name='doctor id')),
                ('name', models.CharField(max_length=150, null=True, verbose_name='office name')),
                ('min_time_slot', models.IntegerField(verbose_name='min slot time')),
                ('first_consultation_fee', models.IntegerField(verbose_name='first consultation fee')),
                ('follow_up_fee', models.IntegerField(null=True, verbose_name='follow up fee')),
                ('start', models.TimeField(auto_now=True, verbose_name='start time')),
                ('end', models.TimeField(auto_now=True, verbose_name='end time')),
                ('AID', models.CharField(max_length=150, null=True, verbose_name='AID')),
                ('monday', models.BooleanField(default=True, verbose_name='monday')),
                ('tuesday', models.BooleanField(default=True, null=True, verbose_name='tuesday')),
                ('wednesday', models.BooleanField(default=True, null=True, verbose_name='wednesday')),
                ('thursday', models.BooleanField(default=True, null=True, verbose_name='thrusday')),
                ('friday', models.BooleanField(default=True, null=True, verbose_name='friday')),
                ('saturday', models.BooleanField(default=True, null=True, verbose_name='saturday')),
                ('sunday', models.BooleanField(default=True, null=True, verbose_name='sunday')),
            ],
        ),
        migrations.CreateModel(
            name='qualification',
            fields=[
                ('QID', models.CharField(max_length=150, primary_key=True, serialize=False, verbose_name='Qualification id')),
                ('DOCID', models.CharField(max_length=150, unique=True, verbose_name='doctor id')),
                ('name', models.CharField(max_length=150, verbose_name='Qualification name')),
                ('institute', models.CharField(max_length=150, verbose_name='institute name')),
                ('year', models.DateField(verbose_name='procurement year')),
                ('city', models.CharField(max_length=150, verbose_name='city')),
            ],
        ),
        migrations.CreateModel(
            name='specialization',
            fields=[
                ('SPEID', models.CharField(max_length=150, primary_key=True, serialize=False, verbose_name='specialization id')),
                ('name', models.CharField(max_length=150, verbose_name='specialization name')),
            ],
        ),
    ]
