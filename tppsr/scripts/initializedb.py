import itertools
import collections

from csvw.dsv import reader
from pyclts import CLTS
from pycldf import Sources
from clldutils.misc import nfilter, slug
from clldutils.color import qualitative_colors
from clld.cliutil import Data, bibtex2source
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib import bibtex
from nameparser import HumanName

import tppsr
from tppsr import models


def iteritems(cldf, t, *cols):  # pragma: no cover
    cmap = {cldf[t, col].name: col for col in cols}
    for item in cldf[t]:
        for k, v in cmap.items():
            item[v] = item[k]
        yield item


def main(args):  # pragma: no cover
    data = Data()
    clts = CLTS(input('Path to cldf-clts/clts:') or '../../cldf-clts/clts')
    ds = data.add(
        common.Dataset,
        tppsr.__name__,
        id=tppsr.__name__,
        name='Tableaux phonétiques des patois suisses romands Online',
        domain='tppsr.clld.org',

        publisher_name="Max Planck Institute for Evolutionary Anthropology",
        publisher_place="Leipzig",
        publisher_url="https://www.eva.mpg.de",
        license="https://creativecommons.org/licenses/by/4.0/",
        jsondata={
            'license_icon': 'cc-by.png',
            'license_name': 'Creative Commons Attribution 4.0 International License'},
    )
    for i, name in enumerate(['Hans Geisler', 'Robert Forkel', 'Johann-Mattis List']):
        common.Editor(
            dataset=ds,
            ord=i,
            contributor=common.Contributor(id=slug(HumanName(name).last), name=name)
        )

    contrib = data.add(
        common.Contribution,
        None,
        id='cldf',
        name=args.cldf.properties.get('dc:title'),
        description=args.cldf.properties.get('dc:bibliographicCitation'),
    )

    def norm_group(s):
        return 'Franco-Provençal' if s.startswith('Franco') else "Langue d'oïl franc-comtois"

    for lang in iteritems(args.cldf, 'LanguageTable', 'id', 'name', 'latitude', 'longitude'):
        data.add(
            models.Variety,
            lang['id'],
            id=lang['Number'],
            name=lang['name'],
            latitude=lang['latitude'],
            longitude=lang['longitude'],
            canton=lang['Canton'],
            group=norm_group(lang['DialectGroup']),
            recorded=int(lang['YearOfRecording']) if lang['YearOfRecording'] else None,
            population=int(lang['Population']) if lang['Population'] else None,
            speaker_age=int(lang['SpeakerAge']) if lang['SpeakerAge'] else None,
            speaker_proficiency=lang['SpeakerProficiency'],
            speaker_language_use=lang['SpeakerLanguageUse'],
            speaker_gender=lang['SpeakerGender'],
        )
    colors = qualitative_colors(len(set(l.canton for l in data['Variety'].values())), set='tol')
    for i, (_, langs) in enumerate(itertools.groupby(
        sorted(data['Variety'].values(), key=lambda l: l.canton),
        lambda l: l.canton,
    )):
        for lang in langs:
            lang.update_jsondata(color=colors[i])

    for rec in bibtex.Database.from_file(args.cldf.bibpath, lowercase=True):
        data.add(common.Source, rec.id, _obj=bibtex2source(rec))

    phrase_map = collections.OrderedDict()  # maps (phrase number, language ID) pairs to Sentence instances
    for example in args.cldf['ExampleTable']:
        phrase_map[tuple(example['ID'].split('-'))] = common.Sentence(
            id=example['ID'],
            language=data['Variety'][example['Language_ID']],
            name=example['Primary_Text'],
            description=example['Translated_Text'],
            original_script=example['Alt_Transcription'],
        )
    phrases_by_concept = collections.defaultdict(list)
    for row in reader(
            args.cldf.tablegroup._fname.parent / '..' / 'etc' / 'phrases.csv', dicts=True):
        for cid in row['Concepts'].split():
            phrases_by_concept[cid].append(row['ID'])

    refs = collections.defaultdict(list)

    for param in iteritems(args.cldf, 'ParameterTable', 'id', 'concepticonReference', 'name'):
        c = data.add(
            models.Concept,
            param['id'],
            id=param['Number'],
            number=int(param['Number']),
            name='{} [{}]'.format(param['name'], param['Number']),
            latin_gloss=param['Latin_Gloss'],
            french_gloss=param['French_Gloss'],
            concepticon_id=param['concepticonReference'],
            concepticon_gloss=param['Concepticon_Gloss'],
            concepticon_concept_id=param['id'].split('_')[0],
        )
        phrase_id = phrases_by_concept.get(str(param['Number']), [None])[0]
        if phrase_id:
            for (pid, _), phrase in phrase_map.items():
                if pid == phrase_id:
                    DBSession.add(models.ConceptSentence(concept=c, sentence=phrase))
                    break

    inventories = collections.defaultdict(set)
    scan_url_template = args.cldf['FormTable', 'Scan'].valueUrl
    for form in iteritems(args.cldf, 'FormTable', 'id', 'value', 'form', 'languageReference', 'parameterReference', 'source'):
        if not form['form']:
            continue
        inventories[form['languageReference']] = inventories[form['languageReference']].union(form['Segments'])
        vsid = (form['languageReference'], form['parameterReference'])
        vs = data['ValueSet'].get(vsid)
        if not vs:
            vs = data.add(
                common.ValueSet,
                vsid,
                id='-'.join(vsid),
                language=data['Variety'][form['languageReference']],
                parameter=data['Concept'][form['parameterReference']],
                contribution=contrib,
            )
        for ref in form.get('source', []):
            sid, pages = Sources.parse(ref)
            refs[(vsid, sid)].append(pages)
        f = data.add(
            models.Form,
            form['id'],  # Gauchat-1925-480-1_
            id=form['id'],
            name=form['form'].replace('+', ' '),
            description=form['value'],
            segments=' '.join(form['Segments']),
            valueset=vs,
            scan=scan_url_template.expand(**form),
            prosodic_structure=form['ProsodicStructure'],
        )
        for phrase_id in phrases_by_concept.get(str(vs.parameter.number), []):
            phrase = phrase_map.get((phrase_id, form['languageReference']))
            if phrase:
                DBSession.add(common.ValueSentence(value=f, sentence=phrase))

    for lid, inv in inventories.items():
        inv = [clts.bipa[c] for c in inv]
        data['Variety'][lid].update_jsondata(
            inventory=[(str(c), c.name) for c in inv if hasattr(c, 'name')])

    for (vsid, sid), pages in refs.items():
        DBSession.add(common.ValueSetReference(
            valueset=data['ValueSet'][vsid],
            source=data['Source'][sid],
            description='; '.join(nfilter(pages))
        ))


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
