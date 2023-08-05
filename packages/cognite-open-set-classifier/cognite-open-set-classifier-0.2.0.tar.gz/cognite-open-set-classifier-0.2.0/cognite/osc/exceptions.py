class MissingColumnException(Exception):
    pass


class WrongTypeException(Exception):
    pass


class EmptyListException(Exception):
    pass


class TooFewSamplesPerClassException(Exception):
    pass


class ColumnNotInDataFrame(Exception):
    pass


class EmptyFeatureException(Exception):
    pass


class MissingTypeNumOrTypeNameException(Exception):
    pass
