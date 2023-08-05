
from PyQt5 import QtWidgets
import os.path

from meg_runtime.app import App
from meg_runtime.config import Config
from meg_runtime.ui.basepanel import BasePanel


class MainPanel(BasePanel):
    """Setup a list of cloned repos."""

    def __init__(self, **kwargs):
        """MainPanel constructor."""
        super().__init__(**kwargs)

    def get_is_closable(self):
        """Get if the panel is closable."""
        return False

    def on_load(self):
        """Load dynamic elements within the panel."""
        instance = self.get_widgets()
        self.download_button = instance.findChild(QtWidgets.QPushButton, 'downloadButton')
        # TODO: Attach handlers
        self.download_button.clicked.connect(App.open_clone_panel)
        self._tree_widget = instance.findChild(QtWidgets.QTreeWidget, 'treeWidget')
        self._tree_widget.itemDoubleClicked.connect(MainPanel._handle_double_click)
        # Load the repos
        # TODO: Get this from the GitManager
        repos = Config.get('path/repos')
        repos = [
            QtWidgets.QTreeWidgetItem([
                os.path.basename(repo['path']),
                repo['url'],
                repo['path'],
            ])
            for repo in repos if repo['path'] and repo['url']
        ]
        self._tree_widget.clear()
        self._tree_widget.addTopLevelItems(repos)

    @staticmethod
    def _handle_double_click(item):
        """Handle a double click."""
        # These columns were set in the load() method -- it would be nice
        # to find a way to get them by column name
        App.open_repo(item.text(1), item.text(2))
