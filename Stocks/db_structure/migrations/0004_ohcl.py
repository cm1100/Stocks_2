# Generated by Django 3.2.7 on 2021-10-13 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db_structure', '0003_lookupstock'),
    ]

    operations = [
        migrations.CreateModel(
            name='OHCL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('open_p', models.IntegerField()),
                ('high_p', models.IntegerField()),
                ('low_p', models.IntegerField()),
                ('close_p', models.IntegerField()),
                ('volume', models.IntegerField()),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db_structure.stock')),
            ],
        ),
    ]
