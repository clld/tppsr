from pyramid.config import Configurator

from clld.interfaces import IMapMarker, IValueSet, ILanguage, IValue, ILinkAttrs
from clld.web.icon import MapMarker
from clldutils.svg import icon, data_url
from clldutils.misc import slug

# we must make sure custom models are known at database initialization!
from tppsr import models

_ = lambda s: s
_('Language')
_('Languages')
_('Parameter')
_('Parameters')
_('Value')
_('Values')
_('ValueSet')
_('ValueSets')


class LanguageByCantonMapMarker(MapMarker):
    def __call__(self, ctx, req):
        if IValue.providedBy(ctx):
            return data_url(icon('c' + ctx.valueset.language.jsondata['color']))
        if IValueSet.providedBy(ctx):
            return data_url(icon('c' + ctx.language.jsondata['color']))
        elif ILanguage.providedBy(ctx):
            return data_url(icon('c' + ctx.jsondata['color']))
    
        return super(LanguageByCantonMapMarker, self).__call__(ctx, req)  # pragma: no cover


def link_attrs(req, obj, **kw):
    if IValue.providedBy(obj):
        # redirect value details to valueset details:
        kw['href'] = req.route_url('valueset', id=obj.valueset.id, **kw.pop('url_kw', {}))
    return kw


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clld.web.app')

    config.include('clldmpg')
    config.registry.registerUtility(LanguageByCantonMapMarker(), IMapMarker)
    config.registry.registerUtility(link_attrs, ILinkAttrs)
    return config.make_wsgi_app()
