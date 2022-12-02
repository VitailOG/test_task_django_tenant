import string
import random

from dataclasses import dataclass

from django.db import transaction
from django.conf import settings

from main.api.serializers import User
from main.models import Restaurant, Domain


@dataclass
class RestaurantCreator:
    owner: User
    name: str
    address: str

    def __call__(self) -> None:
        with transaction.atomic():
            random_schema_name = self._gen_schema_name()
            tenant = Restaurant.objects.create(
                owner_id=self.owner.id,
                name=self.name,
                address=self.address,
                schema_name=random_schema_name
            )
            Domain.objects.create(
                tenant_id=tenant.id,
                domain=random_schema_name + f'.{settings.DOMAIN}'
            )

    def _gen_schema_name(self) -> str:
        return str(self.owner.id) + ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
