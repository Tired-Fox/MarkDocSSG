from __future__ import annotations


from os import path
from json import load

from .types import Markdown, Site, Build, Integration, Nav


class Config:
    def __init__(self, path_: str = ""):
        if len(path_) > 0 and path.isfile(path_):
            with open(path_, "r", encoding="UTF-8") as cfx:
                self._cfg_raw = load(cfx)
        else:
            for conf_file in ["moph.json", "mophidian.json", "conf.json", "config.json"]:
                if path.isfile(conf_file):
                    with open(conf_file, "r", encoding="UTF-8") as cfx:
                        self._cfg_raw = load(cfx)
                    break

        self.errors = []

        sections = [Markdown, Site, Build, Integration, Nav]

        self.markdown = Markdown()
        self.site = Site()
        self.build = Build()
        self.integration = Integration()
        self.nav = Nav()

        for section in sections:
            if section.key() in self._cfg_raw:
                setattr(self, section.key(), section(**self._cfg_raw[section.key()]))
                if getattr(self, section.key()).has_errors():
                    self.errors.append(getattr(self, section.key()).format_errors())

        self.print_errors()

    def print_errors(self):
        from log import FColor, Style, color, RESET

        if len(self.errors) > 0:
            print(
                color(
                    "[",
                    color("IMPORTANT", prefix=[FColor.MAGENTA]),
                    "]",
                    prefix=[Style.BOLD],
                    suffix=[RESET],
                ),
                "These errors were found while loading the config:",
            )

            for error in self.errors:
                print(error)
                print()
