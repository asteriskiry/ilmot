# Generated by Django 2.0.7 on 2018-07-11 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Arkisto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tyyppi', models.CharField(max_length=500, verbose_name='Tapahtuman typpi')),
                ('nimi', models.CharField(max_length=500, verbose_name='Tapahtuman nimi')),
                ('kuvaus', models.TextField(verbose_name='Tapahtuman yleiskuvaus')),
                ('participants', models.IntegerField(verbose_name='Osallistujamäärä')),
                ('omistaja', models.CharField(max_length=500, verbose_name='Tapahtuman pitäjä')),
                ('date', models.DateTimeField(verbose_name='Tapahtuman pitopäivä')),
            ],
        ),
        migrations.CreateModel(
            name='Ekskursio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nimi', models.CharField(max_length=500, verbose_name='Tapahtuman nimi')),
                ('paikka', models.CharField(max_length=200, verbose_name='Pitopaikka')),
                ('date', models.DateTimeField(verbose_name='Tapahtuman pitopäivä')),
                ('kuvaus', models.TextField(verbose_name='Tapahtuman yleiskuvaus')),
                ('kuva', models.ImageField(blank=True, null=True, upload_to='')),
                ('hinta', models.CharField(blank=True, max_length=500, null=True)),
                ('max_osallistujia', models.PositiveIntegerField(blank=True, null=True)),
                ('ilmo_alkaa', models.DateField()),
                ('ilmo_loppuu', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MuuTapahtuma',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nimi', models.CharField(max_length=500, verbose_name='Tapahtuman nimi')),
                ('paikka', models.CharField(max_length=200, verbose_name='Pitopaikka')),
                ('date', models.DateTimeField(verbose_name='Tapahtuman pitopäivä')),
                ('kuvaus', models.TextField(verbose_name='Tapahtuman yleiskuvaus')),
                ('kuva', models.ImageField(blank=True, null=True, upload_to='')),
                ('hinta', models.CharField(blank=True, max_length=500, null=True)),
                ('max_osallistujia', models.PositiveIntegerField(blank=True, null=True)),
                ('ilmo_alkaa', models.DateField()),
                ('ilmo_loppuu', models.DateField(blank=True, null=True)),
                ('min_osallistujia', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Osallistuja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nimi', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('miscInfo', models.TextField(editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Sitsit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nimi', models.CharField(max_length=500, verbose_name='Tapahtuman nimi')),
                ('paikka', models.CharField(max_length=200, verbose_name='Pitopaikka')),
                ('date', models.DateTimeField(verbose_name='Tapahtuman pitopäivä')),
                ('kuvaus', models.TextField(verbose_name='Tapahtuman yleiskuvaus')),
                ('kuva', models.ImageField(blank=True, null=True, upload_to='')),
                ('hinta', models.CharField(blank=True, max_length=500, null=True)),
                ('max_osallistujia', models.PositiveIntegerField(blank=True, null=True)),
                ('ilmo_alkaa', models.DateField()),
                ('ilmo_loppuu', models.DateField(blank=True, null=True)),
                ('quotas', models.CharField(blank=True, max_length=500, null=True, verbose_name='Järjestävien tahojen osallistujakiintiöt')),
                ('avec', models.CharField(blank=True, max_length=500)),
                ('plaseerustoive', models.CharField(blank=True, max_length=500)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TapahtumanOmistaja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nimi', models.CharField(max_length=500, unique=True, verbose_name='Järjestävä taho')),
            ],
        ),
        migrations.CreateModel(
            name='Tapahtumat',
            fields=[
                ('uid', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('omistaja', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventsignup.TapahtumanOmistaja')),
            ],
        ),
        migrations.CreateModel(
            name='TapahtumaTyypit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tyyppi', models.CharField(max_length=500, unique=True, verbose_name='Tapahtuman tyyppi')),
            ],
        ),
        migrations.CreateModel(
            name='Vuosijuhla',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nimi', models.CharField(max_length=500, verbose_name='Tapahtuman nimi')),
                ('paikka', models.CharField(max_length=200, verbose_name='Pitopaikka')),
                ('date', models.DateTimeField(verbose_name='Tapahtuman pitopäivä')),
                ('kuvaus', models.TextField(verbose_name='Tapahtuman yleiskuvaus')),
                ('kuva', models.ImageField(blank=True, null=True, upload_to='')),
                ('hinta', models.CharField(blank=True, max_length=500, null=True)),
                ('max_osallistujia', models.PositiveIntegerField(blank=True, null=True)),
                ('ilmo_alkaa', models.DateField()),
                ('ilmo_loppuu', models.DateField(blank=True, null=True)),
                ('avec', models.CharField(blank=True, max_length=500)),
                ('plaseerustoive', models.CharField(blank=True, max_length=500)),
                ('omistaja', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='eventsignup.TapahtumanOmistaja')),
                ('tyyppi', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='eventsignup.TapahtumaTyypit')),
                ('uid', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='eventsignup.Tapahtumat')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='tapahtumat',
            name='tyyppi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventsignup.TapahtumaTyypit'),
        ),
        migrations.AddField(
            model_name='sitsit',
            name='omistaja',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='eventsignup.TapahtumanOmistaja'),
        ),
        migrations.AddField(
            model_name='sitsit',
            name='tyyppi',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='eventsignup.TapahtumaTyypit'),
        ),
        migrations.AddField(
            model_name='sitsit',
            name='uid',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='eventsignup.Tapahtumat'),
        ),
        migrations.AddField(
            model_name='osallistuja',
            name='tapahtuma',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='eventsignup.Tapahtumat'),
        ),
        migrations.AddField(
            model_name='muutapahtuma',
            name='omistaja',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='eventsignup.TapahtumanOmistaja'),
        ),
        migrations.AddField(
            model_name='muutapahtuma',
            name='tyyppi',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='eventsignup.TapahtumaTyypit'),
        ),
        migrations.AddField(
            model_name='muutapahtuma',
            name='uid',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='eventsignup.Tapahtumat'),
        ),
        migrations.AddField(
            model_name='ekskursio',
            name='omistaja',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='eventsignup.TapahtumanOmistaja'),
        ),
        migrations.AddField(
            model_name='ekskursio',
            name='tyyppi',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='eventsignup.TapahtumaTyypit'),
        ),
        migrations.AddField(
            model_name='ekskursio',
            name='uid',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='eventsignup.Tapahtumat'),
        ),
    ]
