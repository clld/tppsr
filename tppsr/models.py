from zope.interface import implementer
from sqlalchemy import (
    Column,
    Unicode,
    Integer,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.models import common
from clld.web.util.htmllib import HTML
from clld.web.util import concepticon
from clldutils.misc import slug
from pyclts.ipachart import Segment


@implementer(interfaces.ISentence)
class Phrase(CustomModelMixin, common.Sentence):
    pk = Column(Integer, ForeignKey('sentence.pk'), primary_key=True)

    def iter_form_and_concept(self):
        for va in sorted(self.value_assocs, key=lambda i: i.value.valueset.parameter.number):
            yield va.value, va.value.valueset.parameter


@implementer(interfaces.ILanguage)
class Variety(CustomModelMixin, common.Language):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)
    canton = Column(Unicode)
    population = Column(Integer)
    group = Column(Unicode)
    recorded = Column(Unicode)
    speaker_age = Column(Integer)
    speaker_proficiency = Column(Unicode)
    speaker_language_use = Column(Unicode)
    speaker_gender = Column(Unicode)
    investigators = Column(Unicode)

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
    french_gloss = Column(Unicode)
    latin_gloss = Column(Unicode)
    concepticon_id = Column(Unicode)
    concepticon_gloss = Column(Unicode)
    concepticon_concept_id = Column(Unicode)

    def concepticon_link(self, req):
        return concepticon.link(
            req,
            id=self.concepticon_concept_id,
            label=self.concepticon_gloss or self.concepticon_concept_id,
            obj_type='Concept')

    def iter_phrases(self):
        seen = set()
        for sa in self.sentence_assocs:
            if sa.sentence.description not in seen:
                seen.add(sa.sentence.description)
                yield sa.sentence


@implementer(interfaces.IValue)
class Form(CustomModelMixin, common.Value):
    pk = Column(Integer, ForeignKey('value.pk'), primary_key=True)
    segments = Column(Unicode)
    scan = Column(Unicode)
    prosodic_structure = Column(Unicode)


class ConceptSentence(Base):
    concept_pk = Column(Integer, ForeignKey('concept.pk'), nullable=False)
    sentence_pk = Column(Integer, ForeignKey('sentence.pk'), nullable=False)

    concept = relationship(Concept, innerjoin=True, backref='sentence_assocs')
    sentence = relationship(
        common.Sentence, innerjoin=True, backref='concept_assocs', order_by=common.Sentence.id)
