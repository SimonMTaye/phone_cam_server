from numpy import ndarray

# TODO add register filter function/decorator


class FilterMixin:
    def apply_filters(self, frame: ndarray) -> ndarray:
        raise NotImplementedError()
