from django.db import models, connection
from django.conf import settings
from django_tenants.models import DomainMixin
from tenant_users.tenants.models import TenantBase


class Restaurant(TenantBase):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # override owner to one-to-one
    name = models.CharField(verbose_name='Назва ресторана', max_length=256)
    address = models.CharField(verbose_name='Адрес ресторана', max_length=256)

    auto_drop_schema = True

    class Meta:
        verbose_name = 'Ресторан'
        verbose_name_plural = 'Ресторани'

    @classmethod
    def delete_restaurant(cls, schema_name: str, pk: int) -> None:
        with connection.cursor() as cursor:
            query = f'''
                BEGIN;
                    DROP SCHEMA "{schema_name}" CASCADE;
                    DELETE FROM public.main_domain WHERE tenant_id={pk};
                    DELETE FROM public.main_restaurant WHERE id={pk};
                COMMIT;
            '''
            cursor.execute(query)

    def __str__(self):
        return f'{self.id}) {self.owner.email} - {self.name}'


class Domain(DomainMixin):
    pass
