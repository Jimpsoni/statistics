import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import copy
import math


class Statistics:
    def __init__(self, data):
        self.data = np.array(data)
        pd.set_option("display.max_rows", None, "display.max_columns", None)

    def frequency_table(self, num_classes=None, min_value=None, max_value=None, round_to=2):
        """
        :param num_classes: Number of classes we want to have
        :param min_value: Value we start from
        :param max_value: Value we stop to
        :param round_to: How many decimal places we want the values in table to have
        :return: Returns a Pandas dataframe that represents the frequency table
        """

        # First we calculate the class width and initialize our freq table
        class_width = (max_value - min_value) / num_classes
        freq_table = pd.DataFrame()

        # Make a list of classes
        classes = [min_value + (i * class_width) for i in range(num_classes)]

        # Update our frequency table
        freq_table.index = classes
        freq_table.index.name = "Classes"

        # Next up, we want to go through every value in our data and
        # determine in which class it goes
        frequencies = np.zeros(num_classes)

        for value in self.data:
            for index, item in enumerate(classes):
                if item <= value < item + class_width:
                    frequencies[index] += 1
                    continue
        # update our frequency table
        freq_table['Frequencies'] = frequencies

        # Make the relative frequencies in our table
        freq_table['Relative frequencies'] = round(freq_table['Frequencies'] / len(self.data), round_to) * 100

        # Make the cumulative sum
        freq_table['Cumulative Sum'] = freq_table['Frequencies'].cumsum()

        return freq_table

    def mean(self, round_to=2):
        """
        :param round_to: How many decimal places we want to have, if set to -1, doesn't round at all
        :return: mean of the dataset
        """
        if round_to != -1:
            return round(self.data.mean(), round_to)
        else:
            return self.data.mean()

    def mode(self):
        return None

    def median(self):
        return np.median(self.data)

    def hildebrand_rule(self):
        """
        :return: This function returns true or false based on whether the data is symmetrical enough
        """
        ratio = (self.mean(-1) - self.median()) / np.std(self.data)
        print(ratio)
        return True if abs(ratio) < 0.2 else False

    def variance(self, sample_variance=False):
        data = copy.deepcopy(self.data)
        mean = self.mean()

        var = 1 if sample_variance else 0

        return np.sum(list(map(lambda x: (x - mean) ** 2, data))) / (len(data) - var)

    def standard_deviation(self, sample_std=False):
        if sample_std:
            return self.data.std()
        else:
            return self.data.std(ddof=1)

    def coeffiecient_of_variation(self, sample=False):
        if sample:
            return self.data.std(ddof=1) / self.data.mean()
        else:
            return self.data.std() / self.data.mean()

    @staticmethod
    def chebyshevs_theorem(k):
        """
        :param k: The number of stds we want to estimate
        :return: Percentage of data that lies between k number of standard deviations
        """
        return str(round((1 - (1 / k ** 2)) * 100, 2)) + "%"

    def five_number_summary(self):
        """
        Calculate, min, Q1, Median, Q3 and Max
        :return: list of them all in that order
        """

        sorted_data = np.sort(self.data)

        minn = min(self.data)
        q1 = sorted_data[int(math.floor(len(sorted_data) * 0.25))]
        med = np.median(self.data)
        q3 = sorted_data[int(math.floor(len(sorted_data) * 0.75))]
        maxx = max(self.data)

        return[minn, q1, med, q3, maxx]

    def z_score(self, value, sample=False):
        """
        Calculate the Z scores
        :return: the score
        """
        if sample:
            return (value - self.data.mean()) / self.data.std()
        else:
            return (value - self.data.mean()) / self.data.std(ddof=1)
