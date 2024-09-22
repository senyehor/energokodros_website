from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from institutions.models import Facility


class FacilitySerializer(ModelSerializer):
    parent_facility = PrimaryKeyRelatedField(
        queryset=Facility.objects.all(),
        write_only=True
    )

    class Meta:
        model = Facility
        fields = ('pk', 'name', 'description', 'parent_facility')

    def create(self, validated_data):
        parent: Facility = validated_data.pop('parent_facility')
        new_facility = self.Meta.model(**validated_data)
        parent.add_child(instance=new_facility)
        new_facility.save()
        return new_facility
