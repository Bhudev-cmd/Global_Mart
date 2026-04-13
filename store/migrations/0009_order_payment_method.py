from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_category_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(default='Card Payment', max_length=50),
        ),
    ]
