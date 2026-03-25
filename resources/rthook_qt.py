import os
import sys

if getattr(sys, 'frozen', False):
    bundle_dir = sys._MEIPASS
    os.environ['QT_MAC_WANTS_LAYER'] = '1'
    plugin_path = os.path.join(bundle_dir, 'PyQt6', 'Qt6', 'plugins')
    if os.path.isdir(plugin_path):
        os.environ['QT_PLUGIN_PATH'] = plugin_path
