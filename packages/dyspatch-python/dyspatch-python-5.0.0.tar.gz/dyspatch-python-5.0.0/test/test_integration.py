# coding: utf-8

from __future__ import absolute_import

import unittest
import os

import dyspatch_client

version = "application/vnd.dyspatch.2020.04+json"

class TestDraftRead(unittest.TestCase):
    """DraftRead unit test stubs"""

    def setUp(self):
        key = os.environ['DYSPATCH_API_KEY']
        configuration = dyspatch_client.Configuration()
        configuration.api_key['Authorization'] = f'Bearer {key}'
        client = dyspatch_client.ApiClient(configuration)
        self.templates = dyspatch_client.api.templates_api.TemplatesApi(client)
        self.drafts = dyspatch_client.api.drafts_api.DraftsApi(client)

    def test_list_templates(self):
        templates = self.templates.get_templates(version)
        print(templates)

        template = self.templates.get_template_by_id(
            templates.data[0].id,
            "",
            version,
        )
        print(template)

    def test_list_drafts(self):
        drafts = self.drafts.get_drafts(version)
        print(drafts)

        draft = self.drafts.get_draft_by_id(
            drafts.data[0].id,
            "handlebars",
            version,
        )
        print(draft)



if __name__ == '__main__':
    unittest.main()
