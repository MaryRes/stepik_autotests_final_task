#!/usr/bin/env python3
"""
Скрипт для генерации структуры проекта в формате Markdown
"""

import os
import sys
from pathlib import Path


def generate_project_structure(start_path: str = ".", ignore_dirs: list = None):
    if ignore_dirs is None:
        ignore_dirs = ['venv', '__pycache__', '.pytest_cache', '.git', '.idea']

    structure = []
    base_path = Path(start_path)

    for root, dirs, files in os.walk(base_path):
        # Получаем относительный путь
        rel_path = Path(root).relative_to(base_path)

        # Игнорируем ненужные директории
        dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.startswith('.')]
        files = [f for f in files if f not in ignore_dirs and not f.startswith('.')]

        level = len(rel_path.parts)
        indent = '  ' * level

        if level == 0:
            structure.append(f"./")
        else:
            structure.append(f"{indent}└── {rel_path.name}/")

        subindent = '  ' * (level + 1)
        for file in files:
            if file not in ignore_dirs and not file.startswith('.'):
                structure.append(f"{subindent}├── {file}")

    return structure


if __name__ == "__main__":
    # Всегда работаем от корня проекта
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    structure = generate_project_structure()
    print("Структура проекта:\n")
    for line in structure:
        print(line)