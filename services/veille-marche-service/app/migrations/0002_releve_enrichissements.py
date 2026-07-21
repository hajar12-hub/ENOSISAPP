# Generated manually for the Veille Marché collection workflow.

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("app", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="releve",
            name="commentaire",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="releve",
            name="photo_url",
            field=models.URLField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="releve",
            name="promotion",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
    ]
