"""Class A (引き延ばしフィラー, drop) vs class B (リアクション, always keep)
filler classification.

This is NOT a word-list lookup. A word only becomes an A/B *candidate* by
appearing in ``config.filler.filler_words`` / ``reaction_words``; the class
is then decided from acoustic/context features, per the priority rules
below (mirrors the spec verbatim):

  1. If B-criteria are met, classify B even if the word is in
     ``filler_words`` (filler-list membership never overrides B evidence).
  2. If ambiguous (mixed/insufficient signal), resolve via
     ``config.ambiguous_action`` ("keep" by default — spec: prefer
     over-keeping to over-cutting).
  3. Every decision is emitted with its ``features`` and a human-readable
     ``rule_fired`` string — never a bare class label.

B-criteria (all must hold): gap_before >= reaction_gap_threshold, AND
(pitch_ratio >= pitch_rise_threshold OR rms_ratio >= volume_spike_ratio),
AND EITHER of those two is also boosted by combat_score_at_t >=
combat_score_bias_threshold (combat context is corroborating evidence, not
a standalone trigger — a quiet moment with a pitch spike is still B).

A-criteria (all must hold, and B-criteria do NOT hold): gap_before is
~0 (embedded mid-utterance), pitch is flat-or-falling, volume <= surrounding
speech, and it is followed by a content word (not a cut-off/end-of-segment).

Words that match neither the filler list nor the reaction list are not
touched by this module at all (they are ordinary transcript words).
"""

from __future__ import annotations

from edit_cli.config.schema import FillerConfig
from edit_cli.models import FillerAnalysisEntry, Word


def classify_fillers(
    words: list[Word],
    word_features: dict[str, tuple[float, float, float]],
    combat_score_at: dict[float, float],
    config: FillerConfig,
) -> list[FillerAnalysisEntry]:
    """Classify every word in ``words`` that matches ``config.filler_words``
    or ``config.reaction_words`` (case/reading-normalized match) into class
    A or B.

    Args:
        words: full corrected transcript (word order matters — "followed by
            a content word" for the A-criteria looks at the NEXT entry here).
        word_features: from audio.features.extract_word_features, keyed the
            same way (``f"{word.start}:{word.end}"``).
        combat_score_at: 1s-bucketed combat score timeline (score.combat_score
            output) for the B-criteria combat-context boost; keyed by bucket
            start second.
        config: thresholds.yaml: filler.

    Returns:
        One ``FillerAnalysisEntry`` per candidate word (words that aren't
        filler/reaction-list candidates are omitted, not emitted as
        non-decisions).
    """
    raise NotImplementedError
