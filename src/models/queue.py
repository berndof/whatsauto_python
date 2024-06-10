from tortoise.models import Model
from tortoise import fields

class Queue(Model):
    def __str__(self):
        return f"Queue(name={self.name})"

    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255, unique=True)
    greetings_message = fields.TextField()
    index = fields.IntField(unique=True)
    supervised_by = fields.ManyToManyField("models.User", related_name="queuesUnderSupervision", default=None, null=True)
