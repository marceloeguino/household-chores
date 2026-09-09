from django.test import TestCase

from .models import Member


class MemberModelTests(TestCase):
    def test_create_member(self):
        member = Member.objects.create(name="Alex")
        self.assertEqual(str(member), "Alex")
        self.assertEqual(Member.objects.count(), 1)

    def test_members_ordered_by_name(self):
        Member.objects.create(name="Zoe")
        Member.objects.create(name="Alex")
        names = list(Member.objects.values_list("name", flat=True))
        self.assertEqual(names, ["Alex", "Zoe"])
