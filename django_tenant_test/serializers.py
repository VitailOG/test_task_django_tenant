from rest_framework import serializers


class Serializer(serializers.Serializer):

    @property
    def validated_data(self):
        validated_data = super().validated_data

        if not hasattr(self, 'Meta'):
            return validated_data

        if not hasattr(self.Meta, 'exclude_fields'):
            return validated_data

        for fields in validated_data:
            if fields in self.Meta.exclude_fields:
                validated_data.pop(fields)
        return validated_data
