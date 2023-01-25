from typing import Dict, Tuple
from app.utils.exceptions import ValidationError


class Validator:
    def __init__(self, fields: Dict, required: Tuple):
        self.fields = fields
        self.required = required

    def validate(self):
        self.check_required_fields()
        self.validate_fields()

    def check_required_fields(self):
        """Check for required fields"""

        for req_field in self.required:
            field = self.fields.get(req_field)
            if field is None or field.value is None:
                desc = f'{field.value} is required' \
                    if field else f'{", ".join(self.required)} is/are required'
                raise ValidationError(description=desc)

    def validate_fields(self):
        """Check fields are correct"""

        for field in self.fields.values():
            if not field.is_correct():
                raise ValidationError(description=f'{field.name} {field.description}')
