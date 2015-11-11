from django import template
from django.utils.encoding import smart_text
from comment.models import ThreadedComment

from comment.util import annotate_tree_properties, fill_tree as real_fill_tree, CommentHandler

register = template.Library()


@register.filter
def render_tree(comments):
    return CommentHandler(comments).render()


@register.simple_tag
def render_tree_inline(content_type_id, obj_id):
    comments = ThreadedComment.objects.filter(
        content_type_id=content_type_id,
        object_pk=smart_text(obj_id),
        active=True,
    ).order_by('id')

    return CommentHandler(comments).render_comments_inline()


@register.filter
def annotate_tree(comments):
    """
    Add ``open``, ``close`` properties to the comments, to render the tree.

    Syntax::

        {% for comment in comment_list|annotate_tree %}
            {% ifchanged comment.parent_id %}{% else %}</li>{% endifchanged %}
            {% if not comment.open and not comment.close %}</li>{% endif %}
            {% if comment.open %}<ul>{% endif %}

            <li id="c{{ comment.id }}">
                ...
            {% for close in comment.close %}</li></ul>{% endfor %}
        {% endfor %}

    When the :func:`fill_tree` filter, place the ``annotate_tree`` code after it::

        {% for comment in comment_list|fill_tree|annotate_tree %}
            ...
        {% endfor %}
    """
    return annotate_tree_properties(comments)


@register.filter
def fill_tree(comments):
    """
    When paginating the comments, insert the parent nodes of the first comment.

    Syntax::

        {% for comment in comment_list|annotate_tree %}
            ...
        {% endfor %}
    """
    return real_fill_tree(comments)
