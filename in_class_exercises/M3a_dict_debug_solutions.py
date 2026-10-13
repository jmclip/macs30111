"""
MACS 30111 -- Dictionaries: Debugging Lab (Day 1) -- SOLUTIONS (instructors only)

Each of the three functions below has ONE bug. The tests in
test_M3a_dict_debug.py describe what each function is supposed to do.

Your job:
  1. Run the tests:        pytest -v test_M3a_dict_debug.py
  2. Read the failure output carefully: which test? which input? what
     was expected vs. what came back? (or: what error was raised, and
     on which line?)
  3. Fix the bug. Change as little code as possible.
  4. Directly above your fix, add a comment that starts with  # FIX:
     and explains in one sentence what was wrong and why.

You are done when all tests pass.

Each contribution is a dictionary like the ones in the reading:
    {"first_name": "John", "last_name": "Doe", "zip_code": "60637",
     "campaign": "Kang for President 2016", "amount": 27.50}
"""


# ---------------------------------------------------------------------------
# Function 1
# ---------------------------------------------------------------------------
def contributions_by_campaign(contributions):
    """
    Group contributions by campaign.

    Args:
        contributions (List[Dict[str, (str | float)]]): one dictionary per
            contribution

    Returns (Dict[str, List[Dict[str, (str | float)]]]): maps each campaign
        name to the list of contributions to that campaign, in their
        original order.
    """
    rv = {}
    for contribution in contributions:
        campaign = contribution["campaign"]
        # FIX: rv.get(campaign, []) returned a new list that was never stored
        # in rv, so the appends were lost; create and store the list first.
        if campaign not in rv:
            rv[campaign] = []
        rv[campaign].append(contribution)
    return rv


# ---------------------------------------------------------------------------
# Function 2
# ---------------------------------------------------------------------------
def total_by_campaign_by_zip(contributions):
    """
    Compute total contributions for each campaign, broken down by ZIP code.

    Args:
        contributions (List[Dict[str, (str | float)]]): one dictionary per
            contribution

    Returns (Dict[str, Dict[str, float]]): maps each campaign to a
        dictionary that maps each ZIP code to the total amount contributed
        to that campaign from that ZIP code. Example:
            {"Kang for President 2016": {"60637": 77.5, "07974": 10.0},
             "Kodos for President 2016": {"60637": 100.0}}
    """
    by_campaign_by_zip = {}
    for contribution in contributions:
        campaign = contribution["campaign"]
        zip_code = contribution["zip_code"]
        # FIX: the inner dict was reset on every contribution, wiping out
        # earlier ZIP totals; only create it the first time we see a campaign.
        if campaign not in by_campaign_by_zip:
            by_campaign_by_zip[campaign] = {}
        inner = by_campaign_by_zip[campaign]
        inner[zip_code] = inner.get(zip_code, 0) + contribution["amount"]
    return by_campaign_by_zip


# ---------------------------------------------------------------------------
# Function 3
# ---------------------------------------------------------------------------
def drop_small_campaigns(totals, min_total):
    """
    Keep only the campaigns that raised at least min_total.

    Args:
        totals (Dict[str, float]): maps campaign name to total raised
        min_total (float): the minimum total needed to keep a campaign

    Returns (Dict[str, float]): a NEW dictionary containing only the
        campaigns that raised at least min_total. The input dictionary
        must NOT be modified.
    """
    # FIX: deleting keys while looping over totals raises RuntimeError and
    # modifies the caller's dict; build and return a new dict instead.
    # (Collecting keys first, then deleting, avoids the error but still
    # changes the input, so it fails the input-unchanged test.)
    return {campaign: total for campaign, total in totals.items()
            if total >= min_total}
