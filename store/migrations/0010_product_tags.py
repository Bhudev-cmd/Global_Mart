from django.db import migrations, models


def seed_samsung_a35_tags(apps, schema_editor):
    Product = apps.get_model('store', 'Product')
    Product.objects.filter(name__iexact='Samsung Galaxy A35 5G').update(
        tags='mobile, smartphone, android'
    )


def unseed_samsung_a35_tags(apps, schema_editor):
    Product = apps.get_model('store', 'Product')
    Product.objects.filter(name__iexact='Samsung Galaxy A35 5G').update(tags='')


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_order_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.CharField(
                blank=True,
                help_text='Comma-separated keywords, e.g., mobile, smartphone, android',
                max_length=300,
            ),
        ),
        migrations.RunPython(seed_samsung_a35_tags, unseed_samsung_a35_tags),
    ]
