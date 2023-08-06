from marshmallow import (
    Schema,
    fields,
    validate,
)


class DrugIndicationResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    appl_no = fields.String(validate=not_blank, required=True)
    appl_type = fields.String(validate=not_blank, required=True)
    indication_text = fields.String(allow_none=True)
    indications = fields.String(allow_none=True)
    updated_at = fields.DateTime()


class DrugIndicationQueryParamsSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer()
    appl_no = fields.String(validate=not_blank)
    appl_type = fields.String(validate=not_blank)


class DrugIndicationPatchSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    appl_no = fields.String(validate=not_blank)
    appl_type = fields.String(validate=not_blank)
    indication_text = fields.String(allow_none=True)
    indications = fields.String(allow_none=True)
