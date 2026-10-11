import base64
import csv
import os
from dataclasses import dataclass, field


@dataclass
class VFSNode:
    path: str
    is_dir: bool
    content: bytes = b""
    children: dict = field(default_factory=dict)


class VFS:
    def __init__(self):
        self.root = VFSNode(path="/", is_dir=True)
        self.cwd = "/"


    def load_from_csv(self, path: str) -> None:
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Файл VFS не найден: {path}")

        self.root = VFSNode(path="/", is_dir=True)
        self.cwd = "/"

        try:
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                self._validate_header(reader.fieldnames)
                for row in reader:
                    self._parse_row(row)
        except csv.Error as e:
            raise ValueError(f"Ошибка чтения CSV: {e}") from e

    @staticmethod
    def _validate_header(fieldnames) -> None:
        required = {"path", "type", "content"}
        if not fieldnames or not required.issubset(fieldnames):
            raise ValueError(
                "Неверный формат CSV: нужны колонки path, type, content"
            )

    def _parse_row(self, row: dict) -> None:
        path = (row.get("path") or "").strip()
        typ = (row.get("type") or "").strip().lower()
        raw = row.get("content") or ""

        if not path:
            return
        if typ not in ("dir", "file"):
            raise ValueError(f"Неверный тип '{typ}' в строке '{path}'")

        is_dir = typ == "dir"
        content = b"" if is_dir else self._decode_content(raw)
        self._insert(path, is_dir, content)

    @staticmethod
    def _decode_content(raw: str) -> bytes:
        if not raw:
            return b""
        try:
            return base64.b64decode(raw, validate=True)
        except Exception:
            return raw.encode("utf-8")

    def _insert(self, path: str, is_dir: bool, content: bytes) -> None:
        parts = [p for p in path.split("/") if p]
        node = self.root

        for part in parts[:-1]:
            child = node.children.get(part)
            if child is None:
                child = VFSNode(path=self._join(node.path, part), is_dir=True)
                node.children[part] = child
            if not child.is_dir:
                raise ValueError(f"Конфликт: '{child.path}' — файл, а не папка")
            node = child

        if parts:
            leaf_name = parts[-1]
            existing = node.children.get(leaf_name)
            if existing is not None and existing.is_dir != is_dir:
                raise ValueError(f"Конфликт типов на пути '{path}'")
            node.children[leaf_name] = VFSNode(
                path=self._join(node.path, leaf_name),
                is_dir=is_dir,
                content=content,
            )

    @staticmethod
    def _join(parent: str, name: str) -> str:
        return (parent.rstrip("/") + "/" + name) if parent != "/" else "/" + name


    def _resolve(self, path: str) -> VFSNode | None:
        if path is None or path == "":
            return None
        if path.startswith("/"):
            node = self.root
            parts = [p for p in path.split("/") if p]
        else:
            node = self._resolve(self.cwd) or self.root
            parts = [p for p in path.split("/") if p]

        for part in parts:
            if part == ".":
                continue
            if part == "..":
                node = self._go_up(node)
                continue
            if not node.is_dir or part not in node.children:
                return None
            node = node.children[part]
        return node

    def _go_up(self, node: VFSNode) -> VFSNode:
        if node is self.root or node.path == "/":
            return self.root
        parent_path = "/".join(node.path.rstrip("/").split("/")[:-1]) or "/"
        return self._resolve(parent_path) or self.root


    def exists(self, path: str) -> bool:
        return self._resolve(path) is not None

    def is_dir(self, path: str) -> bool:
        node = self._resolve(path)
        return node is not None and node.is_dir

    def is_file(self, path: str) -> bool:
        node = self._resolve(path)
        return node is not None and not node.is_dir

    def list_dir(self, path: str = "") -> list[str]:
        node = self._resolve(path or self.cwd)
        if node is None:
            raise FileNotFoundError(f"Директория не найдена: {path or self.cwd}")
        if not node.is_dir:
            raise NotADirectoryError(f"Не директория: {path or self.cwd}")
        return sorted(node.children.keys())

    def read_file(self, path: str) -> bytes:
        node = self._resolve(path)
        if node is None or node.is_dir:
            raise FileNotFoundError(f"Файл не найден: {path}")
        return node.content

    def change_dir(self, path: str) -> None:
        if not path or path == "/":
            self.cwd = "/"
            return
        node = self._resolve(path)
        if node is None:
            raise FileNotFoundError(f"Директория не найдена: {path}")
        if not node.is_dir:
            raise NotADirectoryError(f"Не директория: {path}")
        self.cwd = node.path