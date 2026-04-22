import pytest
from engagement_engine import EngagementEngine


def test_init_defaults():
    engine = EngagementEngine("user123")
    assert engine.user_handle == "user123"
    assert engine.score == 0.0
    assert engine.verified is False


def test_init_verified_true():
    engine = EngagementEngine("creator", verified=True)
    assert engine.user_handle == "creator"
    assert engine.score == 0.0
    assert engine.verified is True


def test_process_like_unverified():
    engine = EngagementEngine("user1")
    result = engine.process_interaction("like", 3)

    assert result is True
    assert engine.score == 3


def test_process_comment_unverified():
    engine = EngagementEngine("user1")
    result = engine.process_interaction("comment", 2)

    assert result is True
    assert engine.score == 10


def test_process_share_unverified():
    engine = EngagementEngine("user1")
    result = engine.process_interaction("share", 4)

    assert result is True
    assert engine.score == 40


def test_process_like_verified():
    engine = EngagementEngine("verified_user", verified=True)
    result = engine.process_interaction("like", 2)

    assert result is True
    assert engine.score == 3.0


def test_process_comment_verified():
    engine = EngagementEngine("verified_user", verified=True)
    result = engine.process_interaction("comment", 2)

    assert result is True
    assert engine.score == 15.0


def test_process_share_verified():
    engine = EngagementEngine("verified_user", verified=True)
    result = engine.process_interaction("share", 2)

    assert result is True
    assert engine.score == 30.0


def test_process_invalid_interaction_type():
    engine = EngagementEngine("user1")
    result = engine.process_interaction("follow", 5)

    assert result is False
    assert engine.score == 0.0


def test_process_negative_count_raises_error():
    engine = EngagementEngine("user1")
    with pytest.raises(ValueError, match="Negative count"):
        engine.process_interaction("like", -1)


def test_process_default_count_is_one():
    engine = EngagementEngine("user1")
    result = engine.process_interaction("comment")

    assert result is True
    assert engine.score == 5


def test_get_tier_newbie():
    engine = EngagementEngine("user1")
    engine.score = 99
    assert engine.get_tier() == "Newbie"


def test_get_tier_influencer_at_100():
    engine = EngagementEngine("user1")
    engine.score = 100
    assert engine.get_tier() == "Influencer"


def test_get_tier_influencer_middle():
    engine = EngagementEngine("user1")
    engine.score = 500
    assert engine.get_tier() == "Influencer"


def test_get_tier_influencer_at_1000():
    engine = EngagementEngine("user1")
    engine.score = 1000
    assert engine.get_tier() == "Influencer"


def test_get_tier_icon():
    engine = EngagementEngine("user1")
    engine.score = 1001
    assert engine.get_tier() == "Icon"


def test_apply_penalty_one_report():
    engine = EngagementEngine("user1")
    engine.score = 100
    engine.apply_penalty(1)

    assert engine.score == 80


def test_apply_penalty_two_reports():
    engine = EngagementEngine("user1")
    engine.score = 200
    engine.apply_penalty(2)

    assert engine.score == 120


def test_apply_penalty_five_reports_reduces_to_zero():
    engine = EngagementEngine("user1")
    engine.score = 100
    engine.apply_penalty(5)

    assert engine.score == 0


def test_apply_penalty_more_than_five_never_goes_negative():
    engine = EngagementEngine("user1")
    engine.score = 100
    engine.apply_penalty(8)

    assert engine.score == 0


def test_apply_penalty_more_than_ten_reports_removes_verified():
    engine = EngagementEngine("user1", verified=True)
    engine.score = 500
    engine.apply_penalty(11)

    assert engine.verified is False
    assert engine.score == 0


def test_apply_penalty_ten_reports_keeps_verified():
    engine = EngagementEngine("user1", verified=True)
    engine.score = 500
    engine.apply_penalty(10)

    assert engine.verified is True


def test_multiple_interactions_accumulate_score():
    engine = EngagementEngine("user1")
    engine.process_interaction("like", 10)      # 10
    engine.process_interaction("comment", 2)    # 10
    engine.process_interaction("share", 1)      # 10

    assert engine.score == 30


def test_verified_multiple_interactions_accumulate_score():
    engine = EngagementEngine("user1", verified=True)
    engine.process_interaction("like", 10)      # 15
    engine.process_interaction("comment", 2)    # 15
    engine.process_interaction("share", 1)      # 15

    assert engine.score == 45.0