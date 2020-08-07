<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">${_('Languages')}</%block>

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

<h2>${_('Languages')}</h2>

% if map_ or request.map:
${(map_ or request.map).render()}
% endif

<div id="table-container">
    ${ctx.render()}
</div>

<%block name="javascript">
    $(window).load(function() {$('#legend-layers .dropdown-toggle').dropdown('toggle');})
</%block>
