from typing import List

from ccg_nlpy.core.text_annotation import TextAnnotation


class Annotator:
    def load_params(self) -> None:
        """
        Load the relevant model parameters.
        :return: None
        """
        raise NotImplementedError

    def get_view_name(self) -> str:
        """
        Return the name of the view that will be provided by the model.
        :return: viewName
        """
        raise NotImplementedError

    def add_view(self, docta: TextAnnotation) -> TextAnnotation:
        """
        Takes a text annotation and adds the view provided by this model to it.
        :return: TextAnnotation
        """
        raise NotImplementedError

    def get_required_views(self) -> List[str]:
        """
        Return the list of viewnames required by the model.
        :return: List of view names
        """
        raise NotImplementedError