from tortoise.models import Model
from tortoise import fields
from datetime import date

import logging
log = logging.getLogger("Bot2Basics")

class Student(Model):
    id       = fields.BigIntField(pk = True)
    login    = fields.CharField(max_length = 255)

    @classmethod
    async def get_student(cls, member):
        students = await cls.filter(id = member.id)
        if len(students) > 0:
            return students[0]
        else:
            return None

    @classmethod
    async def create_student(cls, member, login):
        student = await cls.create(
            id = member.id,
            login = login
        )
        return student

    @classmethod
    async def create_student_or_update(cls, member, login):
        """
        Retourne Vrai si l'utilisateur est crée,
        Faux s'il est mis à jour.
        """
        student = await cls.get_student(member)
        if student is None:
            await cls.create_student(member, login)
            return True
        else:
            student.login = login
            await student.save()
            return False


    def __str__(self):
        return f"{self.login} (#{self.id})"

class Course(Model):
    id       = fields.UUIDField(pk = True)
    start    = fields.DateField()
    duration = fields.SmallIntField()
    semester = fields.SmallIntField()
    subject  = fields.CharField(max_length = 255)
    topic    = fields.CharField(max_length = 255)
    mode     = fields.CharField(max_length = 255)
    teachers = fields.ManyToManyField('models.Student', related_name = "courses_teacher")
    students = fields.ManyToManyField('models.Student', related_name = "courses_student")
