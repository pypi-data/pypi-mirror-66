from marshmallow import Schema, fields

class ManyRecordsSchema(Schema):
    records = fields.List(fields.Dict())
    
class RecordsCountSchema(Schema):
    count = fields.Int()

records_schema = ManyRecordsSchema()
record_count_schema = RecordsCountSchema()

