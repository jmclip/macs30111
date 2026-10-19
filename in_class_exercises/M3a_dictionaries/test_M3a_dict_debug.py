"""
Tests for M3a_dict_debug.py

Run all:    pytest -v test_M3a_dict_debug.py
Run one:    pytest -v test_M3a_dict_debug.py -k drop_small
"""

import copy

import pytest

from M3a_dict_debug import (
    contributions_by_campaign,
    total_by_campaign_by_zip,
    drop_small_campaigns,
)

KANG = "Kang for President 2016"
KODOS = "Kodos for President 2016"
KRUSTY = "Krusty for President 2016"

# A tiny hand-made dataset, so you can check answers by eye.
C1 = {"first_name": "John", "last_name": "Doe", "zip_code": "60637",
      "campaign": KANG, "amount": 27.50}
C2 = {"first_name": "Jane", "last_name": "Roe", "zip_code": "60637",
      "campaign": KODOS, "amount": 100.00}
C3 = {"first_name": "Jim", "last_name": "Poe", "zip_code": "07974",
      "campaign": KANG, "amount": 10.00}
C4 = {"first_name": "Jen", "last_name": "Loe", "zip_code": "60637",
      "campaign": KANG, "amount": 50.00}
C5 = {"first_name": "Joy", "last_name": "Moe", "zip_code": "10001",
      "campaign": KRUSTY, "amount": 5.00}

CONTRIBUTIONS = [C1, C2, C3, C4, C5]


# ---------------------------------------------------------------------------
# Function 1: contributions_by_campaign
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "contributions, expected",
    [
        ([], {}),
        ([C1], {KANG: [C1]}),
        (CONTRIBUTIONS, {KANG: [C1, C3, C4], KODOS: [C2], KRUSTY: [C5]}),
    ],
    ids=["empty", "one_contribution", "five_contributions"],
)
def test_contributions_by_campaign(contributions, expected):
    assert contributions_by_campaign(contributions) == expected


# ---------------------------------------------------------------------------
# Function 2: total_by_campaign_by_zip
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "contributions, expected",
    [
        ([], {}),
        ([C1], {KANG: {"60637": 27.5}}),
        ([C1, C4], {KANG: {"60637": 77.5}}),
        (
            CONTRIBUTIONS,
            {
                KANG: {"60637": 77.5, "07974": 10.0},
                KODOS: {"60637": 100.0},
                KRUSTY: {"10001": 5.0},
            },
        ),
    ],
    ids=["empty", "one_contribution", "same_campaign_same_zip",
         "five_contributions"],
)
def test_total_by_campaign_by_zip(contributions, expected):
    assert total_by_campaign_by_zip(contributions) == expected


# ---------------------------------------------------------------------------
# Function 3: drop_small_campaigns
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "totals, min_total, expected",
    [
        ({}, 50.0, {}),
        ({KANG: 87.5, KODOS: 100.0}, 50.0, {KANG: 87.5, KODOS: 100.0}),
        ({KANG: 87.5, KODOS: 100.0, KRUSTY: 5.0}, 50.0,
         {KANG: 87.5, KODOS: 100.0}),
        ({KANG: 87.5, KRUSTY: 5.0}, 1000.0, {}),
    ],
    ids=["empty", "keep_all", "drop_one", "drop_all"],
)
def test_drop_small_campaigns(totals, min_total, expected):
    original = copy.deepcopy(totals)
    assert drop_small_campaigns(totals, min_total) == expected
    assert totals == original, "drop_small_campaigns modified its input!"
