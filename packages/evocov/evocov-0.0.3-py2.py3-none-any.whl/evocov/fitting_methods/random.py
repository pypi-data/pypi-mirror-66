# -*- coding: utf-8 -*-
#
#    Copyright 2020 Ibai Roman
#
#    This file is part of EvoCov.
#
#    EvoCov is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    EvoCov is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with EvoCov. If not, see <http://www.gnu.org/licenses/>.

import time

import numpy as np

import deap.gp
import deap.base
import deap.creator
import deap.algorithms

from gplib.fitting_methods.fitting_method import FittingMethod

from .. import primitive_set
from .. import creation


class Random(FittingMethod):
    """

    """

    def __init__(self, obj_fun, max_fun_call=500, dims=1,
                 nested_fit_method=None):

        self.obj_fun = obj_fun
        self.nested_fit_method = nested_fit_method
        self.max_fun_call = max_fun_call

        self.toolbox = deap.base.Toolbox()

        pset = primitive_set.get_primitive_set(
            arg_num=20
        )

        creation.add_creation(
            self.toolbox,
            pset,
            dims=dims,
            max_depth=30
        )

    def fit(self, model, folds, budget=None, verbose=False):
        """

        :param model:
        :type model:
        :param folds:
        :type folds:
        :param budget:
        :type budget:
        :param verbose:
        :type verbose:
        :return:
        :rtype:
        """
        if budget is None or self.max_fun_call < budget:
            max_fun_call = self.max_fun_call
        else:
            max_fun_call = budget

        start = time.time()

        log = {
            'name': self.__class__.__name__,
            'fun_calls': 0,
            'improvements': 0,
            'restarts': 0,
            'time': 0,
            'best': {
                'params': "",
                'value': np.inf,
                'fun_call': 0,
                'nested': None
            }
        }
        best_kernel = None

        while log['fun_calls'] < max_fun_call:
            individual = self.toolbox.RandomIndividual()

            # run optimization
            value = np.inf
            model.set_covariance_function(individual.covariance_function)
            try:
                if self.nested_fit_method is not None:
                    nested_log = self.nested_fit_method.fit(
                        model,
                        folds,
                        budget=(max_fun_call - log['fun_calls'] - 1),
                        verbose=verbose
                    )
                    log['fun_calls'] += (nested_log['fun_calls'])
                value = self.obj_fun(
                    model=model,
                    folds=folds,
                    grad_needed=False
                )
            except (AssertionError, np.linalg.linalg.LinAlgError) as ex:
                if verbose:
                    print(ex)

            log['fun_calls'] += 1
            log['restarts'] += 1
            if value < log['best']['value']:
                log['improvements'] += 1
                log['best']['params'] = str(individual)
                best_kernel = model.covariance_function
                log['best']['value'] = value
                log['best']['fun_call'] = log['fun_calls']
                if self.nested_fit_method is not None:
                    log['best']['nested'] = {
                        'name': self.nested_fit_method.__class__.__name__,
                        'fun_calls': nested_log['fun_calls'],
                        'improvements': nested_log['improvements'],
                        'restarts': nested_log['restarts'],
                        'time': nested_log['time'],
                        'best': {
                            'params' : nested_log['best']['params'],
                            'value' : nested_log['best']['value'],
                            'fun_call' : nested_log['best']['fun_call'],
                            'nested': nested_log['best']['nested']
                        }
                    }

        end = time.time()

        log['time'] = end - start

        assert best_kernel, "No kernel found"

        model.set_covariance_function(best_kernel)

        return log
