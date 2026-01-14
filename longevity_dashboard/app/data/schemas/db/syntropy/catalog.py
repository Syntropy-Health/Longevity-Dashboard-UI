"""Catalog data models."""

from typing import List

from typing_extensions import TypedDict


class CatalogItem(TypedDict, total=False):
    """Type definition for catalog items."""

    id: int
    name: str
    category: str
    price: float
    rating: float
    description: str
    image: str
    in_stock: bool
    is_favorite: bool
    tags: List[str]


class CategoryItem(TypedDict):
    """Type definition for category items."""

    id: str
    name: str
    icon: str
