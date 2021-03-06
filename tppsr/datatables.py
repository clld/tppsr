from sqlalchemy.orm import joinedload

from clld.web import datatables
from clld.web.datatables.base import LinkCol, Col, LinkToMapCol, IntegerIdCol, DetailsRowLinkCol
from clld.web.datatables.parameter import Parameters
from clld.web.datatables.value import Values, ValueSetCol
from clld.web.datatables.sentence import Sentences
from clld.web.util.helpers import map_marker_img
from clld.web.util.htmllib import HTML
from clld.db.meta import DBSession
from clld.db.models import common
from clld.db.util import icontains, as_int, get_distinct_values

from tppsr import models


class IPACol(LinkCol):
    def order(self):
        return common.Value.name

    def search(self, qs):
        return icontains(common.Value.name, qs)


class DialectCol(LinkCol):
    def order(self):
        return as_int(common.Language.id)

    def format(self, item):
        obj = self.get_obj(item)
        return HTML.a('{}. {}'.format(obj.id, obj.name), href=self.dt.req.resource_url(obj))


class CantonCol(Col):
    def order(self):
        return models.Variety.canton

    def search(self, qs):
        return icontains(models.Variety.canton, qs)

    def format(self, item):
        obj = self.get_obj(item)
        return HTML.div(map_marker_img(self.dt.req, obj), ' {}'.format(obj.canton))



class ConceptCol(LinkCol):
    def order(self):
        return as_int(common.Parameter.id)


class Words(Values):
    def get_options(self):
        opts = super(Values, self).get_options()
        if self.parameter:
            opts['aaSorting'] = [[0, 'asc']]
        elif self.language:
            opts['aaSorting'] = [[4, 'asc']]
        return opts

    def base_query(self, query):
        query = query.join(common.ValueSet).options(joinedload(common.Value.valueset))

        if self.language:
            query = query.join(common.ValueSet.parameter)\
                .options(joinedload(common.Value.valueset).joinedload(common.ValueSet.parameter))
            return query.filter(common.ValueSet.language_pk == self.language.pk)

        if self.parameter:
            query = query.join(common.ValueSet.language)\
                .options(joinedload(common.Value.valueset).joinedload(common.ValueSet.language))
            return query.filter(common.ValueSet.parameter_pk == self.parameter.pk)

        return query

    def col_defs(self):
        ps = Col(self,
                 'prosodic_structure',
                 sTitle='Prosodic structure',
                 model_col=models.Form.prosodic_structure)
        if self.parameter:
            ps.choices = sorted(
                (c for c, in
                 DBSession.query(models.Form.prosodic_structure)
                     .join(common.ValueSet)
                     .filter(common.ValueSet.parameter==self.parameter)
                     .distinct() if c),
                key=lambda s: (len(s), s))

        res = [
            Col(self, 'description', sTitle='TPPSR form', sClass="object-language"),
            IPACol(self, 'name', sTitle='IPA form', sClass="ipa-text"),
            Col(self, 'segments', sTitle='Segments', model_col=models.Form.segments, sClass="ipa-text"),
            ps,
        ]
        if self.parameter:
            return [
                DialectCol(
                    self,
                    'dialect',
                    get_object=lambda i: i.valueset.language,
                    model_col=common.Language.name),
                CantonCol(
                    self,
                    'canton',
                    get_object=lambda i: i.valueset.language,
                    choices=get_distinct_values(models.Variety.canton),
                ),
                LinkToMapCol(self, 'm', get_object=lambda i: i.valueset.language),
            ] + res

        if self.language:
            return res + [
                ConceptCol(
                    self,
                    'parameter',
                    sTitle=self.req.translate('Parameter'),
                    model_col=models.Concept.concepticon_gloss,
                    get_object=lambda i: i.valueset.parameter),
                Col(
                    self,
                    'french',
                    sTitle='French gloss',
                    model_col=models.Concept.french_gloss,
                    get_object=lambda i: i.valueset.parameter),
            ]

        return res + [
            ValueSetCol(self, 'valueset', bSearchable=False, bSortable=False),
        ]


class ConcepticonCol(Col):
    def order(self):
        return models.Concept.concepticon_gloss

    def format(self, item):
        return item.concepticon_link(self.dt.req)


class ConceptLinkCol(LinkCol):
    def get_attrs(self, item):
        return {'label': item.french_gloss}


class Concepts(Parameters):
    def col_defs(self):
        return [
            Col(self, 'no.', model_col=models.Concept.number, input_size='mini'),
            LinkCol(self, 'name', sTitle="Concept"),
            Col(self, 'name', sTitle="French gloss", model_col=models.Concept.french_gloss),
            Col(self, 'latin', model_col=models.Concept.latin_gloss, sTitle='Latin gloss'),
            ConcepticonCol(self, 'concepticon'),
        ]


class Languages(datatables.Languages):
    def col_defs(self):
        return [
            IntegerIdCol(self, 'number'),
            LinkCol(self, 'name'),
            Col(self,
                'canton',
                sTitle='Canton',
                model_col=models.Variety.canton,
                choices=get_distinct_values(models.Variety.canton),
            ),
            Col(self,
                'group',
                sTitle='Dialect group',
                model_col=models.Variety.group,
                choices=get_distinct_values(models.Variety.group),
            ),
            #Col(self, 'population', model_col=models.Variety.population),
            Col(self, 'recorded', model_col=models.Variety.recorded, sTitle='Date of recording'),
            Col(self,
                'latitude',
                sDescription='<small>The geographic latitude</small>'),
            Col(self,
                'longitude',
                sDescription='<small>The geographic longitude</small>'),
            LinkToMapCol(self, 'm'),
        ]


class Phrases(Sentences):
    def col_defs(self):
        res = [
            Col(self, 'name', sTitle='Primary Text', sClass="ipa-text"),
            Col(self, 'original_script', sTitle='Original Transcription', sClass="object-language"),
            Col(self,
                'description',
                sTitle=self.req.translate('Translation'),
                sClass="translation"),
        ]
        if not self.language:
            res.append(
                DialectCol(
                    self,
                    'language',
                    model_col=common.Language.name,
                    get_obj=lambda i: i.language,
                )
            )
        res.append(DetailsRowLinkCol(self, 'd'))
        return res

    def get_options(self):
        opts = super(Phrases, self).get_options()
        if not self.language:
            opts['aaSorting'] = [[2, 'asc'], [3, 'asc']]
        return opts


def includeme(config):
    config.register_datatable('values', Words)
    config.register_datatable('sentences', Phrases)
    config.register_datatable('languages', Languages)
    config.register_datatable('parameters', Concepts)
