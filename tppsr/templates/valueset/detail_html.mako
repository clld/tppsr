<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>


<h2>${_('Value Set')} ${h.link(request, ctx.language)}/${h.link(request, ctx.parameter)}</h2>

% if ctx.description:
${h.text2html(h.Markup(ctx.markup_description) if ctx.markup_description else ctx.description, mode='p')}
% endif

% for i, value in enumerate(ctx.values):
<dl>
    <dt>TPPSR form:</dt>
    <dd class="object-language">${value.description}</dd>
    <dt>IPA form:</dt>
    <dd class="ipa-text">${value.name}</dd>
    <dt>Segments:</dt>
    <dd class="ipa-text">${value.segments}</dd>
    <dt>Prosodic structure:</dt>
    <dd>${value.prosodic_structure}</dd>
    <dt class="language">${_('Language')}:</dt>
    <dd class="language">${h.link(request, ctx.language)} (${ctx.language.canton})</dd>
    <dt class="parameter">${_('Parameter')}:</dt>
    <dd class="parameter">${h.link(request, ctx.parameter)} / ${ctx.parameter.french_gloss}</dd>
</dl>
    % if value.sentence_assocs:
        <h3>Sentences</h3>
        <ul class="unstyled">
            % for phrase in value.sentence_assocs:
                ##<li>${h.rendered_sentence(phrase.sentence)|n}</li>
                <li>
                    <blockquote>
                        ${u.rendered_sentence(phrase.sentence, req, value)|n}
                    </blockquote>
                </li>
            % endfor
        </ul>
    % endif
% endfor
<%def name="sidebar()">
<div class="well well-small">
<dl>
    <dt class="source">${_('Source')}:</dt>
        <dd class="source">${h.linked_references(request, ctx)|n}</dd>
        <dd>
            <a href="${ctx.values[0].scan}" target="_blank" title="click for full-size scan">
                <img class="img-polaroid"
                     src="${u.scan_webscale(ctx.values[0].scan)}"/>
            </a>
        </dd>
</dl>
</div>
</%def>
