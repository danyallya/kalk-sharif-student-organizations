from itertools import chain
from django.template.defaultfilters import linebreaksbr

__all__ = ['fill_tree', 'annotate_tree_properties', ]


class CommentHandler:
    def __init__(self, comments):
        self.comments = list(comments)
        self.comments_children = {}

    def render(self):
        self.__create_comment_tree()

        root_comments = filter(lambda comment: not comment.parent_id, self.comments)

        return self.__render_comments(root_comments)

    def __create_comment_tree(self):
        for comment in self.comments:
            children_list = list(filter(lambda child: child.parent_id == comment.id, self.comments))
            self.comments_children[str(comment.id)] = children_list

    def __render_comments(self, comments):
        if not comments:
            return ""

        res = '<ul id="comments-ul">'

        for comment in comments:
            res += '<li class="comment-item"  data-comment-id="%s">' % comment.id

            res += linebreaksbr(comment.text)

            res += ' <a href="javascript:void(0)" class="comment-reply" title="پاسخ">پاسخ</a>'
            res += '<div class="reply-form comment-form hidden"></div><br/>'

            children_list = self.comments_children[str(comment.id)]

            res += self.__render_comments(children_list)

            res += "</li>"

        res += '</ul>'

        return res

    @staticmethod
    def render_comment_item(comment):
        res = '<li class="comment-item"  data-comment-id="%s"><div class="comment-text" id="comment-text-%s">' % (
        comment.id, comment.id)

        if comment.parent_id:
            res += '<span class="comment-parent-right"></span><a class="comment-parent" href="#comment-text-%s">%s</a><br/> ' % \
                   (comment.parent_id, linebreaksbr(comment.parent.text[:20]))

        res += '<span class="comment-name">%s:</span> ' % str(comment.user or comment.user_name or "ناشناس")

        res += '<span class="comment-content">%s</span>' % linebreaksbr(comment.text)

        res += ' <a href="javascript:void(0)" class="comment-reply" title="پاسخ">پاسخ</a>'
        res += '<div class="reply-form comment-form hidden"></div><br/>'

        res += '</div><img src="/static/images/page/person.jpg" class="comment-image"/>'

        res += "</li>"
        return res

    def render_comments_inline(self):
        self.__create_comment_tree()
        root_comments = filter(lambda comment: not comment.parent_id, self.comments)

        res = '<ul id="comments-ul">'
        res += self.render_comments_items(root_comments)
        res += '</ul>'

        return res

    def render_comments_items(self, comments):
        if not comments:
            return ""

        res = ""
        for comment in comments:
            res += CommentHandler.render_comment_item(comment)

            children_list = self.comments_children[str(comment.id)]

            res += self.render_comments_items(children_list)

        return res


def _mark_as_root_path(comment):
    """
    Mark on comment as Being added to fill the tree.
    """
    setattr(comment, 'added_path', True)
    return comment


def fill_tree(comments):
    """
    Insert extra comments in the comments list, so that the root path of the first comment is always visible.
    Use this in comments' pagination to fill in the tree information.

    The inserted comments have an ``added_path`` attribute.
    """
    if not comments:
        return

    it = iter(comments)
    first = next(it)
    extra_path_items = map(_mark_as_root_path, first.root_path)
    return chain(extra_path_items, [first], it)


def annotate_tree_properties(comments):
    """
    iterate through nodes and adds some magic properties to each of them
    representing opening list of children and closing it
    """
    if not comments:
        return

    it = iter(comments)

    # get the first item, this will fail if no items !
    old = next(it)

    # first item starts a new thread
    old.open = True
    last = set()
    for c in it:
        # if this comment has a parent, store its last child for future reference
        if old.last_child_id:
            last.add(old.last_child_id)

        # this is the last child, mark it
        if c.pk in last:
            c.last = True

        # increase the depth
        if c.depth > old.depth:
            c.open = True

        else:  # c.depth <= old.depth
            # close some depths
            old.close = list(range(old.depth - c.depth))

            # new thread
            if old.root_id != c.root_id:
                # close even the top depth
                old.close.append(len(old.close))
                # and start a new thread
                c.open = True
                # empty the last set
                last = set()
        # iterate
        yield old
        old = c

    old.close = range(old.depth)
    yield old
