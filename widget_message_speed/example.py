#!/usr/bin/env python
# coding: utf-8

# Copyright (c) ian.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""

from ipywidgets import DOMWidget
from traitlets import Unicode, List, CInt
from ._frontend import module_name, module_version
from time import time


class ExampleWidget(DOMWidget):
    """TODO: Add docstring here
    """
    _model_name = Unicode('ExampleModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('ExampleView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    value = Unicode('Hello World').tag(sync=True)
    times = List(CInt()).tag(sync=True)
    py_ts_times = List(CInt()).tag(sync=True)
    ts_py_times = List(CInt()).tag(sync=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.on_msg(self.handle_msg)
    def measure_single_message(self):
        self.send({'event':'gogogo'})
    def handle_msg(self, widget, content, buffers):
        cur_time = time()
        if content['event'] == 'yikes':
            self.send({
                'event': 'yikes',
                'start': content['start'],
                'python': cur_time
                },[])
            self.ts_py_times = self.ts_py_times + [cur_time*1000 - content['start']]