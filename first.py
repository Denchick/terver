from collections import defaultdict
from sympy import Integer as i
import matplotlib.pyplot as plt

class DrvProblem:
    def __init__(self, ksi_probabilities, mu_probabilities, theta_function):
        self.theta_function = theta_function
        self.ksi_destr_law = self.create_destribution_law(ksi_probabilities)
        self.mu_destr_law = self.create_destribution_law(mu_probabilities)
        self.theta_destr_law = defaultdict(int)
        self.calc_theta_destribution_law()

    @staticmethod
    def create_destribution_law(probabilities):
        return {i + 1: probabilities[i] for i in range(len(probabilities))}

    def calc_theta_destribution_law(self):
        for ksi in self.ksi_destr_law :
            for mu in self.mu_destr_law:
                value = self.theta_function(ksi, mu)
                probability = self.ksi_destr_law[ksi] * self.mu_destr_law[mu]
                self.theta_destr_law[value] += probability

    def get_as_string(self, destribution_law):
        result = []
        for value in sorted(destribution_law.keys()):
            result.append(f'{value} => {destribution_law[value]}')
        result.append(f'Всего {len(destribution_law)} записей.\n')

        return '\n'.join(result)

    def get_expectation(self, destribution_law):
        return sum(value * destribution_law[value] for value in destribution_law)

    def get_dispersion(self, destribution_law):
        # squared_law = {i**2: destribution_law[i]**2 for i in destribution_law}
        # return self.get_expectation(squared_law) - self.get_expectation(destribution_law)**2
        expectation = self.get_expectation(destribution_law)
        return sum(destribution_law[value] * ((value - expectation) ** 2) for value in destribution_law)

    def get_prefix_sum(self, destribution_law):
        summa = 0
        result = []
        for key in sorted(destribution_law.keys()):
            summa += destribution_law[key]
            result.append(summa)
        return result

    def get_prepared_data_for_plot(self, events, prefix_sums):
        data = []
        for i in range(0, len(events) - 1):
            data.extend([(events[i], events[i + 1]), (prefix_sums[i + 1], prefix_sums[i + 1]), 'green'])
        return data

    def create_destribution_law_plot(self, destribution_law):
        events = sorted(destribution_law.keys())
        prefix_sums = self.get_prefix_sum(destribution_law)

        plt.title('Функция распределения theta')
        plt.xlabel("Событие theta")
        plt.ylabel("Вероятность события theta")
        plt.grid(True)
        plt.arrow(events[0], 0, -1000, 0)
        
        plt.scatter(events, prefix_sums, c='green', marker='.')
        plt.plot(*self.get_prepared_data_for_plot(events, prefix_sums))

        plt.show()



if __name__ == '__main__':
    ksi = [i(1)/6] * 6
    mu = [i(1)/12, i(1)/12, i(1)/3, i(1)/3, i(1)/12,i(1)/12]
    theta = lambda ks, mu:  ks**mu - mu**ks
    result = DrvProblem(ksi, mu, theta)

    print('===Закон распределения theta===')
    print(result.get_as_string(result.theta_destr_law))
    print('===Матожидание theta===')
    print(result.get_expectation(result.theta_destr_law), '\n')
    print('===Дисперсия theta===')
    print(result.get_dispersion(result.theta_destr_law))
    result.create_destribution_law_plot(result.theta_destr_law)

