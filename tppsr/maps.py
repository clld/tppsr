import itertools

from clldutils.misc import slug
from clld.db.meta import DBSession
from clld.db.util import as_int
from clld.db.models import common
from clld.web.maps import Map, ParameterMap, LanguageMap, Legend, Layer
from clld.web.adapters.geojson import GeoJson
from clld.web.util import helpers
from clld.web.util.htmllib import HTML, literal

from tppsr import models


class DialectsGeoJson(GeoJson):
    def feature_iterator(self, ctx, req):
        return ctx

    def feature_properties(self, ctx, req, feature):
        return {
            'language': {
                'id': feature.id,
                'name': feature.name,
            }
        }


class LanguagesMap(Map):
    def get_layers(self):
        for canton, dialects in itertools.groupby(
            DBSession
            .query(models.Variety)
            .order_by(models.Variety.canton, as_int(common.Language.id)),
            lambda l: l.canton
        ):
            dialects = list(dialects)
            json = DialectsGeoJson(None).render(dialects, self.req, dump=False)
            yield Layer(
                slug(canton),
                canton,
                data=json,
                marker=HTML.span(
                    helpers.map_marker_img(self.req, dialects[0], marker=self.map_marker),
                    literal('&nbsp;'),
                    dialects[0].canton_img(self.req),
                    literal('&nbsp;'))
            )

    def get_options(self):
        return {'max_zoom': 15}


class WordMap(ParameterMap):
    def get_options(self):
        return {
            'max_zoom': 15,
            'show_labels': True,
        }


class DialectMap(LanguageMap):
    def get_options(self):
        return {
            'zoom': 10,
            'max_zoom': 15,
        }


def includeme(config):
    config.register_map('languages', LanguagesMap)
    config.register_map('language', DialectMap)
    config.register_map('parameter', WordMap)
