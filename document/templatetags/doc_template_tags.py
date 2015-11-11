# -*- coding:utf-8 -*-

__author__ = 'M.Y'
from django import template

register = template.Library()


@register.filter
def get_parents_level(level_obj):
    parents = []
    while level_obj is not None:
        parents.append(level_obj)
        level_obj = level_obj.parent

    return reversed(parents)


@register.filter
def render_levels_tree(levels):
    from document.util import LevelHandler

    return LevelHandler(levels).render_tree()


@register.filter
def render_edit_levels_tree(levels):
    from document.util import LevelHandler

    return LevelHandler(levels, edit=True).render_tree()


@register.filter
def render_levels_content(levels):
    from document.util import LevelHandler

    return LevelHandler(levels).render_content()


@register.filter
def first_child(level):
    child = level.children.all()[:1]
    return child[0].id if child else 0


@register.simple_tag
def hex_to_rgba(value, opacity):
    value = value.lstrip('#')
    lv = len(value)
    return "rgba" + str(tuple(list(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3)) + [opacity]))

@register.filter
def inside_body(val):
    return val.split('<body>')[1].split('</body>')[0]