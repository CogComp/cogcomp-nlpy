import logging

from .view import *

logger = logging.getLogger(__name__)

class PredicateArgumentView(View):
    def __init__(self, view, tokens):
        super(PredicateArgumentView, self).__init__(view, tokens)

        self.predicates = []

        # The hypothesis is that all nodes with no incoming edges are predicates.
        for constituent in self.cons_list:
            if 'incoming_relations' not in constituent or len(constituent['incoming_relations']) == 0:
                self.predicates.append(constituent)

    def get_predicates(self):
        """
        Function to return a list of predicates which are constituents with no incoming relations

        @return: list of predicates
        """
        return self.predicates

    def get_arguments(self, predicate):
        """
        Function to return a list of outgoing relations given a predicate

        @param: predicate, the predicate to get outgoing relations from 
        @return: a list of relations, None if the predicate is invalid
        """
        if self._check_predicate(predicate):
            res = []
            for index in predicate['outgoing_relations']:
               res.append(self.get_relations(index))
            return res
        return None

    def get_predicate_properties(self, predicate):
        """
        Function to get the properties of given predicate

        @param: predicate, the predicate to get properties from
        @return: a dictionary object contains following keys: predicate, SenseNumber
        """
        if self._check_predicate(predicate):
            return predicate['properties']
        return None

    def _check_predicate(self, predicate):
        """
        Helper function to check if predicate is valid

        @param: predicate, the predicate to evaluate
        @return: True if the predicate is valid. False, otherwise
        """
        if predicate not in self.predicates:
            logger.error("Predicate " + predicate + " not found")
            return False
        else:
            return True
