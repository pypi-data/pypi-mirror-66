#!/usr/bin/env python 
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------
# Copyright (c) 2013, NeXpy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING, distributed with this software.
#-----------------------------------------------------------------------------
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import six

import os
import sys
import tempfile
import pygments
from pygments.formatter import Formatter

from .pyqt import QtCore, QtGui, QtWidgets, getSaveFileName

from .utils import confirm_action
from .widgets import NXLabel, NXLineEdit


def hex2QColor(c):
    r=int(c[0:2],16)
    g=int(c[2:4],16)
    b=int(c[4:6],16)
    return QtGui.QColor(r,g,b)    


class QFormatter(Formatter):
    
    def __init__(self):

        Formatter.__init__(self, style='tango')
        self.data=[]
        
        self.styles={}
        for token, style in self.style:
            qtf = QtGui.QTextCharFormat()

            if style['color']:
                qtf.setForeground(hex2QColor(style['color'])) 
            if style['bgcolor']:
                qtf.setBackground(hex2QColor(style['bgcolor'])) 
            if style['bold']:
                qtf.setFontWeight(QtGui.QFont.Bold)
            if style['italic']:
                qtf.setFontItalic(True)
            if style['underline']:
                qtf.setFontUnderline(True)
            self.styles[str(token)] = qtf
    
    def format(self, tokensource, outfile):
        self.data=[]
        for ttype, value in tokensource:
            l=len(value)
            t=str(ttype)                
            self.data.extend([self.styles[t],]*l)


class Highlighter(QtGui.QSyntaxHighlighter):

    def __init__(self, parent):

        QtGui.QSyntaxHighlighter.__init__(self, parent)

        self.formatter=QFormatter()
        self.lexer = pygments.lexers.PythonLexer()
        
    def highlightBlock(self, text):
        """
        Takes a block and applies format to the document. 
        """
        
        text=six.text_type(self.document().toPlainText())+'\n'
        pygments.highlight(text, self.lexer, self.formatter)
        p = self.currentBlock().position()
        for i in range(len(six.text_type(text))):
            try:
                self.setFormat(i, 1, self.formatter.data[p+i])
            except IndexError:
                pass


class NXScrollBar(QtWidgets.QScrollBar):

    def sliderChange(self, change):
        if (self.signalsBlocked() and 
            change == QtWidgets.QAbstractSlider.SliderValueChange):
            self.blockSignals(False)
        


class NXPlainTextEdit(QtWidgets.QPlainTextEdit):

    def __init__(self, parent):
        super(NXPlainTextEdit, self).__init__()
        self.setFont(QtGui.QFont('Courier'))
        self.setMinimumWidth(700)
        self.setMinimumHeight(600)
        self.setWordWrapMode(QtGui.QTextOption.NoWrap)
        self.setTabStopWidth(4 * self.fontMetrics().width(' '))
        self.parent = parent
        self.blockCountChanged.connect(parent.update_line_numbers)
        self.scrollbar = NXScrollBar(self)
        self.setVerticalScrollBar(self.scrollbar)

    def __repr__(self):
        return 'NXPlainTextEdit()'

    @property
    def count(self):
        return self.blockCount()

       
class NXScriptWindow(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(NXScriptWindow, self).__init__(parent)
        layout = QtWidgets.QVBoxLayout()
        self.tabs = QtWidgets.QTabWidget(self)
        layout.addWidget(self.tabs)
        self.setLayout(layout)
        self.setWindowTitle('Script Editor')
        self.tabs.currentChanged.connect(self.update)

    def __repr__(self):
        return 'NXScriptWindow()'

    @property
    def editors(self):
        return [self.tabs.widget(idx) for idx in range(self.tabs.count())]

    @property
    def editor(self):
        return self.tabs.currentWidget()

    def update(self):
        for editor in self.editors:
            editor.adjustSize()
        if self.tabs.count() == 0:
            self.setVisible(False)

    def closeEvent(self, event):
        self.close()
        event.accept()
        
    def close(self):
        self.editor.close()
        if self.tabs.count() == 0:
            self.setVisible(False)


class NXScriptEditor(QtWidgets.QWidget):
    """Dialog to plot arbitrary NeXus data in one or two dimensions"""
 
    def __init__(self, file_name=None, parent=None):

        if parent is None:
            from .consoleapp import _mainwindow
            self.mainwindow = _mainwindow
        else:
            self.mainwindow = parent
        self.window = self.mainwindow.editors

        QtWidgets.QWidget.__init__(self, parent=self.window.tabs)
 
        self.file_name = file_name
        self.default_directory = self.mainwindow.script_dir

        layout = QtWidgets.QVBoxLayout()
        self.text_layout = QtWidgets.QHBoxLayout()
        self.number_box = QtWidgets.QPlainTextEdit('1')
        self.number_box.setFont(QtGui.QFont('Courier'))
        self.number_box.setStyleSheet(
            "QPlainTextEdit {background-color: "+
            self.palette().color(QtGui.QPalette.Window).name()+
            "; padding: 0; margin: 0; border: 0}")
        self.number_box.setFixedWidth(35)
        self.number_box.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.number_box.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.text_layout.addWidget(self.number_box)
        self.text_box = NXPlainTextEdit(self)
        self.text_box.scrollbar.valueChanged.connect(self.scroll_numbers)
        self.text_layout.addWidget(self.text_box)
        self.text_layout.setSpacing(0)
        layout.addLayout(self.text_layout)
        
        run_button = QtWidgets.QPushButton('Run Script')
        run_button.clicked.connect(self.run_script)
        run_button.setAutoDefault(False)
        self.argument_box = NXLineEdit()
        self.argument_box.setMinimumWidth(200)
        save_button = QtWidgets.QPushButton('Save')
        save_button.clicked.connect(self.save_script)
        save_as_button = QtWidgets.QPushButton('Save as...')
        save_as_button.clicked.connect(self.save_script_as)
        self.delete_button = QtWidgets.QPushButton('Delete')
        self.delete_button.clicked.connect(self.delete_script)
        close_button = QtWidgets.QPushButton('Close Tab')
        close_button.clicked.connect(self.close)
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(run_button)
        button_layout.addWidget(self.argument_box)
        button_layout.addStretch()
        button_layout.addWidget(save_button)
        button_layout.addWidget(save_as_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        if self.file_name:
            self.label = os.path.basename(self.file_name)
            with open(self.file_name, 'r') as f:
                text = f.read()
            self.text_box.setPlainText(text)
            self.window.tabs.addTab(self, self.label)
            self.update_line_numbers()
        else:
            self.label = 'Untitled %s' % (self.window.tabs.count()+1)
            self.delete_button.setVisible(False)
            self.window.tabs.addTab(self, self.label)
        self.index = self.window.tabs.indexOf(self)

        self.window.tabs.adjustSize()
        self.window.tabs.setCurrentWidget(self)

        self.hl = Highlighter(self.text_box.document())

        self.text_box.setFocus()
        self.number_box.setFocusPolicy(QtCore.Qt.NoFocus)

    def __repr__(self):
        return 'NXScriptEditor(%s)' % self.label
        
    def get_text(self):
        text = self.text_box.document().toPlainText().strip()
        return text.replace('\t', '    ')+'\n'

    def update_line_numbers(self):
        count = self.text_box.count
        if count >= 1000:
            self.number_box.setWidth(40)
        self.number_box.setPlainText('\n'.join([str(i).rjust(len(str(count)))
                                                for i in range(1,count+1)]))
        self.scroll_numbers()

    def scroll_numbers(self):
        self.number_box.verticalScrollBar().setValue(
                            self.text_box.verticalScrollBar().value())
        self.text_box.scrollbar.update()

    def run_script(self):
        text = self.get_text()
        if 'sys.argv' in text:
            file_name = tempfile.mkstemp('.py')[1]
            with open(file_name, 'w') as f:
                f.write(self.get_text())
            args = self.argument_box.text()
            self.mainwindow.console.execute('run -i %s %s' % (file_name, args))
            os.remove(file_name)
        else:
            self.mainwindow.console.execute(self.get_text())

    def save_script(self):
        if self.file_name:
            with open(self.file_name, 'w') as f:
                f.write(self.get_text())
        else:
            self.save_script_as()

    def save_script_as(self):
        file_filter = ';;'.join(("Python Files (*.py)", "Any Files (*.* *)"))
        file_name = getSaveFileName(self, "Choose a Filename", 
                                    self.default_directory, filter=file_filter)
        if file_name:
            with open(file_name, 'w') as f:
                f.write(self.get_text())
            self.file_name = file_name
            self.window.tabs.setTabText(self.index, 
                                        os.path.basename(self.file_name))
            self.mainwindow.add_script_action(self.file_name)
            self.delete_button.setVisible(True)

    def delete_script(self):
        if self.file_name:
            if confirm_action(
                    "Are you sure you want to delete '%s'?" % self.file_name,
                    "This cannot be reversed"):
                os.remove(self.file_name)
                self.mainwindow.remove_script_action(self.file_name)
                self.close()

    def close(self):
        self.window.tabs.removeTab(self.index)
        self.deleteLater()
        self.window.update()
