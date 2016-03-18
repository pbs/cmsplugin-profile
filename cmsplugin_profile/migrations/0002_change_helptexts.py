# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmsplugin_profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilegrid',
            name='load_mode_type',
            field=models.CharField(default=(b'load_mode_button', 'Load more button'), help_text='There are two options for pagination type. The <strong>Load More Button</strong> will enable loading of more profiles entries when a user clicks on the Load More button. Best for pages where there are multiple components in the page content area. <strong>Lazy Loading</strong> will enable the page to automatically load more profiles as the user scrolls down the page. Best for pages where this grid is the only component in the page content area.', max_length=20, verbose_name='Pagination type', choices=[(b'load_mode_button', 'Load more button'), (b'load_mode_scroll', 'Lazy loading')]),
        ),
    ]
