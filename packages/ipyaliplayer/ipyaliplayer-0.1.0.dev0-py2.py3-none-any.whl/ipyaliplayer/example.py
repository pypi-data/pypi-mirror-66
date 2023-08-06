#!/usr/bin/env python
# coding: utf-8

# Copyright (c) wangsijie.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""

from ipywidgets import DOMWidget
from traitlets import Unicode, Int
from ._frontend import module_name, module_version


class Player(DOMWidget):
    """TODO: Add docstring here
    """
    _model_name = Unicode('PlayerModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('PlayerView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    _width = Int(480).tag(sync=True)
    _height = Int(270).tag(sync=True)
    value = Unicode('').tag(sync=True)
    def __init__(self, vid, width=480, height=270):
        DOMWidget.__init__(self)
        self._width = width
        self._height = height
        self.value = vid
