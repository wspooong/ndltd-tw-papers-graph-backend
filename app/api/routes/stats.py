from typing import Union, List, Dict
from fastapi import APIRouter, Query

from app.services import os_search

router = APIRouter()

@router.get("/top_field")
def get_top_field_count(
    year: int = Query(109),
) -> Dict[str, List[Dict[str, Union[str, int]]]]:
    return os_search.get_top_field_count(year=year)

@router.get("/institution_department")
def get_institution_department(
    year: int = Query(109),
) -> List[Dict[str, Union[str, int]]]:
    return os_search.get_institution_department_stats(year=year)
