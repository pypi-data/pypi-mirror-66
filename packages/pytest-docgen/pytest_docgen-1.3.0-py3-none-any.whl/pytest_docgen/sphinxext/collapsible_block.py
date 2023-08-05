""" Display code blocks in collapsible sections when outputting
to HTML.

This directive takes a heading to use for the collapsible code block::

    .. collapsible-code-block:: python
        :heading: Some Code

        from __future__ import print_function

        print("Hello, Bokeh!")

This directive is identical to the standard ``code-block`` directive
that Sphinx supplies, with the addition of one new option:

heading : string
    A heading to put for the collapsible block. Clicking the heading
    expands or collapses the block

Examples
--------

The inline example code above produces the following output:

.. collapsible-code-block:: python
    :heading: Some Code

    from __future__ import print_function

    print("Hello, Bokeh!")

"""

# -----------------------------------------------------------------------------
# Boilerplate
# -----------------------------------------------------------------------------
from __future__ import absolute_import, division, print_function, unicode_literals

import logging

import os
from docutils.parsers.rst import Directive
from docutils.parsers.rst.directives import unchanged
from sphinx.util.fileutil import copy_asset


log = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

# Standard library imports
from os.path import basename

# External imports
from docutils import nodes
from jinja2 import Environment, PackageLoader

_env = Environment(loader=PackageLoader("pytest_docgen.sphinxext", "_templates"))

CCB_PROLOGUE = _env.get_template("collapsible_block_prologue.html")
CCB_EPILOGUE = _env.get_template("collapsible_block_epilogue.html")

# -----------------------------------------------------------------------------
# Globals and constants
# -----------------------------------------------------------------------------

__all__ = (
    "collapsible_block",
    "CollapsibleBlock",
    "html_depart_collapsible_block",
    "html_visit_collapsible_block",
    "setup",
)

_EXT_STATIC = os.path.join(os.path.dirname(__file__), "_static")
_JS_ASSETS = [os.path.join(_EXT_STATIC, "js", "collapsible_block.js")]
_CSS_ASSETS = [os.path.join(_EXT_STATIC, "css", "collapsible_block.css")]


# -----------------------------------------------------------------------------
# General API
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Dev API
# -----------------------------------------------------------------------------


class collapsible_block(nodes.General, nodes.Element):
    pass


class CollapsibleBlock(Directive):
    option_spec = {"heading": unchanged}
    has_content = True

    def run(self):
        self.assert_has_content()
        env = self.state.document.settings.env

        rst_source = self.state_machine.node.document["source"]
        rst_filename = basename(rst_source)

        target_id = "%s.ccb-%d" % (rst_filename, env.new_serialno())
        target_id = target_id.replace(".", "-")
        target_node = nodes.target("", "", ids=[target_id])

        node = collapsible_block("\n".join(self.content))

        self.state.nested_parse(self.content, self.content_offset, node)

        node["heading"] = self.options.pop("heading", "Collapse")
        node["target_id"] = target_id

        return [target_node, node]


def html_visit_collapsible_block(self, node):
    self.body.append(CCB_PROLOGUE.render(id=node["target_id"], heading=node["heading"]))


def html_depart_collapsible_block(self, node):
    self.body.append(CCB_EPILOGUE.render())


def copy_asset_files(app, exc):
    asset_files = _JS_ASSETS + _CSS_ASSETS
    if exc is None:  # build succeeded
        for path in asset_files:
            copy_asset(path, os.path.join(app.outdir, "_static"))


def setup(app):
    app.add_node(
        collapsible_block, html=(html_visit_collapsible_block, html_depart_collapsible_block)
    )
    app.add_directive("collapsible-block", CollapsibleBlock)
    app.connect("build-finished", copy_asset_files)

    app.add_javascript("collapsible_block.js")
    app.add_stylesheet("collapsible_block.css")

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
        "version": "1.3.0",
    }
