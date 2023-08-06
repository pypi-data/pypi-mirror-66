import email

import pkg_resources
from lektor.pluginsystem import Plugin
from lektor.types.flow import FlowBlock
from more_itertools import split_before
from simplejson import JSONEncoder


def treeify(flat_list, level_attr='level'):
    if not flat_list:
        return []
    level = min(map(lambda l: l[level_attr], flat_list))
    chunks = split_before(flat_list, lambda r: r[level_attr] == level)
    for chunk in chunks:
        current = chunk.pop(0)
        yield {
            'name': current['caption'],
            'path': current['link'],
            'child': list(treeify(chunk, level_attr))
        }


def jsonify(structure):
    class JSONLeveledListEncoder(JSONEncoder):
        def default(self, obj):
            if isinstance(obj, FlowBlock):
                return {x: obj[x] for x in obj._data.keys()}
            else:
                raise TypeError('not a flowblock')
    return JSONLeveledListEncoder().encode(structure)


def get_description(mod):
    distribution = pkg_resources.get_distribution(mod)
    if distribution.has_metadata('PKG-INFO'):
        meta = distribution.get_metadata('PKG-INFO')
    elif distribution.has_metadata('METADATA'):
        meta = distribution.get_metadata('METADATA')
    else:
        return None
    return email.message_from_string(meta).get('Summary', None)


class TreeifyPlugin(Plugin):
    name = 'Treeify'
    description = get_description(__module__)

    def on_setup_env(self, **extra):
        self.env.jinja_env.filters['treeify'] = treeify
        self.env.jinja_env.filters['jsonify'] = jsonify
