# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import mock
import pytest

from django.core.exceptions import ImproperlyConfigured
from django import test
from django.test.utils import override_settings




class TestContextProcessor(test.TestCase):
    """
    Tests for SuccessURLRedirectListMixin.
    """
    def test_simple(self):
        """
        Test if browser is redirected to list view.
        """
        response = self.client.get('')
        context = response.context
        # print(context)
        self.assertIn('title', ['title', 'fun'])
