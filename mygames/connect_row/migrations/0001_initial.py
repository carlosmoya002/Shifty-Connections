# Generated by Django 5.1.1 on 2024-09-29 13:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('difficulty', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Vocabulary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Vocabulary',
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('difficulty', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('current_state', models.JSONField(blank=True, default=list)),
                ('locked_rows_count', models.IntegerField(default=0)),
                ('connection1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='connection1', to='connect_row.connection')),
                ('connection2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='connection2', to='connect_row.connection')),
                ('connection3', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='connection3', to='connect_row.connection')),
                ('connection4', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='connection4', to='connect_row.connection')),
            ],
        ),
        migrations.AddField(
            model_name='connection',
            name='word1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='word1', to='connect_row.vocabulary'),
        ),
        migrations.AddField(
            model_name='connection',
            name='word2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='word2', to='connect_row.vocabulary'),
        ),
        migrations.AddField(
            model_name='connection',
            name='word3',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='word3', to='connect_row.vocabulary'),
        ),
        migrations.AddField(
            model_name='connection',
            name='word4',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='word4', to='connect_row.vocabulary'),
        ),
    ]
