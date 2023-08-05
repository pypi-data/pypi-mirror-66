# Generated by Django 2.2.9 on 2020-01-13 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("zgw_consumers", "0003_auto_20190514_1009"),
    ]

    operations = [
        migrations.AlterField(
            model_name="service",
            name="api_type",
            field=models.CharField(
                choices=[
                    ("ac", "AC (Authorizations)"),
                    ("nrc", "NRC (Notifications)"),
                    ("zrc", "ZRC (Zaken)"),
                    ("ztc", "ZTC (Zaaktypen)"),
                    ("drc", "DRC (Informatieobjecten)"),
                    ("brc", "BRC (Besluiten)"),
                    ("kic", "KIC (Klantinteracties)"),
                    ("orc", "ORC (Overige)"),
                ],
                max_length=20,
                verbose_name="type",
            ),
        ),
    ]
