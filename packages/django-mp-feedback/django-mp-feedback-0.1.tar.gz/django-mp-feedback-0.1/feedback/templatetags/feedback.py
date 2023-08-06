
from django import template


register = template.Library()


@register.inclusion_tag(
    'feedback/form-js.html',
    takes_context=True,
    name='feedback_form_js')
def render_feedback_form_js(context):
    return context


@register.inclusion_tag(
    'feedback/modal-js.html',
    takes_context=True,
    name='feedback_modal_js')
def render_feedback_modal_js(context):
    return context
