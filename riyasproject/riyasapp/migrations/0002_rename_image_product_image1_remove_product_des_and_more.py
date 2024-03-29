# Generated by Django 4.1 on 2024-01-17 18:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("riyasapp", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="image",
            new_name="image1",
        ),
        migrations.RemoveField(
            model_name="product",
            name="des",
        ),
        migrations.AddField(
            model_name="product",
            name="des1",
            field=models.CharField(default="", max_length=300),
        ),
        migrations.AddField(
            model_name="product",
            name="des2",
            field=models.CharField(default="", max_length=300),
        ),
        migrations.AddField(
            model_name="product",
            name="des3",
            field=models.CharField(default="", max_length=300),
        ),
        migrations.AddField(
            model_name="product",
            name="des4",
            field=models.CharField(default="", max_length=300),
        ),
        migrations.AddField(
            model_name="product",
            name="des5",
            field=models.CharField(default="", max_length=300),
        ),
        migrations.AddField(
            model_name="product",
            name="image2",
            field=models.ImageField(default="", upload_to="shop/images/"),
        ),
        migrations.AddField(
            model_name="product",
            name="image3",
            field=models.ImageField(default="", upload_to="shop/images/"),
        ),
        migrations.AddField(
            model_name="product",
            name="image4",
            field=models.ImageField(default="", upload_to="shop/images/"),
        ),
        migrations.AddField(
            model_name="product",
            name="image5",
            field=models.ImageField(default="", upload_to="shop/images/"),
        ),
        migrations.AddField(
            model_name="product",
            name="mrp",
            field=models.IntegerField(default=0),
        ),
    ]
