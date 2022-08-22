from .models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin


# Register your models here.


# Setup do User no admin.
class AccountAdmin(UserAdmin):
    list_display = ('cpf', 'nome', 'is_active', 'is_staff')
    search_field = 'nome'
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('cpf', 'nome', 'is_active', 'is_staff')

    add_fieldsets = (
            (None, {
                'classes': ('wide',),
                'fields': ('nome', 'password1', 'password2'),
            }),
        )


# Setup da classe Curso no admin.
class CourseAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'duracao', 'tema', 'professor', 'status', 'criado')
    list_filter = ('titulo', 'duracao', 'tema', 'professor', 'status')


# Setup do Tema no admin.
class TemaResource(resources.ModelResource):
    class Meta:
        model = Tema


class TemaAdmin(ImportExportModelAdmin):
    resource_class = TemaResource


# Models que aparecem no admin.
admin.site.register(Professor, AccountAdmin)
admin.site.register(Curso, CourseAdmin)
admin.site.register(Tema, TemaAdmin)
admin.site.register(Topico)
