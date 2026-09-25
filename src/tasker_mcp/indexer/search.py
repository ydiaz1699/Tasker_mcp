"""Search over the SQLite + FTS5 index (BM25 ranking).

Public helpers used by the MCP tools. If the index DB does not exist, callers
should fall back to the in-memory knowledge base (server.py does this), so the
server keeps working even before the first build.

FTS5 query hardening: user text is turned into a safe prefix query so arbitrary
input can't break the FTS5 syntax (quotes each token, adds a * for prefix match).
"""

from __future__ import annotations

import json
import re
import sqlite3
from pathlib import Path
from typing import Optional

from tasker_mcp.indexer.build_db import DB_PATH

_TOKEN_RE = re.compile(r"[A-Za-z0-9%]+")


def index_exists(db_path: Path = DB_PATH) -> bool:
    return db_path.exists()


def _connect(db_path: Path) -> sqlite3.Connection:
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    return con


def _fts_query(text: str) -> str:
    """Build a safe FTS5 MATCH string: quoted tokens with prefix matching."""
    tokens = _TOKEN_RE.findall(text or "")
    if not tokens:
        return ""
    # "wifi"* OR "net"* -> any token may match (higher recall); BM25 ranks the
    # rows matching more/rarer tokens higher, so multi-word queries still work.
    return " OR ".join(f'"{t}"*' for t in tokens)


def search_nodes(
    query: str,
    kind: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 25,
    db_path: Path = DB_PATH,
) -> list[dict]:
    """Full-text search over actions/events/states, ranked by BM25.

    Args:
        query: free text (e.g. 'wifi', 'battery low', 'send sms').
        kind: optional filter 'action' | 'event' | 'state'.
        category: optional exact category filter (e.g. 'Net', 'Alert').
        limit: max results.
    """
    match = _fts_query(query)
    con = _connect(db_path)
    try:
        params: list = []
        where = []
        if match:
            sql = (
                "SELECT n.kind, n.code, n.name, n.category, n.description, "
                "n.args_json, n.deprecated, bm25(nodes_fts) AS rank "
                "FROM nodes_fts JOIN nodes n ON n.id = nodes_fts.rowid "
                "WHERE nodes_fts MATCH ? "
            )
            params.append(match)
        else:
            # Empty query -> list by filters, ordered by name.
            sql = (
                "SELECT n.kind, n.code, n.name, n.category, n.description, "
                "n.args_json, n.deprecated, 0 AS rank FROM nodes n WHERE 1=1 "
            )
        if kind:
            where.append("n.kind = ?")
            params.append(kind)
        if category:
            where.append("n.category = ?")
            params.append(category)
        if where:
            sql += "AND " + " AND ".join(where) + " "
        sql += "ORDER BY rank LIMIT ?" if match else "ORDER BY n.name LIMIT ?"
        params.append(limit)

        rows = con.execute(sql, params).fetchall()
        return [_row_to_node(r) for r in rows]
    finally:
        con.close()


def get_node(code: int, kind: Optional[str] = None, db_path: Path = DB_PATH) -> Optional[dict]:
    """Fetch a single node by code (optionally constrained to a kind)."""
    con = _connect(db_path)
    try:
        if kind:
            row = con.execute(
                "SELECT kind, code, name, category, description, args_json, deprecated "
                "FROM nodes WHERE code = ? AND kind = ?",
                (code, kind),
            ).fetchone()
        else:
            row = con.execute(
                "SELECT kind, code, name, category, description, args_json, deprecated "
                "FROM nodes WHERE code = ? ORDER BY kind LIMIT 1",
                (code,),
            ).fetchone()
        return _row_to_node(row) if row else None
    finally:
        con.close()


def search_variables(query: str, category: Optional[str] = None,
                     limit: int = 25, db_path: Path = DB_PATH) -> list[dict]:
    """Full-text search over built-in variables."""
    match = _fts_query(query)
    con = _connect(db_path)
    try:
        params: list = []
        if match:
            sql = (
                "SELECT v.name, v.category, v.description, v.dynamic, "
                "bm25(variables_fts) AS rank "
                "FROM variables_fts JOIN variables v ON v.id = variables_fts.rowid "
                "WHERE variables_fts MATCH ? "
            )
            params.append(match)
        else:
            sql = ("SELECT name, category, description, dynamic, 0 AS rank "
                   "FROM variables WHERE 1=1 ")
        if category:
            sql += "AND v.category = ? " if match else "AND category = ? "
            params.append(category)
        sql += "ORDER BY rank LIMIT ?" if match else "ORDER BY name LIMIT ?"
        params.append(limit)
        rows = con.execute(sql, params).fetchall()
        return [
            {
                "name": r["name"],
                "category": r["category"],
                "description": r["description"],
                "dynamic": bool(r["dynamic"]),
            }
            for r in rows
        ]
    finally:
        con.close()


def _row_to_node(r: sqlite3.Row) -> dict:
    return {
        "kind": r["kind"],
        "code": r["code"],
        "name": r["name"],
        "category": r["category"],
        "description": r["description"],
        "args": json.loads(r["args_json"]) if r["args_json"] else [],
        "deprecated": bool(r["deprecated"]),
    }
