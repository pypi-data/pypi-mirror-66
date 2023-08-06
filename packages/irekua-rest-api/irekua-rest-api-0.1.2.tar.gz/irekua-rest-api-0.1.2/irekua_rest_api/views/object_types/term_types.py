# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from irekua_database import models
from irekua_rest_api import serializers
from irekua_rest_api import filters
from irekua_rest_api import utils

from irekua_rest_api.permissions import IsAdmin
from irekua_rest_api.permissions import IsAuthenticated



class TermTypeViewSet(utils.CustomViewSetMixin, ModelViewSet):
    queryset = models.TermType.objects.all()  # pylint: disable=E1101
    search_fields = filters.term_types.search_fields
    filterset_class = filters.term_types.Filter

    serializer_mapping = (
        utils.SerializerMapping
        .from_module(serializers.object_types.terms)
        .extend(
            terms=serializers.terms.terms.ListSerializer,
            add_term=serializers.terms.terms.CreateSerializer,
            suggestions=serializers.terms.suggestions.ListSerializer,
            suggest_term=serializers.terms.suggestions.CreateSerializer,
            entailment_types=serializers.object_types.entailments.ListSerializer,
            add_entailment_type=serializers.object_types.entailments.CreateSerializer,
            entailments=serializers.terms.entailments.ListSerializer,
            add_entailment=serializers.terms.entailments.CreateSerializer,
            synonyms=serializers.terms.synonyms.ListSerializer,
            add_synonym=serializers.terms.synonyms.CreateSerializer,
            synonym_suggestions=serializers.terms.synonym_suggestions.ListSerializer,
            suggest_synonym=serializers.terms.synonym_suggestions.CreateSerializer,
        ))

    permission_mapping = utils.PermissionMapping({
        utils.Actions.DESTROY: [IsAuthenticated, IsAdmin],
        utils.Actions.CREATE: [IsAuthenticated, IsAdmin],
        utils.Actions.UPDATE: [IsAuthenticated, IsAdmin],
        'add_term': [IsAuthenticated, IsAdmin],
        'add_entailment_type': [IsAuthenticated, IsAdmin],
        'add_entailment': [IsAuthenticated, IsAdmin],
        'add_synonym': [IsAuthenticated, IsAdmin],
    }, default=IsAuthenticated)

    def get_object(self):
        type_pk = self.kwargs['pk']
        term_type = get_object_or_404(models.TermType, pk=type_pk)

        self.check_object_permissions(self.request, term_type)
        return term_type

    def get_serializer_context(self):
        context = super().get_serializer_context()

        try:
            term_type = self.get_object()
        except (KeyError, AssertionError, AttributeError):
            term_type = None

        context['term_type'] = term_type
        return context

    def get_queryset(self):
        if self.action == 'entailments':
            return models.Entailment.objects.all()  # pylint: disable=E1101

        if self.action == 'entailment_types':
            return models.EntailmentType.objects.all()  # pylint: disable=E1101

        if self.action == 'terms':
            term_type_id = self.kwargs['pk']
            return models.Term.objects.filter(term_type=term_type_id)  # pylint: disable=E1101

        if self.action == 'synonyms':
            term_type_id = self.kwargs['pk']
            return models.Synonym.objects.filter(source__term_type=term_type_id)  # pylint: disable=E1101

        if self.action == 'suggestions':
            term_type_id = self.kwargs['pk']
            return models.TermSuggestion.objects.filter(term_type=term_type_id)  # pylint: disable=E1101

        if self.action == 'synonym_suggestions':
            term_type_id = self.kwargs['pk']
            return models.SynonymSuggestion.objects.filter(source__term_type=term_type_id)  # pylint: disable=E1101

        return super().get_queryset()

    @action(detail=False,
            methods=['GET'],
            filterset_class=filters.entailments.Filter,
            search_fields=filters.entailments.search_fields)
    def entailments(self, request):
        return self.list_related_object_view()

    @entailments.mapping.post
    def add_entailment(self, request):
        self.create_related_object_view()

    @action(
        detail=False,
        methods=['GET'],
        filterset_class=filters.entailment_types.Filter,
        search_fields=filters.entailment_types.search_fields)
    def entailment_types(self, request):
        return self.list_related_object_view()

    @entailment_types.mapping.post
    def add_entailment_type(self, request):
        self.create_related_object_view()

    @action(
        detail=True,
        methods=['GET'],
        filterset_class=filters.terms.Filter,
        search_fields=filters.terms.search_fields)
    def terms(self, request, pk=None):
        return self.list_related_object_view()

    @terms.mapping.post
    def add_term(self, request, pk=None):
        return self.create_related_object_view()

    @action(
        detail=True,
        methods=['GET'],
        filterset_class=filters.synonyms.Filter,
        search_fields=filters.synonyms.search_fields)
    def synonyms(self, request, pk=None):
        return self.list_related_object_view()

    @synonyms.mapping.post
    def add_synonym(self, request, pk=None):
        self.create_related_object_view()

    @action(
        detail=True,
        methods=['GET'],
        filterset_class=filters.term_suggestions.Filter,
        search_fields=filters.term_suggestions.search_fields)
    def suggestions(self, request, pk=None):
        return self.list_related_object_view()

    @suggestions.mapping.post
    def suggest_term(self, request, pk=None):
        self.create_related_object_view()

    @action(
        detail=True,
        methods=['GET'],
        filterset_class=filters.synonym_suggestions.Filter,
        search_fields=filters.synonym_suggestions.search_fields)
    def synonym_suggestions(self, request, pk=None):
        return self.list_related_object_view()

    @synonym_suggestions.mapping.post
    def suggest_synonym(self, request, pk=None):
        self.create_related_object_view()
