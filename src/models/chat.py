from tortoise.models import Model
from tortoise import fields

class Chat(Model):
    def __str__(self):
        return f"Chat(phone={self.phone}, name={self.name})"

    id = fields.IntField(primary_key=True)
    phone = fields.IntField()
    name = fields.CharField(max_length=255)
    is_contact = fields.BooleanField(default=False)
    queue = fields.ForeignKeyField("models.Queue", null=True, on_delete=fields.SET_NULL, related_name="chats", default=None)

        