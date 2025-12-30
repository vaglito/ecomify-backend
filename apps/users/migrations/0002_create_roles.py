from django.db import migrations


def create_roles(apps, schema_editor):
    Group = apps.get_model("auth", "Group")

    for role in ["admin", "staff", "customer"]:
        Group.objects.get_or_create(name=role)


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_roles),
    ]
