from zope.interface import implementer
from sqlalchemy import (
    Column,
    Unicode,
    Integer,
    ForeignKey,
)

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.models import common
from clld.web.util.htmllib import HTML
from clld.web.util import concepticon
from clldutils.misc import slug
from pyclts.ipachart import Segment

from clld_glottologfamily_plugin.models import HasFamilyMixin


@implementer(interfaces.ILanguage)
class Variety(CustomModelMixin, common.Language, HasFamilyMixin):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)
    canton = Column(Unicode)
    population = Column(Integer)
    group = Column(Unicode)
    recorded = Column(Integer)
    speaker_age = Column(Integer)
    speaker_proficiency = Column(Unicode)
    speaker_language_use = Column(Unicode)
    speaker_gender = Column(Unicode)

    @property
    def inventory(self):
        return [Segment(
            sound_bipa=k,
            sound_name=v,
            href='https://clts.clld.org/parameters/{}'.format(v.replace(' ', '_')),
        ) for k, v in self.jsondata['inventory']]

    def canton_img(self, req):
        return HTML.img(
            width=20,
            src=req.static_url('tppsr:static/{}.png'.format(slug(self.canton))))


@implementer(interfaces.IParameter)
class Concept(CustomModelMixin, common.Parameter):
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
    number = Column(Integer)
    concepticon_id = Column(Unicode)
    concepticon_gloss = Column(Unicode)
    concepticon_concept_id = Column(Unicode)

    def concepticon_link(self, req):
        return concepticon.link(
            req,
            id=self.concepticon_concept_id,
            label=self.concepticon_concept_id,
            obj_type='Concept')


@implementer(interfaces.IValue)
class Form(CustomModelMixin, common.Value):
    pk = Column(Integer, ForeignKey('value.pk'), primary_key=True)
    segments = Column(Unicode)
    scan = Column(Unicode)
    prosodic_structure = Column(Unicode)
