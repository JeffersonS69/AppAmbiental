# Generated by Django 3.2.2 on 2023-08-14 16:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('disasterType', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProtocolAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=200)),
                ('steps_before', models.TextField()),
                ('steps_during', models.TextField()),
                ('steps_after', models.TextField()),
                ('responsibilities', models.TextField()),
                ('disaster_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='disasterType.disastertype')),
            ],
        ),
    ]