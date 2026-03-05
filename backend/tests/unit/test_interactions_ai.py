"""AI-generated unit tests for interactions module (curated)."""

from app.routers.interactions import filter_by_max_item_id
from app.models.interaction import InteractionLog
from datetime import datetime


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    return InteractionLog(
        kind="view",
        id=id,
        learner_id=learner_id,
        item_id=item_id,
        created_at=datetime(2025, 1, 1)
    )


# KEPT: covers the empty-list edge case
def test_filter_returns_empty_list_when_no_interactions() -> None:
    result = filter_by_max_item_id(interactions=[], max_item_id=5)
    assert len(result) == 0


# KEPT: tests negative max_item_id boundary
def test_filter_with_negative_max_item_id() -> None:
    interactions = [_make_log(1, 1, 2)]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=-1)
    assert len(result) == 0


# DISCARDED: duplicates existing test
# def test_filter_boundary_duplicate() -> None:
#     ...