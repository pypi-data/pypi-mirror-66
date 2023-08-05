# -*- coding: utf-8 -*-
from django.urls import reverse

from cms.toolbar.items import Break
from cms.cms_toolbars import ADMIN_MENU_IDENTIFIER, ADMIN_SITES_BREAK
from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar

from allink_core.core_apps.allink_categories.models import AllinkCategory


@toolbar_pool.register
class AllinkCategoryToolbar(CMSToolbar):
    model = AllinkCategory

    def populate(self):
        admin_menu = self.toolbar.get_menu(ADMIN_MENU_IDENTIFIER)
        position = admin_menu.find_first(Break, identifier=ADMIN_SITES_BREAK)
        allink_menu = admin_menu.get_or_create_menu(
            'allink-menu',
            'allink',
            position=position
        )

        url = reverse('admin:{}_{}_changelist'.format(self.model._meta.app_label, self.model._meta.model_name))
        allink_menu.add_sideframe_item('Categories', url=url)
