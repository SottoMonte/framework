import unittest
import asyncio
from types import SimpleNamespace

# Simuliamo il modulo language come nel tuo codice
class MockLanguage:
    @staticmethod
    def get(key, data):
        keys = key.split('.')
        for k in keys:
            if isinstance(data, dict):
                data = data.get(k)
            else:
                return None
        return data

    @staticmethod
    def translation(data, *args, **kwargs):
        return data

    @staticmethod
    async def load_module(*args, **kwargs):
        return SimpleNamespace(MyModel=[{'name': 'location'}, {'name': 'path'}])

# La tua classe repository modificata per usare self.language invece di language globale
modules = {'factory': 'framework.service.factory','flow': 'framework.service.flow'}

class TestRepository(IsolatedAsyncioTestCase):
    def setUp(self):
        self.repo = repository(
            location={
                "dev": [
                    "repos/{payload.location}/contents/{payload.path}",
                    "repos/{payload.location}/contents/{payload.path}/{payload.name}",
                ]
            },
            mapper={},
            values={},
            payloads={},
            model="MyModel"
        )
        self.repo.language = MockLanguage
        self.repo.get_nested_value = lambda data, key: MockLanguage.get(key, data)

    # === can_format ===
    def test_can_format_valid(self):
        template = "repos/{payload.location}/contents/{payload.path}"
        data = {
            "payload": {
                "location": "user/repo",
                "path": "src"
            }
        }
        result, count = self.repo.can_format(template, data)
        self.assertTrue(result)
        self.assertEqual(count, 2)

    def test_can_format_invalid(self):
        template = "repos/{payload.location}/contents/{payload.path}/{payload.name}"
        data = {
            "payload": {
                "location": "user/repo",
                "path": "src"
            }
        }
        result, count = self.repo.can_format(template, data)
        self.assertFalse(result)
        self.assertEqual(count, 3)

    # === do_format ===
    def test_do_format(self):
        template = "repos/{payload.location}/contents/{payload.path}"
        data = {
            "payload": {
                "location": "user/repo",
                "path": "src"
            }
        }
        self.repo.language = MockLanguage
        self.repo.get_nested_value = lambda data, key: MockLanguage.get(key, data)
        formatted = self.repo.do_format(template, data)
        self.assertEqual(formatted, "repos/user/repo/contents/src")

    # === find_first_formattable_template ===
    def test_find_first_formattable_template(self):
        templates = [
            "repos/{payload.location}/contents/{payload.path}",
            "repos/{payload.location}/contents/{payload.path}/{payload.name}"
        ]
        data = {
            "payload": {
                "location": "user/repo",
                "path": "src"
            }
        }
        self.repo.language = MockLanguage
        best = self.repo.find_first_formattable_template(templates, data)
        self.assertEqual(best, "repos/{payload.location}/contents/{payload.path}")

    # === parameters (async) ===
    async def test_parameters(self):
        payloads = {}
        self.repo.payloads = payloads
        inputs = {
            "payload": {
                "location": "user/repo",
                "path": "src"
            }
        }
        result = await self.repo.parameters("crud_op", "dev", **inputs)
        self.assertEqual(result["location"], "repos/user/repo/contents/src")
        self.assertEqual(result["provider"], "dev")
        self.assertEqual(result["payload"], {"location": "user/repo", "path": "src"})

    # === results (async) ===
    async def test_results(self):
        self.repo.fields = ['location']
        transaction = {
            "result": [{"location": "loc1"}, {"location": "loc2"}]
        }
        data = {"transaction": transaction, "profile": "dev"}
        self.repo.language = MockLanguage
        result = await self.repo.results(**data)
        self.assertEqual(len(result["result"]), 2)
        self.assertEqual(result["result"][0]["location"], "loc1")
