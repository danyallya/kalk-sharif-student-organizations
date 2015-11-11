from django.template.loader import render_to_string

__author__ = 'M.Y'


class LevelHandler:
    def __init__(self, levels, edit=False):
        self.levels = list(levels)
        self.levels_children = {"0": []}
        # self.header_nums = [0, 0, 0]
        #
        #     if level.depth == 1:
        #         self.header_nums[2] += 1
        #         self.header_nums[1] = 0
        #         self.header_nums[0] = 0
        #     elif level.depth == 2:
        #         self.header_nums[1] += 1
        #         self.header_nums[0] = 0
        #     elif level.depth == 3:
        #         self.header_nums[0] += 1
        #
        #     num_title = ""
        #     if level.depth < 4:
        #         num_title = '.'.join([str(x) for x in self.header_nums])

        self.edit = edit

    def __create_level_tree(self):
        for level in self.levels:
            children_list = list(filter(lambda child: child.parent_id == level.id, self.levels))
            self.levels_children[str(level.id)] = children_list

    def render_tree(self):
        self.__create_level_tree()
        root_levels = list(filter(lambda level: not level.parent_id, self.levels))

        if root_levels and not self.edit:
            document = root_levels[0].document
            if document.intro:
                root_levels = [document.intro_level] + root_levels

        return self.__render_levels_tree(root_levels)

    def render_new_level(self, level):
        children_content = self.__render_levels_tree([])
        return render_to_string('document/level_tree_item.html',
                                {'level': level, 'children_content': children_content,
                                 'edit': self.edit})

    def __render_levels_tree(self, levels):

        if not self.edit and not levels:
            return ""

        res = '<ul>'

        for level in levels:
            children_list = self.levels_children[str(level.id)]

            children_content = self.__render_levels_tree(children_list)

            res += render_to_string('document/level_tree_item.html',
                                    {'level': level, 'children_content': children_content, 'edit': self.edit})

        if self.edit:
            res += """
            <li class='add-level-item'>
                <span>
                طبقه جدید:
                </span>
                <input type='text' class='level-text'/>
                <button class='add-level'>
                ایجاد
                </button>
            </li>
            """

        res += '</ul>'

        return res

    def render_content(self):
        self.__create_level_tree()
        root_levels = list(filter(lambda level: not level.parent_id, self.levels))

        if root_levels:
            document = root_levels[0].document
            if document.intro:
                root_levels = [document.intro_level] + root_levels

        return "<ul id='main-doc-content'>" + self.__render_levels_content(root_levels) + "</ul>"

    def __render_levels_content(self, levels, parent=None):
        if not levels:
            return ""

        res = ""

        for level in levels:
            res += render_to_string('document/level_content_item.html', {'level': level, 'parent': parent})

            children_list = self.levels_children[str(level.id)]

            if level.depth == 2:
                res += "<ul>"

            res += self.__render_levels_content(children_list, level)

            if level.depth == 2:
                res += "</ul>"

            if level.depth == 2:
                res += "</li>"

        return res


from collections import defaultdict


def sorted_by_count(xs):
    counts = defaultdict(int)
    for x in xs:
        counts[x] += 1
    return [x[0] for x in sorted(counts.items(), reverse=True, key=lambda tup: tup[1])]


def get_package_cats():
    from document.models import PackageSubCat
    res = []
    for cat_id, cat in PackageSubCat.CATEGORIES:
        package_cat_item = PackageCatItem(cat_id, PackageSubCat.objects.filter(cat=cat_id))
        res.append(package_cat_item)
    return res


class PackageCatItem:
    def __init__(self, cat_id, sub_cats):
        self.sub_cats = sub_cats
        self.cat_id = cat_id
