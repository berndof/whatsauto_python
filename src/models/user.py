from tortoise.models import Model
from tortoise import fields

class User(Model):
    def __str__(self) -> str:

        pass

    id = fields.IntField(primary_key=True, generated=True)
    is_admin = fields.BooleanField(default=False)
    chat = fields.ForeignKeyField("models.Chat", on_delete=fields.CASCADE, related_name="user", default=None, null=True)
    username = fields.CharField(max_length=30, unique=True)
    password = fields.BinaryField()
    queuesUnderSupervision = fields.ManyToManyField("models.Queue", related_name="queues_under_supervision", default=None, null=True)


