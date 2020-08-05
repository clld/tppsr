<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%! multirow = True %>

<%block name="title">${_('Language')} ${ctx.name}</%block>

<%block name="head">
    <style>
        table caption {
            text-align: left;
        }

        figure {
            display: table;
            margin-left: 0px;
        }

        figcaption {
            display: table-caption;
            caption-side: top;
            font-size: 120%;
        }

            ${vowels_css}
            ${consonants_css}
    </style>
</%block>

<div class="row-fluid">
    <div class="span12">
        <h2>${_('Language')} ${ctx.name}</h2>
    </div>
</div>
<div class="row-fluid">
    <div class="span8">
        <table class="table table-condensed table-nonfluid">
            <tr>
                <th>Canton</th>
                <td>${ctx.canton}</td>
            </tr>
            <tr>
                <th>Population</th>
                <td>${ctx.population or ''}</td>
            </tr>
            <tr>
                <th>Speaker age</th>
                <td>${ctx.speaker_age or ''}</td>
            </tr>
            <tr>
                <th>Speaker proficiency</th>
                <td>${ctx.speaker_proficiency or ''}</td>
            </tr>
            <tr>
                <th>Speaker language use</th>
                <td>${ctx.speaker_language_use or ''}</td>
            </tr>
            <tr>
                <th>Note on speaker</th>
                <td>${ctx.speaker_note or ''}</td>
            </tr>
        </table>
    </div>
    <div class="span4">
        <div class="well well-small">
            ${request.map.render()}
        </div>
    </div>
</div>

<div class="row-fluid">
<div class="tabbable" style="clear: both">
    <ul class="nav nav-tabs">
        <li class="active"><a href="#words" data-toggle="tab">Words</a></li>
        <li><a href="#ipa" data-toggle="tab">Phoneme inventory</a></li>
    </ul>
    <div class="tab-content" style="overflow: visible;">
        <div id="words" class="tab-pane active">
            ${request.get_datatable('values', h.models.Value, language=ctx).render()}
        </div>
        <div id="ipa" class="tab-pane">
            ${consonants_html|n}
            ${vowels_html|n}

            <table class="table table-condensed table-nonfluid">
                <caption>Other phonemes</caption>
                <tbody>
                    % for seg in uncovered:
                        <tr>
                            <th>${seg.sound_bipa}</th>
                            <td>${seg.sound_name}</td>
                        </tr>
                    % endfor
                </tbody>
            </table>
        </div>
    </div>
    <script>
        $(document).ready(function () {
            if (location.hash !== '') {
                $('a[href="#' + location.hash.substr(2) + '"]').tab('show');
            }
            return $('a[data-toggle="tab"]').on('shown', function (e) {
                return location.hash = 't' + $(e.target).attr('href').substr(1);
            });
        });
    </script>
</div>
</div>