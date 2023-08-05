import numpy as np

from scipy.signal import argrelextrema
from joblib import Parallel, delayed

from pge.ranks.extrem_onl import NodeExInfo


class WayEx(NodeExInfo):
    @staticmethod
    def get_ex(gr, root, frm):
        paths, di = gr.get_short_pathes(root)
        xs, lv = gr.get_ln_attrs(frm, paths)
        return WayEx.estimate(xs, lv), np.max(di), np.sum(di)

    @staticmethod
    def get_exes(gr, root, params):
        paths, di = gr.get_short_pathes(root)
        res = []
        for params_ in params:
            xs, lv = gr.get_ln_attrs(params_[0], paths)
            ex1, ex2 = WayEx.estimate(xs, lv)
            res.append((ex1, ex2, params_[1]))
        return res, np.max(di), np.sum(di)

    @staticmethod
    def estimate(xs, lv):
        exes = []

        for t1 in [
            True,
            False
        ]:
            if t1:
                res = np.array(Parallel(n_jobs=2, backend="multiprocessing")(delayed(WayEx.ex_estimate)(xs, u,
                                                                                                        t1) for u in
                                                                             lv))
                ind = np.sort(np.append(argrelextrema(res, np.less), argrelextrema(res, np.greater)))
                if ind.size == 0:
                    exes.append(0)
                else:
                    res = np.sort(res[ind])
                    exes.append(np.mean(res[res.size - 2:]))
            else:
                ex = 1
                for u in lv[::-1]:
                    ex_ = WayEx.ex_estimate(xs, u, t1)
                    if ex_ < ex:
                        ex = ex_
                        break
                    ex = ex_
                exes.append(ex)
        return exes[0], exes[1]

    @staticmethod
    def ex_estimate(xs, lv, t1):
        ts = np.array([])
        for xs_ in xs:
            if t1:
                ts_ = np.where(xs_ > lv)[0]
            else:
                ts_ = np.where(xs_ <= lv)[0]

            if ts_.size > 1:
                ts = np.append(ts, np.diff(ts_))

        if ts.size == 0:
            return 1

        if np.max(ts) > 2:
            return min([1, 2 * np.sum(ts - 1) ** 2 / (ts.size * np.sum(np.multiply(ts - 1, ts - 2)))])
        else:
            return min([1, 2 * np.sum(ts) ** 2 / (ts.size * np.sum(ts ** 2))])

    @staticmethod
    def get_ex_comm(gr, nodes, frm, part=True):
        if part:
            sub = gr.subfraph(nodes)
        else:
            sub = gr

        pathes = sub.get_all_short_pathes(nodes)[0]
        xs, lv = gr.get_ln_attrs(frm, pathes)
        return WayEx.estimate(xs, lv)

    @staticmethod
    def get_exes_comm(gr, nodes, params, part=True):
        if part:
            sub = gr.subgraph(nodes)
        else:
            sub = gr

        pathes = sub.get_all_short_pathes(nodes)[0]
        res = []
        for params_ in params:
            xs, lv = gr.get_ln_attrs(params_[0], pathes)
            ex1, ex2 = WayEx.estimate(xs, lv)
            res.append((ex1, ex2, params_[1]))
        return res
