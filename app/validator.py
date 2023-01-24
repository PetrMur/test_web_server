from typing import List
from app.models.field_types import Field
from app.utils.exceptions import ValidationError


class Validator:
    def __init__(self, fields: List[Field]):
        self.fields = fields

    def validate(self):
        self.validate_fields()
        self.check_required_fields()

    def check_required_fields(self):
        """Check for required fields"""

        for field in self.fields:
            if field.is_required and field is None:
                raise ValidationError

    def validate_fields(self):
        """Check fields are correct"""

        for field in self.fields:
            if not field.is_correct():
                raise ValidationError

    def check_type(self, field):
        pass
