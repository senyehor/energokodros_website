import factory
from django.db import transaction
from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils.translation import gettext_lazy as _
from factory import django

from institutions.models import Institution, AccessLevel, Object


class InstitutionTest(TestCase):
    def setUp(self):
        self.name = 'test institution name'
        self.institution_description = 'test institution description'

    def test_creating_institution(self):
        institution = Institution(
            institution_name=self.name,
            institution_description=self.institution_description
        )
        self.assertEqual(
            institution.institution_name,
            self.name,
            _('institution name is set incorrectly')
        )
        self.assertEqual(
            institution.institution_description,
            self.institution_description,
            _('institution description is set incorrectly')
        )


class InstitutionFactory(django.DjangoModelFactory):
    institution_name = factory.Sequence(lambda n: f'institution {n}')
    institution_description = factory.Sequence(lambda n: f'institution {n} description')

    class Meta:
        model = 'institutions.Institution'


class AccessLevelTest(TestCase):
    def setUp(self):
        self.level_def = 1
        self.level_description = 'test level description'

    def test_creating_access_level(self):
        access_level = AccessLevel(
            level_def=self.level_def,
            level_description=self.level_description
        )
        self.assertEqual(
            access_level.level_def,
            self.level_def,
            _('level definition is set incorrectly')
        )
        self.assertEqual(
            access_level.level_description,
            self.level_description,
            _('level definition is set incorrectly')
        )


class AccessLevelFactory(django.DjangoModelFactory):
    level_def = factory.Sequence(lambda n: n)
    level_description = factory.Sequence(lambda n: f'level {n} description')

    class Meta:
        model = 'institutions.AccessLevel'


class ObjectTest(TestCase):
    def setUp(self):
        self.institution = InstitutionFactory()
        self.access_level = AccessLevelFactory()
        self.name = 'some object'
        self.description = 'some object description'

    def test_creating_object(self):
        parent = Object(
            institution=self.institution,
            object_name='parent',
            object_description='parent object',
            access_level=self.access_level
        )
        obj = Object(
            institution=self.institution,
            object_name=self.name,
            object_description=self.description,
            access_level=self.access_level,
            parent=parent
        )
        self.assertEqual(
            obj.institution,
            self.institution,
            _('institution is set incorrectly')
        )
        self.assertEqual(
            obj.object_name,
            self.name,
            _('object_name is set incorrectly')
        )
        self.assertEqual(
            obj.object_description,
            self.description,
            _('object_description is set incorrectly')
        )
        self.assertEqual(
            obj.access_level,
            self.access_level,
            _('access_level is set incorrectly')
        )
        self.assertEqual(
            obj.parent,
            parent,
            _('parent is set incorrectly')
        )

    def test_object_wrong_relations(self):
        # we need separate transaction for each case, as TestCase by default is
        # transactional, so when we try to create incorrect object, 'with self.assertRaises...'
        # catches it, but test case wide transaction remains invalid
        with transaction.atomic():
            with self.assertRaises(
                    IntegrityError,
                    msg=_('object was created with no institution and access_level')
            ):
                Object(
                    object_name=self.name,
                    object_description=self.description,
                ).save()
        with transaction.atomic():
            with self.assertRaises(
                    IntegrityError,
                    msg=_('object was created with no access level')
            ):
                Object(
                    institution=self.institution,
                    object_name=self.name,
                    object_description=self.description,
                ).save()
        with transaction.atomic():
            with self.assertRaises(
                    IntegrityError,
                    msg=_('object was created with no institution')
            ):
                Object(
                    object_name=self.name,
                    object_description=self.description,
                    access_level=self.access_level
                ).save()


class ObjectFactory(django.DjangoModelFactory):
    object_name = factory.Sequence(lambda n: f'object {n}')
    object_description = factory.Sequence(lambda n: f'object {n} description')

    class Meta:
        model = 'institutions.Object'
