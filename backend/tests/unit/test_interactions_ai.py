"""Unit tests for interaction edge cases and boundary values."""

from datetime import datetime, timezone

from app.models.interaction import InteractionLog, InteractionLogCreate, InteractionModel
from app.routers.interactions import filter_by_max_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    return InteractionLog(id=id, learner_id=learner_id, item_id=item_id, kind="attempt")


class TestFilterByMaxItemIdEdgeCases:
    """Edge case tests for filter_by_max_item_id."""

    def test_all_interactions_above_max_returns_empty(self) -> None:
        """When all item_ids exceed max_item_id, return empty list."""
        interactions = [_make_log(1, 1, 5), _make_log(2, 2, 10)]
        result = filter_by_max_item_id(interactions=interactions, max_item_id=3)
        assert result == []

    def test_multiple_interactions_at_same_boundary(self) -> None:
        """Multiple interactions with item_id equal to max_item_id are all included."""
        interactions = [
            _make_log(1, 1, 3),
            _make_log(2, 2, 3),
            _make_log(3, 3, 3),
        ]
        result = filter_by_max_item_id(interactions=interactions, max_item_id=3)
        assert len(result) == 3

    def test_unsorted_interactions_mixed_values(self) -> None:
        """Filtering works correctly regardless of input order."""
        interactions = [
            _make_log(1, 1, 10),
            _make_log(2, 2, 1),
            _make_log(3, 3, 5),
            _make_log(4, 4, 3),
        ]
        result = filter_by_max_item_id(interactions=interactions, max_item_id=4)
        assert len(result) == 2
        assert {i.id for i in result} == {2, 4}

    def test_zero_item_id_included_when_max_is_zero(self) -> None:
        """Zero item_id is included when max_item_id is zero."""
        interactions = [_make_log(1, 1, 0), _make_log(2, 2, 1)]
        result = filter_by_max_item_id(interactions=interactions, max_item_id=0)
        assert len(result) == 1
        assert result[0].item_id == 0

    def test_negative_item_id_values(self) -> None:
        """Negative item_id values are handled correctly."""
        interactions = [
            _make_log(1, 1, -5),
            _make_log(2, 2, 0),
            _make_log(3, 3, 5),
        ]
        result = filter_by_max_item_id(interactions=interactions, max_item_id=0)
        assert len(result) == 2
        assert {i.item_id for i in result} == {-5, 0}


class TestInteractionLogCreateValidation:
    """Boundary value tests for InteractionLogCreate model."""

    def test_empty_kind_string(self) -> None:
        """Empty string for kind field is accepted by model."""
        log = InteractionLogCreate(learner_id=1, item_id=1, kind="")
        assert log.kind == ""

    def test_very_long_kind_string(self) -> None:
        """Very long kind string is accepted by model."""
        long_kind = "a" * 10000
        log = InteractionLogCreate(learner_id=1, item_id=1, kind=long_kind)
        assert log.kind == long_kind

    def test_negative_learner_id(self) -> None:
        """Negative learner_id is accepted by model (FK constraint at DB level)."""
        log = InteractionLogCreate(learner_id=-1, item_id=1, kind="attempt")
        assert log.learner_id == -1


class TestInteractionModelResponse:
    """Tests for InteractionModel response schema."""

    def test_model_with_very_large_ids(self) -> None:
        """InteractionModel handles very large integer IDs."""
        large_id = 2**63 - 1
        model = InteractionModel(
            id=large_id,
            learner_id=large_id,
            item_id=large_id,
            kind="attempt",
            created_at=datetime.now(timezone.utc),
        )
        assert model.id == large_id


class TestInteractionLogModelEdgeCases:
    """Edge case tests for InteractionLog model."""

    def test_model_with_unicode_kind(self) -> None:
        """InteractionLog accepts unicode characters in kind field."""
        log = InteractionLog(learner_id=1, item_id=1, kind="尝试_テスト_시도")
        assert log.kind == "尝试_テスト_시도"
