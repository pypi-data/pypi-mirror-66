#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .thread import Thread

class AFThread(Thread):
    def __init__(self, parent):
        super(AFThread, self).__init__(parent)
        self.sig.connect(parent.cbMDThread)

    def run(self):
        html_text = self.parent().mdrenderer._render_md(self.parent().post["body"])
        self.sig.emit(html_text)
