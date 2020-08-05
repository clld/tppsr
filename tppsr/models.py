from zope.interface import implementer
from sqlalchemy import (
    Column,
    String,
    Unicode,
    Integer,
    Boolean,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.models import common
from clld.web.util.htmllib import HTML
from clldutils.misc import slug
from pyclts.ipachart import Segment

from clld_glottologfamily_plugin.models import HasFamilyMixin


@implementer(interfaces.ILanguage)
class Variety(CustomModelMixin, common.Language, HasFamilyMixin):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)
    canton = Column(Unicode)
    population = Column(Integer)
    speaker_age = Column(Integer)
    speaker_proficiency = Column(Unicode)
    speaker_language_use = Column(Unicode)
    speaker_note = Column(Unicode)

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


#ID,Local_ID,Language_ID,Parameter_ID,Value,Form,Segments,Comment,Source,Cognacy,Loan,Graphemes,Profile,Scan,ProsodicStructure
#1-Gauchat-1925-480-1_ilfait-1,,1,Gauchat-1925-480-1_ilfait,yė fā,jə fa̠ː,j ə + f aː,,Gauchat1925[2],,,,^ y ė + f ā $,0020,CV_CV
@implementer(interfaces.IValue)
class Form(CustomModelMixin, common.Value):
    pk = Column(Integer, ForeignKey('value.pk'), primary_key=True)
    segments = Column(Unicode)
    scan = Column(Unicode)
    prosodic_structure = Column(Unicode)
