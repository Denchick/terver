from collections import defaultdict
from sympy import Integer as i
import matplotlib.pyplot as plt

class DrvProblem:
    @staticmethod
    def get_destribution_law(ksi_destr_law, mu_destr_law, theta_function):
        theta_destr_law = defaultdict(int)
        for ksi in ksi_destr_law :
            for mu in mu_destr_law:
                value = theta_function(ksi, mu)
                probability = ksi_destr_law[ksi] * mu_destr_law[mu]
                theta_destr_law[value] += probability
        return theta_destr_law


    @staticmethod
    def create_destribution_law(probabilities):
        return {i + 1: probabilities[i] for i in range(len(probabilities))}

    @staticmethod
    def get_as_string(destribution_law):
        result = []
        for value in sorted(destribution_law.keys()):
            result.append(f'{value} => {destribution_law[value]}')
        result.append(f'Всего {len(destribution_law)} записей.\n')

        return '\n'.join(result)

    @staticmethod
    def get_expectation(destribution_law):
        return sum(value * destribution_law[value] for value in destribution_law)

    @staticmethod
    def get_dispersion(destribution_law):
        expectation = DrvProblem.get_expectation(destribution_law)
        return sum(destribution_law[value] * ((value - expectation) ** 2) for value in destribution_law)

    @staticmethod
    def get_standard_deviation(destribution_law):
        return DrvProblem.get_dispersion(destribution_law)**0.5

    @staticmethod
    def get_median(destribution_law):
        items = sorted(destribution_law.items(), key=lambda item: item[0])
        for i in range(len(items) - 1):
            before = sum(item[1] for item in items[:i + 1])
            after = sum(item[1] for item in items[i:])
            if before >= 0.5 and after >= 0.5:
                return items[i][0]


        #items = sorted(destribution_law.items(), key=lambda item: item[0])
        #for index in range(len(items)):
        #    before = sum(item[1] for item in items[:index + 1])
        #    after = sum(item[1] for item in items[index + 1:])
        #    if before >= 0.5 and after >= 0.5:
        #        return items[index]


if __name__ == '__main__':
    ksi = {index: i(1) / 6 for index in range(1, 6 + 1)}
    mu = {index: i(1) / 12 for index in range(1, 6 + 1)}
    mu[3] = i(1)/3
    mu[4] = i(1)/3

    one = lambda ks, mu: ks ** mu - mu ** ks
    other = lambda ks, mu: max(ks + mu, 2 * mu)

    one_destribution_law = DrvProblem.get_destribution_law(ksi, mu, one)
    other_destribution_law = DrvProblem.get_destribution_law(ksi, mu, other)
    
    one_expectation = DrvProblem.get_expectation(one_destribution_law)
    other_expectation = DrvProblem.get_expectation(other_destribution_law)

    one_dispersion = DrvProblem.get_dispersion(one_destribution_law)
    other_dispersion = DrvProblem.get_dispersion(other_destribution_law)

    covariance_func = lambda ks, mu: (one(ks, mu) - one_expectation) * (other(ks, mu) - other_expectation)
    covariance_destribution = DrvProblem.get_destribution_law(ksi, mu, covariance_func)
    covariance = DrvProblem.get_expectation(covariance_destribution)

    correlation = covariance / (one_dispersion * other_dispersion)**0.5


    print('===Мое распределение===\nlambda ks, mu:  ks**mu - mu**ks', '\n')
    print('(a)===Медиана===')
    print(DrvProblem.get_median(one_destribution_law), '\n')
    print('(b)===Среднеквадратичное отклонение===')
    print(DrvProblem.get_standard_deviation(one_destribution_law), '\n')
    print('===Другое распределение===\nlambda ks, mu: max(ks + mu, 2 * mu)', '\n')
    print('===Их ковариция===')
    print(covariance, '\n')
    print('===Их корреляция===')
    print(correlation)
