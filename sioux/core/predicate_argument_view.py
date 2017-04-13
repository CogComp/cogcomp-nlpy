import logging

from .view import *

logger = logging.getLogger(__name__)

class PredicateArgumentView(View):
    def __init__(self, view, tokens):
        super(PredicateArgumentView, self).__init__(view, tokens)

        self.predicates = []

        # Building connection between constituents based on relation
        # Assuming that relations exist, otherwise this __init__ should not be called
        for relation_index in range(len(self.relation_array)):
            relation = self.relation_array[relation_index]
            src = self.cons_list[relation['srcConstituent']]
            target = self.cons_list[relation['targetConstituent']]
            if 'outgoing_relations' not in src:
                src['outgoing_relations'] = []
            if 'incoming_relations' not in target:
                target['incoming_relations'] = []
            src['outgoing_relations'].append(relation_index)
            target['incoming_relations'].append(relation_index)

        # The hypothesis is that all nodes with no incoming edges are predicates.
        for constituent in self.cons_list:
            if 'incoming_relations' not in constituent or len(constituent['incoming_relations']) == 0:
                self.predicates.append(constituent)

    # return a list of predicates (constituents)
    def get_predicates(self):
        return self.predicates

    # list of outgoing relations
    def get_arguments(self, predicate):
        if self._check_predicate(predicate):
            res = []
            for index in predicate['outgoing_relations']:
               res.append(self.get_relations(index))
            return res
        return None

    def get_predicate_properties(self, predicate):
        if self._check_predicate(predicate):
            return predicate['properties']
        return None

    def _check_predicate(self, predicate):
        if predicate not in self.predicates:
            logger.error("Predicate " + predicate + " not found")
            return False
        else:
            return True
