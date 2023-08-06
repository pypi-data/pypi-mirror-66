# -*- coding: utf-8 -*-
"""This module contains classes and functions related to the
construction of finite element matrices.

The basic workflow is the following:

1. Create :class:`~skfem.assembly.InteriorBasis` and/or :class:`~skfem.assembly.FacetBasis`
   objects.
2. Define the bilinear and linear forms using the decorators :func:`~skfem.assembly.bilinear_form`
   and :func:`~skfem.assembly.linear_form`.
3. Assemble finite element matrices using :func:`~skfem.assembly.asm`.

"""

from typing import Union

from numpy import ndarray

from scipy.sparse import csr_matrix

from .basis import Basis, InteriorBasis, FacetBasis
from .dofs import Dofs
from .form import Form, BilinearForm, LinearForm, Functional,\
    bilinear_form, linear_form, functional


def asm(form: Form,
        *args, **kwargs) -> Union[ndarray, csr_matrix]:
    return form.assemble(*args, **kwargs)
