#!/usr/bin/env python3

#
# author : Michael Brockus.  
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#

_MESONUI_THEME = '''\
/*
*/
QMainWindow, QDialog {
    border: 0px solid #263238;
    background-color: rgb(41, 41, 49);
    color: white;
}

/*
 theme for all labels
*/
QLabel#label_sourcedir,
QLabel#label_builddir {
    font: 13pt Monaco;
    color: white
}

QLabel {
    font: 11pt Monaco;
    color: white
}

/*
 theme for buttons
*/
QPushButton
{
    background-color: rgb(105, 105, 105);
    border-style: outset;
    border-width: 2px;
    border-radius: 10px;
    border-color: rgb(127, 127, 127);
    color: white;
    min-width: 2em;
    padding: 2px;
}

QPushButton:disabled {
    background-color: rgb(105, 105, 105);
    border-style: outset;
    border-width: 2px;
    border-radius: 10px;
    border-color: rgb(127, 127, 127);
    color: gray;
    min-width: 5em;
    padding: 2px;
}

QPushButton:pressed
{
    background-color: rgb(127, 127, 127);
    border-style: inset;
    color: rgb(36, 255, 6);
}


QPushButton#control_push_open_sourcedir,
QPushButton#control_push_clear_sourcedir
{
    background-color: rgb(105, 105, 105);
    border-style: outset;
    border-width: 2px;
    border-radius: 5px;
    border-color: rgb(127, 127, 127);
}

QPushButton:pressed#control_push_open_sourcedir,
QPushButton:pressed#control_push_clear_sourcedir
{
    background-color: rgb(127, 127, 127);
    border-style: inset;
    color: rgb(36, 255, 6);
}

/*
 theme for list view
*/
QScrollBar:vertical
{
    border: 2px solid grey;
    background: gray;
    width: 15px;
}

QScrollBar::handle:vertical {
    background: white;
    min-height: 20px;
}

QScrollBar::add-page:vertical, sub-page:vertical {
    background: none;
}

QListWidget {
    background-attachment: scroll;
    background-color: rgb(61, 64, 55);
    border-color: rgb(245, 251, 251);
    border-style: outset;
    border-width: 1px;
    border-radius: 10px;
    border-color: beige;
    padding: 6px;
    color: yellow;
    font: 13pt Monaco;
}

QPlainTextEdit#info {
    background-attachment: scroll;
    background-color: rgb(61, 64, 55);
    border-color: rgb(245, 251, 251);
    border-style: outset;
    border-width: 1px;
    border-radius: 10px;
    border-color: beige;
    color: white;
    padding: 6px;
    font: 11pt;
}

QPlainTextEdit {
    background-attachment: scroll;
    background-color: rgb(61, 64, 55);
    border-color: rgb(245, 251, 251);
    border-style: outset;
    border-width: 1px;
    border-radius: 10px;
    border-color: beige;
    padding: 6px;
    color: lightgreen;
    font: 13pt Monaco;
}

/*
 theme for all group box objects
*/
QGroupBox#group_core,
QGroupBox#group_base,
QGroupBox#group_path,
QGroupBox#group_test,
QGroupBox#group_backend,
QGroupBox#group_subcore {
    background-color: rgb(61, 64, 55);
    border: 1px solid rgb(255, 255, 255);
    color: white;
}

QGroupBox {
    border: 1px solid rgb(255, 255, 255);
    color: white;
}


/*
 theme for combo box items
*/
QComboBox:enabled {
    background-color: white;
    selection-color: lightgreen;
    color: green;
    border-width: 5px;
    border-radius: 5px;
    border: 2px solid gray;
}

QComboBox:disabled {
    background-color: lightgray;
    color: gray;
    border-width: 5px;
    border-radius: 5px;
    border: 2px solid gray;
}

QComboBox:editable {
    background: white;
}

QComboBox:on { /* shift the text when the popup opens */
    padding-top: 3px;
    padding-left: 4px;
}

/* shift the arrow when popup is open */
QComboBox::down-arrow:on {
    top: 1px;
    left: 1px;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 15px;

    border-left-width: 1px;
    border-left-color: darkgray;
    border-left-style: solid; /* just a single line */
    border-top-right-radius: 3px; /* same radius as the QComboBox */
    border-bottom-right-radius: 3px;
}


/*
 theme for all line edit entry objects
*/
QLineEdit#project_sourcedir,
QLineEdit#project_builddir
{
    background-color: rgb(255, 255, 255);
    color: black;
}

QLineEdit {
    background-color: white;
    color: green;
}

/*
 theme for all tab objects
*/
QTabWidget::pane { /* The tab widget frame */
    border-top: 2px solid #C2C7CB;
}

QTabWidget::tab-bar {
    left: 5px; /* move to the right by 5px */
}

/* Style the tab using the tab sub-control. Note that
    it reads QTabBar _not_ QTabWidget */
QTabBar::tab {
    background: rgb(123, 123, 123);
    border: 2px solid #C4C4C3;
    border-bottom-color: #C2C7CB; /* same as the pane color */
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    min-width: 15ex;
    color: white;
    padding: 2 17px;
}

QTabBar::tab:selected, QTabBar::tab:hover {
    background: rgb(148, 147, 147);
}

QTabBar::tab:selected {
    border-color: #9B9B9B;
    border-bottom-color: #C2C7CB; /* same as pane color */
}

QTabBar::tab:!selected {
    margin-top: 2px; /* make non-selected tabs look smaller */
}

/* make use of negative margins for overlapping tabs */
QTabBar::tab:selected {
    /* expand/overlap to the left and right by 4px */
    margin-left: -4px;
    margin-right: -4px;
}

QTabBar::tab:first:selected {
    margin-left: 0; /* the first selected tab has nothing to overlap with on the left */
}

QTabBar::tab:last:selected {
    margin-right: 0; /* the last selected tab has nothing to overlap with on the right */
}

QTabBar::tab:only-one {
    margin: 0; /* if there is only one tab, we don't want overlapping margins */
}

'''

class MesonUiTheme:
    @staticmethod
    def set_theme():
        return _MESONUI_THEME
