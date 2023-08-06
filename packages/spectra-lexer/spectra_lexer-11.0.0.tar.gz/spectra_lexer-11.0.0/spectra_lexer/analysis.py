from typing import List, Mapping, Sequence, Tuple

from spectra_lexer.lexer import LexerResult, LexerRule, \
    PrefixMatcher, SpecialMatcher, StenoLexer, StrokeMatcher, WordMatcher
from spectra_lexer.resource.keys import StenoKeyConverter
from spectra_lexer.resource.rules import StenoRule, StenoRuleCollection


class StenoAnalyzer:
    """ Key-converting wrapper for the lexer. Also uses multiprocessing to make an examples index. """

    # Methods for special rules by ID that have hard-coded behavior in the lexer.
    LEXER_SPECIALS = {"~ABBR": SpecialMatcher.add_rule_abbreviation,
                      "~PROP": SpecialMatcher.add_rule_proper,
                      "~PFSF": SpecialMatcher.add_rule_affix,
                      "~????": SpecialMatcher.add_rule_fallback}

    def __init__(self, converter:StenoKeyConverter, lexer:StenoLexer, refmap:Mapping[LexerRule, StenoRule]) -> None:
        self._to_skeys = converter.rtfcre_to_skeys   # Converts user RTFCRE steno strings to s-keys.
        self._to_rtfcre = converter.skeys_to_rtfcre  # Converts s-keys back to RTFCRE.
        self._lexer = lexer                          # Main analysis engine; operates only on s-keys.
        self._refmap = refmap                        # Mapping of lexer rule objects to their original StenoRules.

    def query(self, keys:str, letters:str, match_all_keys=False) -> StenoRule:
        """ Return an analysis matching <keys> to <letters>. Thoroughly parse the key string into s-keys first.
           If <match_all_keys> is True and the best result is missing some, return a fully unmatched result instead. """
        skeys = self._to_skeys(keys)
        result = self._lexer.query(skeys, letters)
        info = self._result_info(result)
        rule = StenoRule.analysis(keys, letters, info)
        unmatched_skeys = result.unmatched_skeys
        last_match_end = 0
        if match_all_keys and unmatched_skeys:
            unmatched_skeys = skeys
        else:
            for lr, start in zip(result.rules, result.rule_positions):
                child = self._refmap[lr]
                length = len(lr.letters)
                last_match_end = start + length
                rule.add_connection(child, start, length)
        if unmatched_skeys:
            ur = StenoRule.unmatched(self._to_rtfcre(unmatched_skeys))
            rule.add_connection(ur, last_match_end, len(letters) - last_match_end)
        return rule

    @staticmethod
    def _result_info(result:LexerResult) -> str:
        """ Return an info string for this result. The output is nowhere near reliable if some keys are unmatched. """
        if not result.unmatched_skeys:
            info = "Found complete match."
        elif result.rules:
            info = "Incomplete match. Not reliable."
        else:
            info = "No matches found."
        return info

    def best_translation(self, translations:Sequence[Tuple[str, str]]) -> Tuple[str, str]:
        """ Return the best (most accurate) from a sequence of <translations>. """
        converted = [(self._to_skeys(keys), letters) for keys, letters in translations]
        best_index = self._lexer.find_best_translation(converted)
        return translations[best_index]

    def query_rule_ids(self, keys:str, letters:str) -> List[str]:
        """ Make a lexer query and return the rule IDs in a list with their matching keys and letters.
            This output format works well for parallel operations because:
                - results may be returned out of order, so the matching input is saved with the output.
                - StenoRule objects are recursive structures that pickle poorly, so only the IDs are saved. """
        skeys = self._to_skeys(keys)
        result = self._lexer.query(skeys, letters)
        id_list = self._valid_result_ids(result)
        return [keys, letters, *id_list]

    def _valid_result_ids(self, result:LexerResult) -> List[str]:
        """ Only fully matched translations should have rule IDs returned. Lexer specials should not be included. """
        id_list = []
        if not result.unmatched_skeys:
            for lr in result.rules:
                rule = self._refmap[lr]
                r_id = rule.id
                if r_id not in self.LEXER_SPECIALS:
                    id_list.append(r_id)
        return id_list

    @classmethod
    def from_resources(cls, converter:StenoKeyConverter, rules:StenoRuleCollection,
                       key_sep:str, unordered_keys:str) -> "StenoAnalyzer":
        """ Distribute rules among lexer rule matchers and build the lexer and analyzer. """
        prefix_matcher = PrefixMatcher(key_sep, unordered_keys)
        stroke_matcher = StrokeMatcher(key_sep)
        word_matcher = WordMatcher()
        special_matcher = SpecialMatcher(key_sep)
        refmap = {}
        for rule in rules:
            skeys = converter.rtfcre_to_skeys(rule.keys)
            letters = rule.letters
            # Rare rules are uncommon in usage and/or prone to causing false positives.
            # They lose when breaking ties for the most accurate rule map. """
            weight = 10 * len(letters) - rule.is_rare
            lr = LexerRule(skeys, letters, weight)
            refmap[lr] = rule
            # Add the rule to one of the lexer rule matchers based on its flags.
            if rule.is_special:
                # Special rules are not used by the lexer unless they have a specific ID.
                method = cls.LEXER_SPECIALS.get(rule.id)
                if method is not None:
                    method(special_matcher, lr)
            elif rule.is_stroke:
                # Stroke rules are matched only by complete strokes.
                stroke_matcher.add(lr)
            elif rule.is_word:
                # Word rules are matched only by whole words (but still case-insensitive).
                word_matcher.add(lr)
            else:
                # Rules are added to the tree-based prefix matcher by default.
                prefix_matcher.add(lr)
        lexer = StenoLexer(prefix_matcher, stroke_matcher, word_matcher, special_matcher)
        return cls(converter, lexer, refmap)
