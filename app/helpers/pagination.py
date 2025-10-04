from typing import Any, List, Dict

def paginate(items: List[Any], page: int, page_size: int, total: int) -> Dict[str, Any]:
    return {
        "items": items,
        "page": page,
        "page_size": page_size,
        "total": total,
    }
