"""MEG UI Manager
"""

import pkg_resources
from PyQt5 import QtWidgets, QtGui, uic
from meg_runtime.logger import Logger
from meg_runtime.app import App


class UIManager(QtWidgets.QMainWindow):
    """Main UI manager for the MEG system."""

    UI_FILE = 'mainwindow.ui'

    # The window class widgets
    __widgets = None

    def __init__(self, **kwargs):
        """UI manager constructor."""
        # Load window resource if needed
        if UIManager.__widgets is None:
            # Load the resource setup from the package
            UIManager.__widgets = uic.loadUiType(pkg_resources.resource_filename(__name__, UIManager.UI_FILE))
        # Initialize the super class
        super().__init__(**kwargs)
        # Setup window resource
        UIManager.__widgets[0]().setupUi(self)
        # Set the window panel stack
        self._panels = []
        self._current_panel = None
        # Set handler for closing a panel
        self._panel = self.findChild(QtWidgets.QTabWidget, 'panelwidget')
        self._panel.tabCloseRequested.connect(self.remove_view_by_index)
        self._panel.currentChanged.connect(self._show_view_by_index)
        # Get status widget
        self._statusbar = self.findChild(QtWidgets.QStatusBar, 'statusbar')
        # Set handlers for main buttons
        # TODO: Add more handlers for these
        self._action_clone = self.findChild(QtWidgets.QAction, 'action_Clone')
        self._action_clone.triggered.connect(App.open_clone_panel)
        self._action_open = self.findChild(QtWidgets.QAction, 'action_Open')
        self._action_open.triggered.connect(App.open_repo_panel)
        self._action_quit = self.findChild(QtWidgets.QAction, 'action_Quit')
        self._action_quit.triggered.connect(App.quit)
        self._action_about = self.findChild(QtWidgets.QAction, 'action_About')
        self._action_about.triggered.connect(App.open_about)
        self._action_preferences = self.findChild(QtWidgets.QAction, 'action_Preferences')
        self._action_preferences.triggered.connect(App.open_prefs_panel)
        self._action_manage_plugins = self.findChild(QtWidgets.QAction, 'action_Manage_Plugins')
        self._action_manage_plugins.triggered.connect(App.open_plugins_panel)
        # Set the default title
        self.set_title()
        # Set the icon
        icon_path = App.get_icon()
        if icon_path is not None:
            self.setWindowIcon(QtGui.QIcon(icon_path))

    def set_title(self, panel=None):
        """Update the window title from the current panel"""
        # Set the new window title, if provided by the panel
        if panel is not None and panel.get_title():
            title = panel.get_title()
            self.setWindowTitle(f'{App.get_name()} - {title}')
            container = self.get_panel_container()
            if container is not None:
                index = container.indexOf(panel.get_widgets())
                if index >= 0:
                    container.setTabText(index, title)
                    container.setTabIcon(index, panel.get_icon())
        else:
            self.setWindowTitle(f'{App.get_name()}')

    def set_status(self, panel=None, timeout=0):
        """Update the window status from the current panel"""
        self.set_status_text('' if panel is None else panel.get_status(), timeout)

    def set_status_text(self, message, timeout=0):
        """Update the window status from the current panel"""
        if self._statusbar is not None:
            self._statusbar.showMessage('' if message is None else message, timeout)

    def get_panel_container(self):
        """Get the panel container widget"""
        return self._panel

    def get_panels(self):
        """Get all the panels in the window panel stack"""
        if not isinstance(self._panels, list):
            self._panels = []
        return self._panels

    def get_panel(self, name):
        """Get a panel in the window panel stack by name"""
        # Check panels by name
        for panel in self.get_panels():
            if panel.get_name() == name:
                # Return the panel
                return panel
        # Panel not found
        return None

    def get_panel_by_index(self, index):
        """Get a panel in the window panel stack by index"""
        # Get panel container
        container = self.get_panel_container()
        if container is not None:
            # Get the widgets of the panel
            widgets = container.widget(index)
            if widgets is not None:
                # Check the panels for matching widgets
                for panel in self.get_panels():
                    if panel.get_widgets() == widgets:
                        # Found the panel
                        return panel
        # Panel not found
        return None

    def get_current_panel(self):
        """Get the current panel in the window stack"""
        return self._current_panel

    def push_view(self, panel):
        """Push a panel onto the stack being viewed."""
        Logger.debug(f'MEG UI: Adding panel "{panel.get_name()}"')
        # Hide the current panel
        current_panel = self.get_current_panel()
        if current_panel is not None:
            current_panel.on_hide()
        # Show the current panel
        panel.on_show()
        # Update the title for the panel
        self.set_title(panel)
        # Update the status for the panel
        self.set_status(panel)
        # Get the window central widget
        container = self.get_panel_container()
        if container is not None:
            # Add the panel to the view stack
            widgets = panel.get_widgets()
            widgets.setParent(container)
            title = panel.get_title()
            index = container.addTab(widgets, 'Home' if not title else title)
            # Remove the close button if not closable
            tabbar = container.tabBar()
            if not panel.get_is_closable():
                tabbar.tabButton(index, QtWidgets.QTabBar.RightSide).deleteLater()
                tabbar.setTabButton(index, QtWidgets.QTabBar.RightSide, None)
            # Add the panel icon
            tabbar.setTabIcon(index, panel.get_icon())
            # Set the panel to the view
            container.setCurrentIndex(index)
            # Add the panel to the panel stack
            self.get_panels().append(panel)

    def set_view(self, panel):
        """Set the panel to be viewed in the stack or push the panel onto the stack being viewed."""
        # Get the window central widget
        container = self.get_panel_container()
        if container is not None:
            # Get the index of the panel
            index = container.indexOf(panel.get_widgets())
            if index >= 0:
                # Set the new panel
                container.setCurrentIndex(index)
                # Do not continue since the panel was found do not push
                Logger.debug(f'MEG UI: Setting panel "{panel.get_name()}"')
                return
        # Push the panel instead because it was not found
        self.push_view(panel)

    def remove_view(self, panel):
        """Remove a panel from the stack being viewed."""
        # Check if the panel is closable
        if panel is not None and panel.get_is_closable():
            Logger.debug(f'MEG UI: Removing panel "{panel.get_name()}"')
            # Close the panel
            panel.on_hide()
            panel.on_close()
            # Remove the panel from the list
            panels = self.get_panels()
            if panel in panels:
                panels.remove(panel)
            if self._current_panel == panel:
                self._current_panel = None
            # Get the window central widget
            container = self.get_panel_container()
            if container:
                # Get the index of this panel
                index = container.indexOf(panel.get_widgets())
                if index >= 0:
                    # Remove the panel from the view stack
                    container.removeTab(index)
                    panel.get_widgets().setParent(None)

    def remove_view_by_index(self, index):
        """Remove a panel from the stack being viewed."""
        # Get the panel by index
        Logger.debug(f'MEG UI: Removing panel by index ({index})')
        panel = self.get_panel_by_index(index)
        if panel is not None and panel.get_is_closable():
            # Remove the panel
            self.remove_view(panel)

    def _show_view_by_index(self, index):
        """Show the panel on click"""
        # Get the panel by index
        panel = self.get_panel_by_index(index)
        # Get the current panel
        current_panel = self.get_current_panel()
        # Check if the panel is not the current panel
        if current_panel != panel:
            # Hide the current panel
            if current_panel is not None:
                current_panel.on_hide()
            # Set the current panel
            self._current_panel = panel
            # Update the title
            self.set_title(panel)
            # Update the status
            self.set_status(panel)
            # Show the new panel
            if panel is not None:
                panel.on_show()
