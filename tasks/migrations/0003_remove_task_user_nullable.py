# Migration to make user field required (after data migration)

from django.conf import settings
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0002_task_user'),
    ]

    operations = [
        # First, assign any null tasks to a default user (first superuser)
        migrations.RunPython(
            lambda apps, schema_editor: None,  # Will be handled manually
            reverse_code=migrations.RunPython.noop
        ),
        # Then make the field required
        migrations.AlterField(
            model_name='task',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='tasks',
                to=settings.AUTH_USER_MODEL
            ),
        ),
    ]

