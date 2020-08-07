from sqlalchemy.orm import joinedload
from clld.web import datatables
from clld.web.datatables.base import LinkCol, Col, LinkToMapCol, IntegerIdCol
from clld.web.datatables.parameter import Parameters
from clld.web.datatables.value import Values, ValueSetCol
from clld.web.datatables.sentence import Sentences
from clld.web.util import concepticon
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


class ConceptCol(LinkCol):
    def order(self):
        return as_int(common.Parameter.id)


class Words(Values):
    def get_options(self):
        opts = super(Values, self).get_options()
        if self.parameter:
            opts['aaSorting'] = [[4, 'asc']]
        elif self.language:
            opts['aaSorting'] = [[4, 'asc']]
        return opts

    def col_defs(self):
        ps = Col(self, 'prosodic_structure', model_col=models.Form.prosodic_structure)
        if self.parameter:
            ps.choices = sorted(
                (c for c, in
                 DBSession.query(models.Form.prosodic_structure)
                     .join(common.ValueSet)
                     .filter(common.ValueSet.parameter==self.parameter)
                     .distinct() if c),
                key=lambda s: (len(s), s))

        res = [
            IPACol(self, 'name', sTitle='IPA'),
            Col(self, 'description', sTitle='Form'),
            Col(self, 'segments', sTitle='Segments', model_col=models.Form.segments),
            ps,
        ]
        if self.parameter:
            return res + [
                DialectCol(
                    self,
                    'dialect',
                    get_object=lambda i: i.valueset.language,
                    model_col=common.Language.name),
                LinkToMapCol(self, 'm', get_object=lambda i: i.valueset.language),
            ]

        if self.language:
            return res + [
                ConceptCol(
                    self,
                    'parameter',
                    sTitle=self.req.translate('Parameter'),
                    model_col=common.Parameter.name,
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


class Concepts(Parameters):
    def col_defs(self):
        return [
            Col(self, 'no.', model_col=models.Concept.number, input_size='mini'),
            LinkCol(self, 'name'),
            Col(self, 'latin', model_col=models.Concept.description),
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
            Col(self, 'population', model_col=models.Variety.population),
            Col(self, 'recorded', model_col=models.Variety.recorded, sTitle='Year of recording'),
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
            Col(self, 'name', sTitle='Primary text', sClass="object-language"),
            Col(self, 'original_script', sTitle='Original Transcription'),
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
