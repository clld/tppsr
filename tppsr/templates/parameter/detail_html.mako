<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<%block name="title">${_('Parameter')} ${ctx.name}</%block>

<ul class="nav nav-pills" style="float: right">
    <li class="">
        <a href="#map-container">
            <img src="${req.static_url('tppsr:static/Map_Icon.png')}"
                 width="35">
            Map
        </a>
    </li>
    <li class="">
        <a href="#table-container">
            <img src="${req.static_url('tppsr:static/Table_Icon.png')}"
                 width="35">
            Table
        </a>
    </li>
</ul>

<h2>${_('Parameter')} ${ctx.name} / ${ctx.french_gloss}</h2>

<div style="width: 60%">
    <table class="table table-nonfluid">
        % if ctx.phrase:
            <tr>
                <th>Sentence:</th>
                <td>${ctx.phrase}</td>
            </tr>
        % endif
        <tr>
            <th>Latin/Proto-Romance:</th>
            <td>${ctx.latin_gloss}</td>
        </tr>
        <tr>
            <th>Concepticon:</th>
            <td>${ctx.concepticon_link(request)|n}</td>
        </tr>
    </table>
</div>

% if map_ or request.map:
${(map_ or request.map).render()}
% endif

<div class="tabbable" style="clear: both" id="table-container">
    <ul class="nav nav-tabs">
        <li class="active"><a href="#words" data-toggle="tab">Forms</a></li>
        <li><a href="#source" data-toggle="tab">Source</a></li>
    </ul>
    <div class="tab-content" style="overflow: visible;">
        <div id="words" class="tab-pane active">
            ${request.get_datatable('values', h.models.Value, parameter=ctx).render()}
        </div>
        <div id="source" class="tab-pane">
            % for scan in scans:
                <div style="text-align: center; font-size: larger"><strong>${ctx}</strong></div>
                <img style="width: 100%" src="${scan}"/>
            % endfor
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
