from typing import Dict, Any, List

def apply_filters_sql(base_sql: str, filters: Dict[str, Any]) -> str:
    clauses: List[str] = []
    if 'q' in filters and filters['q']:
        clauses.append("(name LIKE :q OR code LIKE :q)")
    if 'status' in filters and filters['status']:
        clauses.append("status = :status")
    if clauses:
        return base_sql + " WHERE " + " AND ".join(clauses)
    return base_sql
