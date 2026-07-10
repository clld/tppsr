from clld.db.meta import DBSession
from clld.db.models import common
from clld.web.util.htmllib import HTML
from clld.web.util.helpers import link

from tppsr import models


def language_detail_html(context=None, request=None, **kw):
    return context.render_inventory(request=request)


def scan_webscale(scan):
    base, sep, _ = scan.partition('-0_')
    return base + sep + 'web.jpg'


def parameter_detail_html(context=None, request=None, **kw):
    return {'scans': sorted(set(
        (r[0], scan_webscale(r[0]))
        for r in DBSession.query(models.Form.scan)
        .join(common.ValueSet)
        .filter(common.ValueSet.parameter==context)
    ), key=lambda i: i[0].split('-0_')[-1])}


def rendered_sentence_concepts(sentence, req, concept=None):
    units = []
    for i, (_, c) in enumerate(sentence.iter_form_and_concept()):
        units.extend([
            '\u00a0' if i != 0 else '',
            link(req, c, label=c.french_gloss) if concept != c else c.french_gloss,
        ])
    return HTML.span(*units)


def rendered_sentence(sentence, req, form=None):
    units = []
    for i, (f, concept) in enumerate(sentence.iter_form_and_concept()):
        units.append(HTML.div(
            HTML.div(
                link(req, f, label=f.description) if f != form else f.description,
                class_='original-script'),
            HTML.div(f.name, class_='object-language'),
            HTML.div(
                link(req, concept, label=concept.french_gloss) if f != form else concept.french_gloss,
            ),
            class_='gloss-unit',
        ))

    return HTML.div(
        HTML.div(
            HTML.div(
                HTML.div(*units, **{'class': 'gloss-box'}) if units else '',
                class_='body',
            ),
            class_="sentence",
        ),
        class_="sentence-wrapper",
    )
