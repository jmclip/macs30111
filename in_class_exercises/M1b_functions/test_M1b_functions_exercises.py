"""
Tests for M1b_functions_exercises.py

Run from the folder that holds both files, naming THIS test file:

    pytest -v test_M1b_functions_exercises.py                     # everything
    pytest -v -k part1 test_M1b_functions_exercises.py            # one part (part1, part2, part3a, part3b)
    pytest -v -k describe_song test_M1b_functions_exercises.py    # one exercise
    pytest -x test_M1b_functions_exercises.py                     # stop at the first failure

(Running pytest on M1b_functions_exercises.py finds no tests: "collected 0 items".)

Each failing test prints a HINT. Read the hint first, then the
"assert" line just above it, which shows what your code actually returned.
"""

import copy
import importlib
import os

import pytest

# Instructors: set M1B_MODULE=M1b_functions_exercises_solutions to test the key.
ex = importlib.import_module(os.environ.get("M1B_MODULE", "M1b_functions_exercises"))


def fresh_songs():
    """A private copy of the library, so one test can't break another."""
    return copy.deepcopy(ex.SONGS)


# ===========================================================================
# PART 1: tuples vs. lists
# ===========================================================================

def test_part1_describe_song():
    song = ("Shake It Off", "1989", 219, 4.5)
    try:
        got = ex.describe_song(song)
    except TypeError as err:
        pytest.fail(f"HINT: {err}. One of your variables holds the wrong piece of the song -- "
                    "the tuple is (title, album, seconds, rating), matched BY POSITION.")
    assert got == "Shake It Off (1989) - 3:39", (
        "HINT: the names on the left of `title, ... = song` are matched to the "
        "tuple BY POSITION. The song tuple is (title, album, seconds, rating)."
    )


def test_part1_describe_song_pads_seconds():
    got = ex.describe_song(("Song", "Album", 181, 3.0))
    assert got == "Song (Album) - 3:01", "HINT: 181 seconds should show as 3:01, not 3:1."


def test_part1_update_rating():
    song = ("Love Story", "Fearless", 235, 4.2)
    try:
        got = ex.update_rating(song, 5.0)
    except TypeError as err:
        pytest.fail(f"HINT: tuples can't be changed in place ({err}). "
                    "Build and return a NEW tuple instead.")
    assert got == ("Love Story", "Fearless", 235, 5.0), "HINT: only the rating (last item) should change."
    assert isinstance(got, tuple), f"HINT: return a tuple, not a {type(got).__name__}."
    assert song == ("Love Story", "Fearless", 235, 4.2), "HINT: the original song must not change."


def test_part1_build_queue():
    songs = fresh_songs()[:2]
    original = list(songs)
    extra = ex.SONGS[3]
    try:
        got = ex.build_queue(songs, extra)
    except AttributeError as err:
        pytest.fail(f"HINT: {err}. Tuples have no .append() -- a queue that grows should be a list.")
    assert isinstance(got, list), f"HINT: the queue should be a list, not a {type(got).__name__}."
    assert got == original + [extra], "HINT: the queue should be the songs in order, then the extra song."
    assert songs == original, (
        "HINT: the caller's list changed! `queue = songs` is an alias (same list). "
        "Make a new list, e.g. list(songs)."
    )


# ===========================================================================
# PART 2: lists of lists, aliases, shallow and deep copies
# ===========================================================================

def test_part2_empty_ratings_shape():
    got = ex.empty_ratings(3, 4)
    assert got == [[0, 0, 0, 0]] * 3, "HINT: expected 3 rows of 4 zeros."


def test_part2_empty_ratings_rows_are_separate():
    got = ex.empty_ratings(3, 4)
    got[0][0] = 5
    assert got[1][0] == 0, (
        "HINT: changing row 0 also changed row 1, so every row is the SAME list on the heap. "
        "[[0]*4]*3 copies the arrow to one row three times. Use a list comprehension "
        "so a new row is made each time: [[0]*num_songs for i in range(num_friends)]."
    )


def test_part2_add_friend():
    ratings = [[5, 4, 3], [4, 5, 2]]
    got = ex.add_friend(ratings, [1, 2, 3])
    assert got == [[5, 4, 3], [4, 5, 2], [1, 2, 3]], "HINT: the new row should be added at the end."
    assert ratings == [[5, 4, 3], [4, 5, 2]], (
        "HINT: the original table changed! `new_table = ratings` is an ALIAS (two names, one list). "
        "Make a copy first. (Adding a row only changes the outer list, so a shallow copy "
        "like ratings[:] is enough here.)"
    )


def test_part2_what_if():
    ratings = [[5, 4, 3], [4, 5, 2]]
    got = ex.what_if(ratings, 1, 2, 5)
    assert got == [[5, 4, 3], [4, 5, 5]], "HINT: friend 1 should now give song 2 a score of 5."
    assert ratings == [[5, 4, 3], [4, 5, 2]], (
        "HINT: the original table changed! ratings[:] is a SHALLOW copy: a new outer list "
        "whose rows are still shared. Changing a number inside a row needs a DEEP copy: "
        "copy.deepcopy(ratings) or [row[:] for row in ratings]."
    )


# ===========================================================================
# PART 3a: functions basics (on your own)
# ===========================================================================

def test_part3a_format_duration():
    got = ex.format_duration(219)
    assert got is not None, (
        "HINT: format_duration returned None. Did you print instead of return "
        "(or not finish the TODO)? A function that only prints gives back None."
    )
    assert got == "3:39"
    assert ex.format_duration(181) == "3:01", "HINT: seconds should always have two digits."
    assert ex.format_duration(59) == "0:59"


def test_part3a_playlist_length_default_minutes():
    got = ex.playlist_length(fresh_songs())
    assert got is not None, "HINT: playlist_length returned None -- did you return the total?"
    assert got == 23.1, "HINT: 1387 total seconds is 23.1 minutes (rounded to 1 decimal)."


def test_part3a_playlist_length_keyword_seconds():
    assert ex.playlist_length(fresh_songs(), unit="seconds") == 1387, (
        "HINT: with unit=\"seconds\", return the total number of seconds (an int)."
    )
    assert ex.playlist_length([], unit="seconds") == 0, "HINT: an empty playlist is 0 seconds long."


# ===========================================================================
# PART 3b: scope, the call stack, catching errors
# ===========================================================================

def test_part3b_album_bonus():
    assert ex.album_bonus(("Anti-Hero", "Midnights", 200, 4.8)) == 0.5, (
        "HINT: a song on FAVORITE_ALBUM should get BONUS (0.5). Did you return a value?"
    )
    assert ex.album_bonus(("Love Story", "Fearless", 235, 4.2)) == 0, "HINT: other albums get 0."


def test_part3b_album_bonus_reads_the_global(monkeypatch):
    monkeypatch.setattr(ex, "FAVORITE_ALBUM", "Red")
    assert ex.album_bonus(("All Too Well", "Red", 329, 4.9)) == 0.5, (
        "HINT: when FAVORITE_ALBUM changes, the bonus should follow it. "
        "Compare against the global FAVORITE_ALBUM instead of typing \"Midnights\"."
    )


def test_part3b_predict_shadowing():
    assert ex.PREDICT_RESULT is not None and ex.PREDICT_GLOBAL_AFTER is not None, (
        "HINT: fill in PREDICT_RESULT and PREDICT_GLOBAL_AFTER (both strings)."
    )
    assert ex.PREDICT_RESULT == "Red", (
        "HINT: inside pick_album, FAVORITE_ALBUM = \"Red\" makes a new LOCAL variable, "
        "and the function returns that local value."
    )
    assert ex.PREDICT_GLOBAL_AFTER == "Midnights", (
        "HINT: assigning inside a function creates a LOCAL variable that shadows the "
        "global; the global itself never changes (that would need the `global` keyword)."
    )


def test_part3b_call_stack():
    assert ex.CALL_STACK, "HINT: fill in CALL_STACK with function names, oldest call first."
    assert ex.CALL_STACK == ["build_playlist", "rank_songs", "song_score", "album_bonus"], (
        "HINT: start with the first function called (build_playlist) and follow the calls "
        "down to album_bonus. Try show_call_stack() inside album_bonus to check."
    )


def test_part3b_scored_lives_in():
    assert ex.SCORED_LIVES_IN == "rank_songs", (
        "HINT: a local variable lives in the frame of the function that creates it. "
        "Which function has the line `scored = []`?"
    )


def test_part3b_to_seconds():
    assert ex.to_seconds("5:52") == 352, "HINT: \"5:52\" is 5 minutes and 52 seconds = 352 seconds."
    assert ex.to_seconds("3:05") == 185, "HINT: \"3:05\" should be 185."
    assert ex.to_seconds(220) == 220, "HINT: ints should come back unchanged."


def test_part3b_total_seconds_handles_messy_data():
    try:
        got = ex.total_seconds(fresh_songs() + copy.deepcopy(ex.BONUS_TRACKS))
    except TypeError as err:
        pytest.fail(f"HINT: still crashing with TypeError: {err}. "
                    "Use to_seconds(song[2]) so string lengths are converted first.")
    assert got == 1387 + 220 + 352, "HINT: expected 1959 seconds in total."


def test_part3b_rank_songs_best_first():
    try:
        playlist = ex.build_playlist(fresh_songs(), 3)
    except TypeError as err:
        pytest.fail(f"HINT: {err}. Finish album_bonus (Exercise 3.3) first -- "
                    "song_score adds its result to the rating.")
    titles = [song[0] for song in playlist]
    assert titles == ["Anti-Hero", "Cruel Summer", "All Too Well"], (
        f"HINT: got {titles}. No error, but the 'top 3' are the LOWEST-scored songs -- "
        "a silent error! .sort() goes smallest-to-largest; use .sort(reverse=True)."
    )
