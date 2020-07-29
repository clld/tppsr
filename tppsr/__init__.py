from pyramid.config import Configurator

from clld.interfaces import IMapMarker, IValueSet, ILanguage, IValue
from clld.web.icon import MapMarker
from clldutils.svg import pie, icon, data_url

# we must make sure custom models are known at database initialization!
from tppsr import models

_ = lambda s: s
_('Language')
_('Languages')
_('Parameter')
_('Parameters')


class LanguageByCantonMapMarker(MapMarker):
    def __call__(self, ctx, req):
        if IValue.providedBy(ctx):
            return data_url(icon('c' + ctx.valueset.language.jsondata['color']))
        if IValueSet.providedBy(ctx):
            return data_url(icon('c' + ctx.language.jsondata['color']))
        elif ILanguage.providedBy(ctx):
            return data_url(icon('c' + ctx.jsondata['color']))
    
        return super(LanguageByCantonMapMarker, self).__call__(ctx, req)



def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clld.web.app')

    config.include('clldmpg')
    config.registry.registerUtility(LanguageByCantonMapMarker(), IMapMarker)
    return config.make_wsgi_app()
