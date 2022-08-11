from django.test import TestCase

from institutions.models import Facility, MoveOptions


class FacilityTest(TestCase):
    def test_creating_facility_set(self):
        root: Facility = Facility.add_root(name='root')
        child: Facility = root.add_child(name='root child')
        child_child: Facility = child.add_child(name='child child')
        root.refresh_from_db()
        self.assertTrue(
            child.is_child_of(root),
            'child is not child of root'
        )
        self.assertTrue(
            child_child.is_descendant_of(root),
            'child_child is not descendant of root'
        )
        child_child.move(root, MoveOptions.CHILD)
        self.assertTrue(
            child_child.is_child_of(root),
            'child_child is not child of root after moving'
        )
