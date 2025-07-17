import os
import sys

class Challenge:
    """Represents a single CTF challenge."""

    def __init__(self, id, ch_number, name, folder, script, flag):
        self.id = id  # Unique identifier
        self.ch_number = ch_number  # Challenge number for display
        self.name = name  # Human-readable name
        self.complete = False  # Default: not completed
        self.flag = flag  # Real flag (plaintext in admin version)

        # Detect PyInstaller frozen mode
        if getattr(sys, 'frozen', False):
            base_dir = sys._MEIPASS  # PyInstaller extracts files here
        else:
            base_dir = os.path.dirname(
                os.path.abspath(__file__).replace(
                    "/web_version_admin/utils", "/challenges"
                )
            )

        self.folder = os.path.normpath(os.path.join(base_dir, folder))
        self.script = os.path.normpath(os.path.join(self.folder, script))

    def setComplete(self):
        """Mark this challenge as completed."""
        self.complete = True

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getFolder(self):
        return self.folder

    def getScript(self):
        return self.script

    def getFlag(self):
        return self.flag

    def __repr__(self):
        return (
            f"#{self.ch_number} {self.name} | ID={self.id} | "
            f"Folder={self.folder} | Script={self.script} | "
            f"Flag={self.flag}"
        )
