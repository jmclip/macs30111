"""
MACS 30111 -- M1b in-class exercises: tuples, lists of lists, and functions
===========================================================================

Theme: building a playlist from a (small, made-up) song library.
Song titles and albums are real; lengths and ratings are approximate / invented.

HOW TODAY WORKS
---------------
This file has three parts. Each exercise is a function with a docstring that
says what it SHOULD do.

    Part 1  Tuples vs. lists          FIX the broken code        (3 exercises)
    Part 2  Lists of lists & copies   FIX the broken code        (3 exercises)
    Part 3  Functions
        3a  basics (on your own)      FILL IN the blanks         (2 exercises)
        3b  harder (in class)         FILL IN + FIX              (4 exercises)

Look for lines marked  # BUG  (parts 1-2) or  # TODO  (part 3).

HOW TO CHECK YOUR WORK
----------------------
Open a terminal, `cd` into the folder that holds this file, and run pytest
on the TEST file, test_M1b_functions_exercises.py.
(Be in your conda environment, e.g. `conda activate 111`.)

    pytest -v test_M1b_functions_exercises.py                          # every test
    pytest -v -k part1 test_M1b_functions_exercises.py                 # just Part 1
    pytest -v -k part2 test_M1b_functions_exercises.py                 # just Part 2
    pytest -v -k part3b test_M1b_functions_exercises.py                # just Part 3b
    pytest -v -k "part2 and what_if" test_M1b_functions_exercises.py   # one exercise
    pytest -x test_M1b_functions_exercises.py                          # stop at first failure

Do NOT run `pytest M1b_functions_exercises.py` (this file): it has no tests in it,
so pytest just says "collected 0 items".

Every test that fails prints a HINT explaining what it expected. Read it!

You can also try things in ipython (see the "Trying your code in ipython" slide).
Turn on autoreload BEFORE importing, so saved edits are picked up automatically:

    In [1]: %load_ext autoreload
    In [2]: %autoreload 2
    In [3]: import M1b_functions_exercises as m1b
    In [4]: m1b.describe_song(m1b.SONGS[0])

After you edit and save this file, just call the function again (no re-import).

Running this file directly (`python M1b_functions_exercises.py`) runs the
short demos marked "DEMO".
"""

import copy
import traceback

# ---------------------------------------------------------------------------
# The song library
# ---------------------------------------------------------------------------
# Each song is a TUPLE:  (title, album, length_in_seconds, rating_out_of_5)
#                          str    str       int               float
# A tuple is a good fit for one song: it is a fixed "record" whose pieces
# always come in the same order, and nobody should change it by accident.
# The LIBRARY itself is a LIST of tuples, because we add and remove songs.

SONGS = [
    ("Shake It Off", "1989", 219, 4.5),
    ("Anti-Hero", "Midnights", 200, 4.8),
    ("Love Story", "Fearless", 235, 4.2),
    ("Cruel Summer", "Lover", 178, 5.0),
    ("All Too Well", "Red", 329, 4.9),
    ("The Fate of Ophelia", "The Life of a Showgirl", 226, 4.6),
]


# ===========================================================================
# PART 1: TUPLES VS. LISTS                                    (~8 minutes)
# ===========================================================================
#
# DEMO A -- tuples can hold MIXED TYPES
#   A single song mixes strings, an int, and a float. That's fine: tuples
#   (and lists) can hold any mix of types.
#
# DEMO B -- tuples are IMMUTABLE (they can't be changed after creation)
#   Trying to change one piece of a tuple raises a TypeError.
#   Run this file (`python M1b_functions_exercises.py`) to see both demos.

def demo_tuples():
    """DEMO: mixed types in a tuple, and what happens if you try to change one."""
    song = SONGS[0]
    print("DEMO A: one song tuple:", song)
    for piece in song:
        print("   ", repr(piece), "has type", type(piece).__name__)

    print("\nDEMO B: trying to change the rating with song[3] = 5.0 ...")
    try:
        song[3] = 5.0
    except TypeError as err:
        # We'll cover try/except properly later -- here it just lets the demo
        # keep running so you can read the error message.
        print("    TypeError:", err)
    print("    The song is unchanged:", song)


# ---------------------------------------------------------------------------
# Exercise 1.1  (FIX)  Unpacking a tuple
# ---------------------------------------------------------------------------
# "Unpacking" assigns each piece of a tuple to its own variable in one line:
#       title, album, seconds, rating = song
# The names on the left are matched to the pieces BY POSITION.

def describe_song(song):
    """
    Describe a song as a string like "Shake It Off (1989) - 3:39".

    Inputs:
        song (tuple): (title, album, length_in_seconds, rating)

    Returns (str): "<title> (<album>) - <minutes>:<seconds>", with the
        seconds always shown as two digits (3:09, not 3:9).
    """
    title, seconds, album, rating = song          # BUG: check the order!
    minutes = seconds // 60
    leftover = seconds % 60
    return f"{title} ({album}) - {minutes}:{leftover:02d}"


# ---------------------------------------------------------------------------
# Exercise 1.2  (FIX)  "Changing" a tuple means making a new one
# ---------------------------------------------------------------------------
# You can't change a tuple in place (see DEMO B). Instead, build a NEW tuple
# that has the pieces you want. Two ways that work:
#       (song[0], song[1], song[2], new_value)
#       song[:3] + (new_value,)        <- note the comma: (x,) is a 1-item tuple

def update_rating(song, new_rating):
    """
    Return a NEW song tuple with the rating replaced by new_rating.
    The original song must not change.

    Inputs:
        song (tuple): (title, album, length_in_seconds, rating)
        new_rating (float): the new rating

    Returns (tuple): the same song, with the new rating
    """
    song[3] = new_rating                          # BUG: tuples are immutable
    return song

# [on your own, after class!]
# ---------------------------------------------------------------------------
# Exercise 1.3  (FIX)  When you need a list instead 
# ---------------------------------------------------------------------------
# An "up next" queue grows and shrinks, so it should be a LIST.
# Careful: `queue = songs` would NOT make a new list -- it's a second name for
# the same list (an "alias"), so appending would change the caller's list too.

def build_queue(songs, extra_song):
    """
    Return an "up next" queue: all of `songs` in order, then `extra_song`.
    The list passed in as `songs` must not change.

    Inputs:
        songs (list of tuples): the songs already queued
        extra_song (tuple): one more song to add at the end

    Returns (list of tuples): the new queue
    """
    queue = tuple(songs)                          # BUG: can a tuple .append()?
    queue.append(extra_song)
    return queue


# ===========================================================================
# PART 2: LISTS OF LISTS -- ALIASES, SHALLOW COPIES, DEEP COPIES  (~13 min)
# ===========================================================================
#
# WHERE DO LISTS LIVE? THE HEAP
# -----------------------------
# Python keeps every list object in a region of memory called the HEAP.
# A variable doesn't hold the list itself -- it holds a REFERENCE (an arrow)
# pointing at the list on the heap. A list of lists is a list of arrows,
# each pointing at another list on the heap:
#
#     ratings ──► [ ● , ● , ● ]          <- the "outer" list
#                   │   │   │
#                   ▼   ▼   ▼
#                 [5,4] [3,5] [4,4]      <- three separate "inner" lists (rows)
#
# Three ways to "copy" ratings, from least to most copying:
#
#   ALIAS         r2 = ratings
#                 No copy at all: a second arrow to the SAME outer list.
#                 Changing r2 in any way changes ratings.
#
#   SHALLOW COPY  r2 = ratings[:]        (or list(ratings), copy.copy(ratings))
#                 A NEW outer list, but its arrows point at the SAME rows.
#                 r2.append(row) is safe.   r2[0][1] = 9 changes ratings too!
#
#   DEEP COPY     r2 = copy.deepcopy(ratings)   (or [row[:] for row in ratings])
#                 New outer list AND new rows. Nothing is shared.
#
# Rule of thumb (from the slides): are you modifying with something NEW
# (replacing/adding a row), or changing a row IN PLACE (r2[i][j] = ...)?
# In-place changes to rows need a deep copy.
#
# Our data: a RATINGS TABLE. Each row is one friend; each column is one song.
#                       song 0  song 1  song 2
#     ratings = [      [  5,      4,      3  ],    # friend 0
#                      [  4,      5,      2  ]]    # friend 1

def demo_heap():
    """DEMO: `is` tells you whether two names point at the same object on the heap."""
    ratings = [[5, 4, 3], [4, 5, 2]]
    alias = ratings
    shallow = ratings[:]
    deep = copy.deepcopy(ratings)
    print("alias is ratings?          ", alias is ratings)          # True
    print("shallow is ratings?        ", shallow is ratings)        # False
    print("shallow[0] is ratings[0]?  ", shallow[0] is ratings[0])  # True (shared row!)
    print("deep[0] is ratings[0]?     ", deep[0] is ratings[0])     # False


# ---------------------------------------------------------------------------
# Exercise 2.1  (FIX)  Building an empty table
# ---------------------------------------------------------------------------
# Remember from the slides:   m = [[0]*5]*5   vs.   m1 = [[0]*5 for i in range(5)]

def empty_ratings(num_friends, num_songs):
    """
    Make a ratings table full of zeros, with one row per friend and one
    column per song. Every row must be its own separate list.

    Inputs:
        num_friends (int): number of rows
        num_songs (int): number of columns

    Returns (list of lists of ints): the table
    """
    return [[0] * num_songs] * num_friends        # BUG: how many row lists exist on the heap?


# ---------------------------------------------------------------------------
# Exercise 2.2  (FIX)  Adding a friend without changing the original
# ---------------------------------------------------------------------------

def add_friend(ratings, new_row):
    """
    Return a NEW table with new_row added as the last row.
    The original `ratings` must not change.

    Inputs:
        ratings (list of lists): the current table
        new_row (list): the new friend's ratings

    Returns (list of lists): the bigger table
    """
    new_table = ratings                           # BUG: alias or copy?
    new_table.append(new_row)
    return new_table


# ---------------------------------------------------------------------------
# Exercise 2.3  (FIX)  A "what if" table
# ---------------------------------------------------------------------------
# Think about which kind of copy you need when you change ONE NUMBER inside a row.

def what_if(ratings, friend, song, new_score):
    """
    Return a NEW table that is the same as `ratings`, except that
    friend `friend` gives song `song` the score `new_score`.
    The original `ratings` (including its rows) must not change.

    Inputs:
        ratings (list of lists): the current table
        friend (int): row index
        song (int): column index
        new_score (int): the new score

    Returns (list of lists): the "what if" table
    """
    new_table = ratings[:]                        # BUG: is a shallow copy enough here?
    new_table[friend][song] = new_score
    return new_table


# ===========================================================================
# PART 3: FUNCTIONS                                           (~20 minutes)
# ===========================================================================

# ---------------------------------------------------------------------------
# PART 3a: BASICS -- on your own (we skip these in class)
# ---------------------------------------------------------------------------

# Exercise 3.1  (FILL IN)  print vs. return
# A function that only PRINTS gives back None. To use a result somewhere
# else (in a test, in another function), you must RETURN it.

def format_duration(seconds):
    """
    Turn a length in seconds into a "m:ss" string, e.g. 219 -> "3:39".

    Inputs:
        seconds (int): a length in seconds

    Returns (str): the length as "minutes:seconds", seconds always 2 digits
    """
    # TODO: compute the minutes and leftover seconds and RETURN the string
    # (Exercise 1.1 has a line that will help.)
    pass


# Exercise 3.2  (FILL IN)  Default parameters and keyword arguments
# A parameter with a default value can be left out when calling:
#       playlist_length(SONGS)                    -> uses unit="minutes"
#       playlist_length(SONGS, unit="seconds")    -> keyword argument

def playlist_length(songs, unit="minutes"):
    """
    Total length of a list of songs.

    Inputs:
        songs (list of tuples): the songs
        unit (str): "minutes" (default) or "seconds"

    Returns (float or int): total minutes rounded to 1 decimal place if
        unit is "minutes"; total seconds (an int) if unit is "seconds"
    """
    # TODO: add up the lengths (index 2 of each song tuple), then return the
    # total in the requested unit. round(x, 1) rounds to one decimal place.
    pass


# ---------------------------------------------------------------------------
# PART 3b: HARDER -- in class: scope, the call stack, and catching errors
# ---------------------------------------------------------------------------
# These functions work together to build a "top songs" playlist:
#
#     build_playlist(songs, n)            make the playlist
#         └── rank_songs(songs)           sort songs best-first
#               └── song_score(song)      rating + bonus
#                     └── album_bonus(song)   +0.5 for the favorite album
#
# FAVORITE_ALBUM is a GLOBAL variable: it is defined outside every function,
# so any function can READ it. ALL_CAPS signals "this is a constant -- read it,
# don't change it." Variables created inside a function are LOCAL: they exist
# only while that function is running.

FAVORITE_ALBUM = "Midnights"
BONUS = 0.5


def show_call_stack():
    """
    Helper (already written): print the functions from this file that are
    on the call stack right now, oldest call first. Call it from inside any
    function to see how you got there.
    """
    names = [frame.name for frame in traceback.extract_stack()[:-1]
             if frame.filename == __file__ and frame.name != "<module>"]
    print("call stack (oldest first):", " -> ".join(names))


# Exercise 3.3  (FILL IN)  Global vs. local variables

def album_bonus(song):
    """
    Return BONUS if the song is on FAVORITE_ALBUM, otherwise 0.

    Inputs:
        song (tuple): (title, album, length_in_seconds, rating)

    Returns (float): the bonus
    """
    # TODO: compare the song's album (index 1) to the GLOBAL FAVORITE_ALBUM
    pass


# Now PREDICT what this code does. Don't run it until you've decided!
#
#     FAVORITE_ALBUM = "Midnights"          # (the global above)
#
#     def pick_album(mood):
#         FAVORITE_ALBUM = "Red"            # assignment inside a function...
#         if mood == "sad":
#             return FAVORITE_ALBUM
#         return "1989"
#
#     result = pick_album("sad")
#
# After these lines run, what are `result` and the global FAVORITE_ALBUM?
# TODO: replace each None with your answer (a string).
PREDICT_RESULT = None
PREDICT_GLOBAL_AFTER = None


# Exercise 3.4  (FILL IN)  The function call stack

def song_score(song):
    """Score = the song's rating plus its album bonus. (Already written.)"""
    return song[3] + album_bonus(song)


def rank_songs(songs):
    """
    Return the songs sorted from HIGHEST score to LOWEST.
    (Used in Exercise 3.6 -- leave it alone for now.)
    """
    scored = []
    for song in songs:
        scored.append((song_score(song), song))
    scored.sort()                                  # sorts by score (the first item)
    return [song for score, song in scored]


def build_playlist(songs, n):
    """Return the top n songs, best first. (Already written.)"""
    ranked = rank_songs(songs)
    return ranked[:n]


# When build_playlist(SONGS, 3) runs, at the moment album_bonus is running,
# which functions are on the call stack? List them OLDEST call first, as
# strings. (Each call adds a frame; a frame is removed when its function returns.)
#
# Check yourself: add the line  show_call_stack()  as the first line of
# album_bonus, then run  m1b.build_playlist(m1b.SONGS, 3)  in ipython. Remove it after.
#
# TODO: fill in the list
CALL_STACK = []

# In which ONE function's frame does the local variable `scored` live?
# TODO: replace None with the function name (a string)
SCORED_LIVES_IN = None


# Exercise 3.5  (FIX)  A REAL error: messy data raises a TypeError
# ---------------------------------------------------------------------------
# Someone added bonus tracks by hand and typed one length as "m:ss" text.
# total_seconds(SONGS + BONUS_TRACKS) crashes. Run it in ipython and READ the
# traceback: which line fails, and what types is it trying to add?

BONUS_TRACKS = [
    ("Wildest Dreams", "1989", 220, 4.4),
    ("Enchanted", "Speak Now", "5:52", 4.7),       # <- length typed as a string
]


def to_seconds(length):
    """
    Convert a song length to an int number of seconds.

    Inputs:
        length (int or str): either an int number of seconds (returned as-is)
            or a string "m:ss" such as "5:52" (which is 352 seconds)

    Returns (int): the length in seconds
    """
    # TODO: if length is a string, split it on ":" and convert the pieces
    # with int(...). Otherwise, return it unchanged.
    # Hint: type(length) == str   tells you whether it's a string.
    pass


def total_seconds(songs):
    """
    Add up the lengths of all songs, in seconds.

    Inputs:
        songs (list of tuples): the songs (lengths may be ints or "m:ss" strings)

    Returns (int): total seconds
    """
    total = 0
    for song in songs:
        total = total + song[2]                     # BUG: crashes on "5:52" -- use to_seconds
    return total


# Exercise 3.6  (FIX)  A SILENT error: wrong answer, no crash
# ---------------------------------------------------------------------------
# build_playlist(SONGS, 3) runs without any error... but listen to the
# playlist it makes. Are those really the three best-scored songs?
# Find the bug in rank_songs (above) and fix it.
# Hint: look up what the `reverse` argument of .sort() does.


# ---------------------------------------------------------------------------
# Running the file directly runs the demos.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    demo_tuples()
    print()
    demo_heap()
