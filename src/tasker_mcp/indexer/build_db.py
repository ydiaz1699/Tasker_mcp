"""Build the SQLite + FTS5 search index (the DB step of the n8n-mcp pattern).

Merges two inputs:
  1. AUTHORITATIVE source (loader.py): code -> name -> kind (actions/events/states).
     This is what makes the index re-buildable instead of hand-maintained.
  2. ENRICHMENT from this repo's knowledge/*.py: descriptions, args (JSON),
     the 99 built-in variables and (optionally) automation patterns.

Output: a single SQLite file `tasker_index.db` with:
  - a base table `nodes(kind, code, name, category, description, args_json)`
  - an FTS5 virtual table `nodes_fts` (name, category, description) with BM25
    ranking, kept in sync via triggers.
  - a table `variables(name, category, description, dynamic)` + `variables_fts`.

Re-index:  python -m tasker_mcp.indexer.build_db --refresh
"""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

from tasker_mcp.indexer.loader import load_entries

DB_PATH = Path(__file__).parent / "data" / "tasker_index.db"

_SCHEMA = """
PRAGMA journal_mode = WAL;

DROP TABLE IF EXISTS nodes;
DROP TABLE IF EXISTS nodes_fts;
DROP TABLE IF EXISTS variables;
DROP TABLE IF EXISTS variables_fts;
DROP TABLE IF EXISTS meta;

CREATE TABLE nodes (
    id          INTEGER PRIMARY KEY,
    kind        TEXT NOT NULL,          -- action | event | state
    code        INTEGER NOT NULL,
    name        TEXT NOT NULL,
    category    TEXT,
    description TEXT,
    args_json   TEXT,                   -- JSON array of arg names
    deprecated  INTEGER NOT NULL DEFAULT 0,
    UNIQUE(kind, code)
);

CREATE VIRTUAL TABLE nodes_fts USING fts5(
    name, category, description,
    content='nodes', content_rowid='id',
    tokenize = 'unicode61'
);

CREATE TRIGGER nodes_ai AFTER INSERT ON nodes BEGIN
    INSERT INTO nodes_fts(rowid, name, category, description)
    VALUES (new.id, new.name, new.category, new.description);
END;
CREATE TRIGGER nodes_ad AFTER DELETE ON nodes BEGIN
    INSERT INTO nodes_fts(nodes_fts, rowid, name, category, description)
    VALUES ('delete', old.id, old.name, old.category, old.description);
END;

CREATE TABLE variables (
    id          INTEGER PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE,
    category    TEXT,
    description TEXT,
    dynamic     INTEGER NOT NULL DEFAULT 0
);

CREATE VIRTUAL TABLE variables_fts USING fts5(
    name, category, description,
    content='variables', content_rowid='id',
    tokenize = 'unicode61'
);

CREATE TRIGGER variables_ai AFTER INSERT ON variables BEGIN
    INSERT INTO variables_fts(rowid, name, category, description)
    VALUES (new.id, new.name, new.category, new.description);
END;

CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT);
"""


def _enrichment() -> tuple[dict, dict, dict, dict]:
    """Import this repo's in-memory knowledge for enrichment.

    Returns (actions_by_code, events_by_code, states_by_code, variables_by_name).
    """
    from tasker_mcp.knowledge import (
        BUILTIN_VARIABLES,
        PROFILE_EVENTS,
        PROFILE_STATES,
        TASKER_ACTIONS,
    )

    return (TASKER_ACTIONS, PROFILE_EVENTS, PROFILE_STATES, BUILTIN_VARIABLES)


def build_database(db_path: Path = DB_PATH, refresh: bool = False) -> dict:
    """Build the index. Returns a small stats dict.

    refresh=True re-downloads the authoritative source (and re-vendors it).
    """
    db_path.parent.mkdir(parents=True, exist_ok=True)

    entries = load_entries(refresh=refresh)
    actions, events, states, variables = _enrichment()

    enrich_by_kind = {"action": actions, "event": events, "state": states}

    if db_path.exists():
        db_path.unlink()
    con = sqlite3.connect(db_path)
    try:
        con.executescript(_SCHEMA)

        counts = {"action": 0, "event": 0, "state": 0, "deprecated": 0, "variable": 0}

        for e in entries:
            deprecated = 1 if e.kind == "action_deprecated" else 0
            kind = "action" if e.kind == "action_deprecated" else e.kind
            # Enrich from in-memory KB (same code) if present.
            enr = enrich_by_kind.get(kind, {}).get(e.code)
            category = getattr(enr, "category", None)
            description = getattr(enr, "description", None)
            args = getattr(enr, "args", None)
            args_json = json.dumps(args) if args else None

            con.execute(
                "INSERT OR REPLACE INTO nodes "
                "(kind, code, name, category, description, args_json, deprecated) "
                "VALUES (?,?,?,?,?,?,?)",
                (kind, e.code, e.name, category, description, args_json, deprecated),
            )
            counts["deprecated" if deprecated else kind] += 1

        # Variables come only from the KB (source has none).
        for var in variables.values():
            con.execute(
                "INSERT OR REPLACE INTO variables (name, category, description, dynamic) "
                "VALUES (?,?,?,?)",
                (var.name, var.category, var.description, 1 if var.dynamic else 0),
            )
            counts["variable"] += 1

        con.execute("INSERT INTO meta(key,value) VALUES('source_entries', ?)",
                    (str(len(entries)),))
        con.commit()
        return counts
    finally:
        con.close()


def main() -> None:
    ap = argparse.ArgumentParser(description="Build the Tasker SQLite+FTS5 index.")
    ap.add_argument("--refresh", action="store_true",
                    help="Re-download the authoritative source before building.")
    ap.add_argument("--db", type=Path, default=DB_PATH, help="Output DB path.")
    args = ap.parse_args()

    stats = build_database(db_path=args.db, refresh=args.refresh)
    total = sum(stats.values())
    print(f"Built {args.db} ({total} rows):")
    for k, v in stats.items():
        print(f"  {k:12} {v}")


if __name__ == "__main__":
    main()
