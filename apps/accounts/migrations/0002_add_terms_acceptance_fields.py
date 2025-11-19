# Generated manually

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='terms_and_conditions_accepted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='terms_accepted_at',
            field=models.DateTimeField(blank=True, help_text='Timestamp when user accepted terms and conditions', null=True),
        ),
    ]

