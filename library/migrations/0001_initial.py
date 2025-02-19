# Generated by Django 5.1.5 on 2025-02-04 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Book",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=200)),
                ("author", models.CharField(max_length=200)),
                ("year_published", models.CharField(max_length=4)),
                ("kind", models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name="Customer",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=200)),
                ("city", models.CharField(blank=True, max_length=200, null=True)),
                ("age", models.IntegerField()),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Loan",
            fields=[
                ("cust_id", models.AutoField(primary_key=True, serialize=False)),
                ("book_id", models.CharField(max_length=200)),
                ("loan_date", models.DateField(blank=True, null=True)),
                ("return_date", models.DateField()),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
            ],
        ),
    ]
