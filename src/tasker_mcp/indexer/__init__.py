"""Tasker indexer: build a SQLite + FTS5 search index from authoritative sources.

Pattern (adapted from czlonkowski/n8n-mcp):
    SOURCE  ->  LOADER  ->  PARSER  ->  DB (SQLite + FTS5)  ->  MCP search tools

- SOURCE (authoritative): Taskomater/Tasker-XML-Info `Tasker_XML_Codes.md`
  gives code -> name -> category for Actions (373), Events (82), States (50).
- ENRICHMENT: this repo's `knowledge/*.py` adds descriptions, args, the 99
  built-in variables and the automation patterns that the source does not carry.
- DB: `build_db.py` merges both into `tasker_index.db` with FTS5 (BM25) search.

Re-index with:  python -m tasker_mcp.indexer.build_db --refresh
"""

from tasker_mcp.indexer.build_db import DB_PATH, build_database

__all__ = ["build_database", "DB_PATH"]
