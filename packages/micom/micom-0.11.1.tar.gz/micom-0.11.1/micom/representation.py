"""Converts between QP representations."""

import numpy as np
from scipy.sparse import csc_matrix


def sparse_problem(com):
    nv = len(com.variables)
    nc = len(com.constraints)
    var_ids = {v: i for i, v in enumerate(com.variables)}
    coefs = [1 for v in var_ids]
    var_bounds = np.array(
        [
            [
                -np.infty if v.lb is None else v.lb,
                np.infty if v.ub is None else v.ub,
            ]
            for v in com.variables
        ]
    )
    const_bounds = np.zeros((len(com.constraints), 2))
    ri = list(range(len(var_ids)))
    ci = [var_ids[v] for v in var_ids]
    for i, co in enumerate(com.constraints):
        if co.lb is None:
            const_bounds[i, 0] = -np.infty
        else:
            const_bounds[i, 0] = co.lb
        if co.ub is None:
            const_bounds[i, 1] = np.infty
        else:
            const_bounds[i, 1] = co.ub
        c = co.get_linear_coefficients(co.variables)
        ci.extend([var_ids[v] for v in c])
        coefs.extend([c[v] for v in c])
        ri.extend([nv + i for v in c])
    A = csc_matrix((coefs, (ri, ci)), shape=(nv + nc, nv))
    bmid = [
        var_ids[v]
        for co in com.constraints
        for v in co.variables
        if co.name.startswith("objective_") and "reverse" not in v.name
    ]
    p_coef = [2 for i in bmid]
    P = csc_matrix((p_coef, (bmid, bmid)), shape=(nv, nv))
    q = np.zeros(nv)
    bounds = np.r_[var_bounds, const_bounds]
    co_i = var_ids[com.variables.community_objective]
    bounds[co_i, :] = (0.5 * com.slim_optimize(), np.infty)
    print(bounds[co_i, :])
    return (P, q, A, bounds[:, 0], bounds[:, 1])
