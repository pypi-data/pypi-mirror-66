"""
A plugin to generate a local_scheme version with the node and dirty tag.

If the source tree is at a tag, it returns e.g. "0.1". if it is three commits
ahead a tag, it returns "0.1+3". if it is three commits ahead a tag and has
local modifications, it returns "0.1+3.dirty"
"""

__version__ = "0.0.0.post0"


def node_and_dirty_tag(version):
    return (
        version.format_with("")
        if version.tag and not version.distance
        else version.format_choice("+{node}", "+{node}.dirty")
    )
