<%inherit file="../home_comp.mako"/>


<%def name="sidebar()">
    <div class="well well-small">
        <h4>Cite as</h4>
        <blockquote>
            Hans Geisler, Robert Forkel, & Johann-Mattis List. (2020).
            CLDF dataset derived from Gauchat et al.'s "Tableaux phonétiques des patois suisses romands" from 1925 (Version v1.0)
            [Data set]. Zenodo. <a href="http://doi.org/10.5281/zenodo.3988472">DOI: 10.5281/zenodo.3988472</a>
        </blockquote>
    </div>
</%def>


<h2>The "Tableaux phonétiques des patois suisses romands" Online</h2>

<p>
    The <a href="${req.route_url('source', id='Gauchat1925')}">"Tableaux phonétiques des patois suisses romands"</a> presents
    data recorded between 1904 and 1907 in
    <a href="${req.route_url('languages')}">62 villages</a> to document
    a puzzling variety of French and Franco-Provençal dialects that is
    unparalleled in the Romance-speaking world.
</p>
<p>
    Louis Gauchat and his collaborators Jules Jeanjaquet and Ernest Tappolet
    collected data for a questionnaire consisting of
    <a href="${req.route_url('sentences')}">short sentences</a> that deal with everyday
    rural life. The questionnaire focuses on phonetics but covers also characteristic
    morphological and lexical features of local dialects.
</p>
<p>
    The sentences were split up in words, each representing
    <a href="${req.route_url('parameters')}">a single concept</a>,
    which are arranged in tabular form containing the phonetic realizations at the
    queried local dialects as cell values.
</p>

<div style="text-align: center">
    <iframe src="https://archive.org/embed/gauchat-et-al-1925-tppsr" width="560" height="384" frameborder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe>
</div>
