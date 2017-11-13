#!/usr/bin/env python

"""
test_dj_guitar
--------------

Tests for `dj-guitar` middlewares module.
"""

from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.views.generic.base import TemplateView

from guitar.middlewares import GuitarMiddleware


class GuitarMiddlewareTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.url = reverse("middlewares:guitar_middleware")
        self.view = TemplateView.as_view(template_name="base.html")

        # Create request and middleware.
        self.request = self.factory.get(self.url)
        self.middleware = GuitarMiddleware(self.view)  # ``self.view`` will be stored as ``self.get_response``.

        # Ask the middleware to process the request.
        self.middleware.process_request(self.request)

    def test_request(self):
        # Validate all attributes exist.
        self.assertTrue(hasattr(self.request, "ABSOLUTE_ROOT"))
        self.assertTrue(hasattr(self.request, "ABSOLUTE_URL"))
        self.assertTrue(hasattr(self.request, "ROUTE"))
        self.assertTrue("app_name" in self.request.ROUTE)
        self.assertTrue("namespace" in self.request.ROUTE)
        self.assertTrue("url_name" in self.request.ROUTE)
        self.assertTrue("view_name" in self.request.ROUTE)

        # Check attributes value.
        self.assertEqual(self.request.ABSOLUTE_ROOT, "http://testserver")
        self.assertEqual(self.request.ABSOLUTE_URL, "http://testserver{}".format(self.url))
        self.assertEqual(self.request.ROUTE["app_name"], "middlewares_app")
        self.assertEqual(self.request.ROUTE["namespace"], "middlewares")
        self.assertEqual(self.request.ROUTE["url_name"], "guitar_middleware")
        self.assertEqual(self.request.ROUTE["view_name"], "middlewares:guitar_middleware")

    def test_response(self):
        # Execute the view and ask the middleware to process the response.
        response = self.middleware.get_response(self.request)  # middleware.get_response == self.view
        response = self.middleware.process_template_response(self.request, response)

        # Validate all context data exist.
        self.assertTrue(hasattr(response, "context_data"))
        self.assertTrue("DJANGO_ENV" in response.context_data)
        self.assertTrue("ABSOLUTE_ROOT" in response.context_data)
        self.assertTrue("ABSOLUTE_URL" in response.context_data)

        # Check context data value.
        self.assertEqual(response.context_data["DJANGO_ENV"], "test")
        self.assertEqual(response.context_data["ABSOLUTE_ROOT"], "http://testserver")
        self.assertEqual(response.context_data["ABSOLUTE_URL"], "http://testserver{}".format(self.url))
