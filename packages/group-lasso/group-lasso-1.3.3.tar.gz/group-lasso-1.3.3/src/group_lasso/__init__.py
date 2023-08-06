"""Group lasso regularised linear models.
"""


__version__ = "1.3.3"
__author__ = "Yngve Mardal Moe"
__email__ = "yngve.m.moe@gmail.com"


from group_lasso._group_lasso import (
    GroupLasso,
    LogisticGroupLasso,
    BaseGroupLasso,
)


MultinomialGroupLasso = LogisticGroupLasso
