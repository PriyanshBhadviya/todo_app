from flask_marshmallow import Marshmallow
from marshmallow import fields
from models import Task

ma = Marshmallow()

class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        load_instance = True

    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str()
    due_date = fields.DateTime()
    priority = fields.Str(required=True)
    status = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

