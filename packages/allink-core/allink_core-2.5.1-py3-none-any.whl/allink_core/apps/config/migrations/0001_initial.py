# Generated by Django 2.1.8 on 2019-07-02 17:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djangocms_text_ckeditor.fields
import filer.fields.image
import parler.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AllinkPageExtension',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extended_object', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='cms.Page')),
                ('og_image', filer.fields.image.FilerImageField(blank=True, help_text='og: image is used when shared on Facebook/ Twitter etc. (Min. 1200 x 630 px)<br>Page: 1. fallback is teaser_image, 2. fallback is field allink_config.default_og_image.<br>App: 1. fallback = preview_image 2. fallback is teaser_image, 3. fallback is defined in allink_config.default_og_image.<br>', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='config_allinkpageextension_og_image', to=settings.FILER_IMAGE_MODEL, verbose_name='og:Image')),
                ('public_extension', models.OneToOneField(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='draft_extension', to='config.AllinkPageExtension')),
                ('teaser_image', filer.fields.image.FilerImageField(blank=True, help_text='Optional field for teaser image. og: properties are used when shared on Facebook/ Twitter etc. (Min. 1200 x 630 px)<br>Also used as "meta" property="og:image"<br>Page: 1. fallback is allink_config.default_og_image.<br>App: 1. fallback = preview_image 2. fallback is defined in allink_config.default_og_image.<br>', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='config_allinkpageextension_teaser_image', to=settings.FILER_IMAGE_MODEL, verbose_name='Teaser image')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AllinkTitleExtension',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('og_title', models.CharField(blank=True, default='', help_text='title-tag is used when shared on Facebook/ Twitter etc.<br>Also used to overwrite "meta property="og:image.."" and title-tag<br>Page: fallback is field "title" of the page.<br>App: fallback is field "title".', max_length=255, verbose_name='og:title | <title> Tag')),
                ('og_description', models.TextField(blank=True, default='', help_text='Description is used when shared on Facebook/ Twitter etc.<br>Also used to overwrite  "meta" property="og:description" .. and "meta name="description"<br>Page: fallback is field "teaser_description" of the page, if set. Otherwise empty.<br>App: fallback is field "lead", if set. Otherwise empty.', max_length=255, verbose_name='og:description | meta description')),
                ('teaser_title', models.CharField(blank=True, default='', help_text='Page: fallback is field "title" of the page.<br>App: fallback is field "title".', max_length=255, verbose_name='Teaser title')),
                ('teaser_technical_title', models.CharField(blank=True, default='', help_text='Page: no fallback.<br>App: fallback is hardcoded per app in the teaser_dict.', max_length=255, verbose_name='Teaser technical title')),
                ('teaser_description', models.TextField(blank=True, default='', help_text='Page: no fallback.<br>App: fallback is field "lead".', verbose_name='Teaser description')),
                ('teaser_link_text', models.CharField(blank=True, default='', help_text='Page: no fallback.<br>App: fallback is hardcoded per app in the teaser_dict.', max_length=255, verbose_name='Teaser link text')),
                ('extended_object', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='cms.Title')),
                ('public_extension', models.OneToOneField(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='draft_extension', to='config.AllinkTitleExtension')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme_color', models.CharField(blank=True, help_text='Theme color for Android Chrome', max_length=50, null=True, verbose_name='Theme Color')),
                ('mask_icon_color', models.CharField(blank=True, help_text='Mask icon color for safari-pinned-tab.svg', max_length=50, null=True, verbose_name='Mask icon color')),
                ('msapplication_tilecolor', models.CharField(blank=True, help_text='MS application TitleColor Field', max_length=50, null=True, verbose_name='msapplication TileColor')),
                ('google_site_verification', models.CharField(blank=True, max_length=64, null=True, verbose_name='Google Site Verification Code')),
                ('default_to_email', models.EmailField(default='itcrowd@allink.ch', max_length=255, verbose_name='Default to email')),
                ('default_from_email', models.EmailField(default='itcrowd@allink.ch', max_length=255, verbose_name='Default from email')),
                ('default_og_image', filer.fields.image.FilerImageField(blank=True, help_text='Default preview image when page/post is shared on Facebook. <br>Min. 1200 x 630 for best results.', null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.FILER_IMAGE_MODEL, verbose_name='og:image')),
            ],
            options={
                'verbose_name': 'Configuration',
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ConfigTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('default_base_title', models.CharField(blank=True, help_text='Default base title, Is also used for default base og:title when page/post is shared on Facebook. <br>If not supplied the name form Django Sites will be used instead.', max_length=50, null=True, verbose_name='Base title')),
                ('newsletter_lead', djangocms_text_ckeditor.fields.HTMLField(blank=True, help_text='Teaser text in the newsletter signup view (data usage explainer).', null=True, verbose_name='Newsletter Signup Text')),
                ('newsletter_declaration_of_consent', djangocms_text_ckeditor.fields.HTMLField(blank=True, help_text='Detailed declaration of consent.', null=True, verbose_name='Declaration of consent')),
                ('master', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='config.Config')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
