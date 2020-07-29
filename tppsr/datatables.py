from sqlalchemy.orm import joinedload
from clld.web import datatables
from clld.web.datatables.base import LinkCol, Col, LinkToMapCol
from clld.web.datatables.parameter import Parameters
from clld.web.util import concepticon

from tppsr import models


class ConcepticonCol(Col):
    def order(self):
        return models.Concept.concepticon_gloss

    def format(self, item):
        return concepticon.link(
            self.dt.req,
            id=item.concepticon_concept_id,
            label=item.concepticon_concept_id,
            obj_type='Concept')


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
            LinkCol(self, 'name'),
            Col(self, 'description', sTitle='Canton'),
            Col(self,
                'latitude',
                sDescription='<small>The geographic latitude</small>'),
            Col(self,
                'longitude',
                sDescription='<small>The geographic longitude</small>'),
            LinkToMapCol(self, 'm'),
        ]



def includeme(config):
    config.register_datatable('languages', Languages)
    config.register_datatable('parameters', Concepts)
