"""Post-transcription correction: applies config/corrections.yaml rules.

Word-window-aware replacement — when a rule's match spans multiple raw
words, timing for the replacement token(s) is re-derived by proportionally
splitting the original matched words' [start, end] range, so downstream
modules never see a corrected word with a fabricated/zero-length timespan.
"""

from __future__ import annotations

from edit_cli.config.schema import CorrectionRule
from edit_cli.models import Word


def apply_corrections(words: list[Word], rules: list[CorrectionRule]) -> list[Word]:
    """Apply ``rules`` in order against ``words``, returning a new list with
    ``corrected_word`` (and ``start``/``end`` where a match spans/merges
    multiple raw words) updated. ``raw_word`` is preserved unmodified for
    audit purposes.
    """
    raise NotImplementedError
