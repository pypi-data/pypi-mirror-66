from django.db import models
from dal import autocomplete

from irekua_database import models as irekua_models


class InstitutionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = irekua_models.Institution.objects.all()

        if self.q:
            institution_name_query = models.Q(institution_name__istartswith=self.q)
            institution_code_query = models.Q(institution_code__istartswith=self.q)
            subdependency_query = models.Q(subdependency__istartswith=self.q)
            qs = qs.filter(
                institution_name_query |
                institution_code_query |
                subdependency_query)

        return qs


class DeviceBrandAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = irekua_models.DeviceBrand.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class DeviceAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = irekua_models.Device.objects.all()

        if self.q:
            brand_query = models.Q(brand__name__istartswith=self.q)
            model_query = models.Q(model__istartswith=self.q)
            type_query = models.Q(device_type__name__istartswith=self.q)
            qs = qs.filter(brand_query | model_query | type_query)

        return qs


class CollectionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = irekua_models.Collection.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class CollectionTypeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = irekua_models.CollectionType.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class MetacollectionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = irekua_models.MetaCollection.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class TermsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = irekua_models.Term.objects.all()

        term_type = self.forwarded.get('term_type', None)

        if term_type:
            qs = qs.filter(term_type=term_type)

        if self.q:
            qs = qs.filter(value__istartswith=self.q)

        return qs


class TagsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = irekua_models.Tag.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class AnnotationToolsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = irekua_models.AnnotationTool.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class SamplingEventTypesAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = irekua_models.SamplingEventType.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = irekua_models.User.objects.all()

        if self.q:
            qs = qs.filter(email__istartswith=self.q)

        return qs

    def get_result_label(self, item):
        return item.email


class LocalityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = irekua_models.Locality.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

    def get_result_label(self, item):
        label = '{type}: {name}'.format(name=item.name, type=item.locality_type)

        if item.is_part_of.exists():
            part_of = ', '.join([part.name for part in item.is_part_of.all()])
            label = '{label} ({part_of})'.format(label=label, part_of=part_of)

        return label


class SiteDescriptorAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = irekua_models.SiteDescriptor.objects.all()

        if self.q:
            qs = qs.filter(value__icontains=self.q)

        if 'type' in self.request.GET:
            qs = qs.filter(descriptor_type=self.request.GET['type'])

        return qs

    def get_result_label(self, item):
        return item.value
