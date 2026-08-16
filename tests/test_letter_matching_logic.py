import numpy as np

from screens.game_letter_matching import LETTERS, is_match, shuffle_pairs


def test_shuffle_pairs_produces_two_of_each_letter():
    layout = shuffle_pairs(LETTERS, rng=np.random.RandomState(0))
    assert sorted(layout.keys()) == list(range(2 * len(LETTERS)))
    counts = {}
    for letter in layout.values():
        counts[letter] = counts.get(letter, 0) + 1
    assert set(counts) == set(LETTERS)
    assert all(count == 2 for count in counts.values())


def test_is_match():
    assert is_match("A", "A") is True
    assert is_match("A", "B") is False
