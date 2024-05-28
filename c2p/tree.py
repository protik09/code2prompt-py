#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""
Generate a text representation of the project tree.

author: Protik Banerji <protik09@noreply.github.com>

"""

import os
import sys
from collections import deque
from pathlib import Path
from typing import TextIO

PIPE = "│"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "


class DirectoryTree:
    def __init__(
        self,
        root_directory: str,
        directories_only: bool = False,
        ignore: str = ".",
        output: TextIO = sys.stdout,
    ):
        self.output: TextIO = output
        self.tree_generator: TreeGenerator = TreeGenerator(
            root_directory, ignore, directories_only
        )

    def generate(self):
        tree_structure: deque = self.tree_generator.build_tree()
        if self.output != sys.stdout:
            tree_structure.appendleft("```")
            tree_structure.append("```")
            with open(self.output, mode="w", encoding="UTF-8") as output_file:
                for line in tree_structure:
                    print(line, file=output_file)
        else:
            for line in tree_structure:
                print(line, file=self.output)


class TreeGenerator:
    def __init__(
        self,
        root_directory: str,
        ignore: str,
        directories_only: bool = False,
    ):
        self.root_directory: Path = Path(root_directory).absolute()
        self.directories_only: bool = directories_only
        self.tree_structure: deque = deque()
        self.ignore: str = ignore

    def build_tree(self) -> deque:
        # Add root directory at the top of the structure
        self.tree_structure.append(f"{self.root_directory.name}{os.sep}")
        self._add_directory_contents(self.root_directory)
        return self.tree_structure

    def _add_directory_contents(self, directory: Path, prefix: str = ""):
        # Get all directories
        sorted_entries: list = self._get_sorted_entries(directory)
        # Filter out folders that start with "."
        entries: list = [
            entry for entry in sorted_entries if not entry.name.startswith(self.ignore)
        ]
        last_entry_index: int = len(entries) - 1
        for index, entry in enumerate(entries):
            if index == last_entry_index:
                connector = ELBOW
            else:
                connector = TEE
            if entry.is_dir():
                self._add_directory(entry, index, last_entry_index, prefix, connector)
            else:
                # Add files
                self.tree_structure.append(f"{prefix}{connector} {entry.name}")

    def _get_sorted_entries(self, directory: Path):
        entries = sorted(directory.iterdir(), key=lambda entry: str(entry).lower())
        if self.directories_only:
            entries = [entry for entry in entries if entry.is_dir()]
        return entries

    def _add_directory(
        self,
        directory: Path,
        index: int,
        last_entry_index: int,
        prefix: str,
        connector: str,
    ):
        self.tree_structure.append(f"{prefix}{connector} {directory.name}{os.sep}")
        extension = PIPE_PREFIX if index != last_entry_index else SPACE_PREFIX
        self._add_directory_contents(directory, prefix + extension)


if __name__ == "__main__":
    # Example usage:
    # generate_directory_tree('/path/to/directory', directories_only=False, output='output.txt')
    tree = DirectoryTree(".").generate()
