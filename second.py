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
        for index in range(len(items)):
            before = sum(item[1] for item in items[:index + 1])
            after = sum(item[1] for item in items[index + 1:])
            if before >= 0.5 and after >= 0.5:
                return items[index]


if __name__ == '__main__':
    ksi = {index: i(1) / 6 for index in range(1, 6 + 1)}
    mu = {index: i(1) / 12 for index in range(1, 6 + 1)}
    mu[3] = i(1)/3
    mu[4] = i(1)/3

    theta = lambda ks, mu:  ks**mu - mu**ks
    another = lambda ks, mu: min(2 ** ks, mu) # КН-302

    one = DrvProblem.get_destribution_law(ksi, mu, theta)
    other = DrvProblem.get_destribution_law(ksi, mu, another)
    
    one_expectation = DrvProblem.get_expectation(one)
    other_expectation = DrvProblem.get_expectation(other)

    covariance_func = lambda xi, mu: (theta(xi, mu) - one_expectation) * (another(xi, mu) - other_expectation)
    covariance_destribution = DrvProblem.get_destribution_law(one, other, covariance_func)
    covariance = DrvProblem.get_expectation(covariance_destribution)


    #print('===Распределение theta===\nlambda ks, mu:  ks**mu - mu**ks', '\n')
    #print('===Закон распределения theta===')
    #print(DrvProblem.get_as_string(one), '\n')
    #print('===Матожидание theta===')
    #print(one_expectation, '\n')
    #print('===Дисперсия theta===')
    #print(DrvProblem.get_dispersion(one), '\n')
    #print('(a)===Медиана theta===')
    #print(DrvProblem.get_median(one), '\n')
    #print('(b)===Среднеквадратичное отклонение===')
    #print(DrvProblem.get_standard_deviation(one), '\n')

    #print('===Распределение another===\nlambda ks, mu: max(ks + mu, 2 * mu)', '\n')
    #print('===Матожидание another===')
    #print(other_expectation, '\n')
    #print('===Ковариция theta и another===')
    #print(covariance)
    ##print('===Корреляция theta и another===')
    ##print(DrvProblem.get_correlation(one, other))

