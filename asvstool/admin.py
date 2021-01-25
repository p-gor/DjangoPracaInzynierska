from django.contrib import admin
from asvstool.models import Chapter, Subsection, Requirement, Project, ReqsProject
# Register your models here.

admin.site.register(Chapter)
admin.site.register(Subsection)
admin.site.register(Requirement)
admin.site.register(Project)
admin.site.register(ReqsProject)