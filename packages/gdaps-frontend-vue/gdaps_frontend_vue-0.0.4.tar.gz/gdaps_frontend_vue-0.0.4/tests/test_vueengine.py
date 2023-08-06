from django.core import management
from django.test import TestCase



class TestVueEngine(TestCase):

    def test_prereq_check(self):
        management.call_command("initfrontend")


