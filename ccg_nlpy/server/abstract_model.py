from typing import List

from ccg_nlpy.core.text_annotation import TextAnnotation


class AbstractModel:
    def load_params(self) -> None:
        """
        Load the relevant model parameters.
        :return: None
        """
        raise NotImplementedError

    def get_provided_view(self) -> str:
        """
        Return the name of the view that will be provided by the model.
        :return: viewName
        """
        raise NotImplementedError

    def inference_on_ta(self, docta: TextAnnotation) -> TextAnnotation:
        """
        Takes a text annotation and adds the view provided by this model to it.
        :return: viewName
        """
        raise NotImplementedError

    def get_required_views(self) -> List[str]:
        """
        Return the list of viewnames required by the model.
        :return: viewName
        """
        raise NotImplementedError