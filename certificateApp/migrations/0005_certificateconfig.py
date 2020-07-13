# Generated by Django 2.1.5 on 2020-07-13 04:33

import certificateApp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificateApp', '0004_auto_20200707_2031'),
    ]

    operations = [
        migrations.CreateModel(
            name='CertificateConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('namex', models.CharField(default='0', max_length=50)),
                ('namey', models.CharField(default='0', max_length=50)),
                ('profilex', models.CharField(default='0', max_length=50)),
                ('profiley', models.CharField(default='0', max_length=50)),
                ('typex', models.CharField(default='0', max_length=50)),
                ('typey', models.CharField(default='0', max_length=50)),
                ('d1x', models.CharField(default='0', max_length=50)),
                ('d1y', models.CharField(default='0', max_length=50)),
                ('d2x', models.CharField(default='0', max_length=50)),
                ('d2y', models.CharField(default='0', max_length=50)),
                ('datex', models.CharField(default='0', max_length=50)),
                ('datey', models.CharField(default='0', max_length=50)),
                ('renox', models.CharField(default='0', max_length=50)),
                ('renoy', models.CharField(default='0', max_length=50)),
                ('logox', models.CharField(default='0', max_length=50)),
                ('logoy', models.CharField(default='0', max_length=50)),
                ('signx', models.CharField(default='0', max_length=50)),
                ('signy', models.CharField(default='0', max_length=50)),
                ('namesize', models.CharField(default='0', max_length=50)),
                ('typesize', models.CharField(default='0', max_length=50)),
                ('profilesize', models.CharField(default='0', max_length=50)),
                ('datesize', models.CharField(default='0', max_length=50)),
                ('dsize', models.CharField(default='0', max_length=50)),
                ('certificate_img', models.ImageField(default='certificate.jpg', upload_to=certificateApp.models.CertificateConfig.filerename)),
                ('certificate_pdf', models.FileField(default='certificate.pdf', upload_to=certificateApp.models.CertificateConfig.filerename)),
                ('logo_img', models.ImageField(default='logo.png', upload_to=certificateApp.models.CertificateConfig.filerename)),
                ('sign_img', models.ImageField(default='signature.png', upload_to=certificateApp.models.CertificateConfig.filerename)),
                ('namefont', models.FileField(default='default.ttf', upload_to='certificate_file/fonts')),
                ('otherfont', models.FileField(default='default.ttf', upload_to='certificate_file/fonts')),
                ('cktl', models.CharField(default='1200', max_length=50)),
                ('cktw', models.CharField(default='1600', max_length=50)),
                ('logol', models.CharField(default='165', max_length=50)),
                ('logow', models.CharField(default='165', max_length=50)),
                ('signl', models.CharField(default='78', max_length=50)),
                ('signw', models.CharField(default='224', max_length=50)),
            ],
        ),
    ]
