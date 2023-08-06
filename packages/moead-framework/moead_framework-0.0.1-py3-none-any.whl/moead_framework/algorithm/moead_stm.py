import random

import numpy as np

from moead_framework.algorithm import MoeadDRA


class MoeadSTM(MoeadDRA):

    def __init__(self, problem, max_evaluation, number_of_objective, number_of_weight, number_of_weight_neighborhood,
                 delta, number_of_replacement, number_of_crossover_points=2,
                 threshold_before_evaluate_subproblem_utility=30,
                 delta_threshold=0.001, debug=False, x_reference=None, y_reference=None,
                 weight_file=None):
        super().__init__(
            problem=problem,
            max_evaluation=max_evaluation,
            number_of_objective=number_of_objective,
            number_of_weight=number_of_weight,
            number_of_weight_neighborhood=number_of_weight_neighborhood,
            delta=delta,
            number_of_replacement=number_of_replacement,
            number_of_crossover_points=number_of_crossover_points,
            threshold_before_evaluate_subproblem_utility=threshold_before_evaluate_subproblem_utility,
            delta_threshold=delta_threshold,
            debug=debug,
            x_reference=x_reference,
            y_reference=y_reference,
            weight_file=weight_file
        )

        self.z_nad = self.init_z_nad()

    def run(self, g, checkpoint=None):
        self.init_checkpoint()

        current_eval = 0
        while current_eval < self.max_evaluation:

            # Step 2
            sub_problems = self.select_sub_problems()

            # Step 3
            pop_q = []
            for i in sub_problems:
                self.update_current_sub_problem(sub_problem=i)
                self.mating_pool = self.selection(sub_problem=i)[:]
                y = self.reproduction(population=self.mating_pool)
                y = self.repair(solution=y)
                pop_q.append(y)

                self.update_z(solution=y)
                self.update_z_nad(solution=y)

                current_eval += 1

            pop_r = self.population + [i for i in pop_q if i not in self.population]
            self.population = self.stm(pop_r, aggregation_function=g)

            # update the score history of all sub_problem
            # just before compute the utility of sub problems
            if ((self.gen + 1) % self.threshold_before_evaluate_subproblem_utility == 0) | (self.gen == 0):
                all_sub_problems = list(range(self.number_of_weight))
                for i in all_sub_problems:
                    score = g.run(solution=self.population[i],
                                  number_of_objective=self.number_of_objective,
                                  weights=self.weights,
                                  sub_problem=i,
                                  z=self.z)
                    self.update_scores(sub_problem=i, score=score)

            # Step 5
            self.gen += 1
            if self.gen % self.threshold_before_evaluate_subproblem_utility == 0:
                self.update_pi()

            if checkpoint is not None:
                checkpoint()

        self.final_checkpoint()

        return self.population

    def init_z_nad(self):
        z_nad = np.copy(self.z)

        for i in range(self.number_of_weight):
            for j in range(self.number_of_objective):
                f_j = self.population[i].F[j]

                if z_nad[j] < f_j:  # in minimisation context !
                    z_nad[j] = f_j

        return z_nad

    def update_z_nad(self, solution):
        for i in range(self.number_of_objective):
            if self.z_nad[i] < solution.F[i]:  # in minimisation context !
                self.z_nad[i] = solution.F[i]

    def stm(self, solution_set, aggregation_function):
        future_population = [None for x in range(self.number_of_weight)]
        fp = np.zeros(self.number_of_weight)
        fx = np.zeros(len(solution_set))
        mem = np.zeros((len(solution_set), self.number_of_weight))

        pref_of_solutions, pref_of_problems = self.compt_pref(solution_set=solution_set, g=aggregation_function)

        while not all(p == 1 for p in fp):
            problem_i = random.choice(np.array(np.where(fp == 0)).T)[0]
            preferences_of_problem = pref_of_problems[problem_i]

            solution_j = -1
            for j in preferences_of_problem:
                if mem[j][problem_i] == 0:
                    solution_j = j
                    break

            mem[solution_j][problem_i] = 1

            if fx[solution_j] == 0:
                # if solution_j is free
                future_population[problem_i] = solution_set[solution_j]
                fp[problem_i] = 1
                fx[solution_j] = 1
            else:
                # if solution_j is not free
                problem_k = self.get_problem_from_solution(future_population=future_population, x=solution_set[solution_j])
                rank_of_problem_i = pref_of_solutions[solution_j].index(problem_i)
                rank_of_problem_k = pref_of_solutions[solution_j].index(problem_k)

                if rank_of_problem_i < rank_of_problem_k:
                    # if the problem i (the new potential partner) is preferred instead of the problem k (the curr part)
                    future_population[problem_i] = solution_set[solution_j]
                    future_population[problem_k] = None
                    fp[problem_i] = 1
                    fp[problem_k] = 0

        return future_population

    def compt_pref(self, solution_set, g):
        m = len(solution_set)
        n = self.number_of_weight
        delta_p = np.zeros((n, m))
        delta_x = np.zeros((m, n))

        for i in range(m):
            for j in range(n):
                delta_p[j][i] = g.run(solution=solution_set[i],
                                      number_of_objective=self.number_of_objective,
                                      weights=self.weights,
                                      sub_problem=j,
                                      z=self.z)
                delta_x[i][j] = self.distance(solution_set[i], self.weights[j])

        pref_x = []
        pref_p = []
        for i in range(m):
            pref_x.append(sorted(range(len(delta_x[i])), key=lambda k: delta_x[i][k]))

        for i in range(n):
            pref_p.append(sorted(range(len(delta_p[i])), key=lambda k: delta_p[i][k]))

        return pref_x, pref_p

    def distance(self, solution, sub_problem):
        vec_ind = np.zeros(self.number_of_objective)
        vec_proj = np.zeros(self.number_of_objective)
        for i in range(self.number_of_objective):
            vec_ind[i] = (solution.F[i] - self.z[i]) / (self.z_nad[i] - self.z[i])

        scale = np.dot(vec_ind, sub_problem) / np.dot(sub_problem, sub_problem)

        for i in range(self.number_of_objective):
            vec_proj[i] = vec_ind[i] - scale * sub_problem[i]

        return np.linalg.norm(vec_proj)

    def get_problem_from_solution(self, future_population, x):
        for i in range(len(future_population)):
            if future_population[i] is not None:
                if np.array_equal(np.array(future_population[i].solution), np.array(x.solution)):
                    return i

        return -1
