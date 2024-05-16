import os
import subprocess
from shutil import copyfileobj
from urllib.request import urlopen

import sublime

from LSP.plugin import AbstractPlugin

SESSION_NAME = 'autohotkey2'
INSTALL_SCRIPT_URL = 'https://raw.githubusercontent.com/thqby/vscode-autohotkey2-lsp/main/tools/install.js'
INSTALL_SCRIPT_FILENAME = 'install.js'


class AutoHotkey2(AbstractPlugin):
    @classmethod
    def name(cls):
        return SESSION_NAME

    @classmethod
    def basedir(cls) -> str:
        return os.path.join(cls.storage_path(), __package__)

    @classmethod
    def needs_update_or_installation(cls) -> bool:
        filepath = os.path.join(cls.basedir(), INSTALL_SCRIPT_FILENAME)
        return not (os.path.exists(filepath) and os.path.isfile(filepath))

    @classmethod
    def install_or_update(cls) -> None:
        dst_dir = cls.basedir()
        os.makedirs(dst_dir, exist_ok=True)

        filepath = os.path.join(dst_dir, INSTALL_SCRIPT_FILENAME)
        with urlopen(INSTALL_SCRIPT_URL) as response, open(filepath, 'wb') as fp:
            copyfileobj(response, fp)

        subprocess.check_call(['node', filepath], shell=True, cwd=dst_dir)
