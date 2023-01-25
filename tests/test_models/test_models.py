import unittest
from app.models.models import AbstractModel
from app.models.field_types import SmallStringFIO


class ModelWithName(AbstractModel):
    name = SmallStringFIO

    _required = ('name', )


class TestAbstractModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fields = {'name': 'Иван'}
        cls.model = AbstractModel.create_object(fields)

        cls.model_with_name = ModelWithName.create_object(fields)

    def test_model(self):
        fields = {'name': 'Иван'}
        self.assertEqual(self.model.get_fields, {})
        self.assertEqual(self.model_with_name.get_fields.keys(), fields.keys())
        self.assertFalse(self.model_with_name.get_fields == {'name': SmallStringFIO('Иван')})
