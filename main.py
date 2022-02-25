# Used in Frequency Table
import pandas as pd

# Used in variance
import copy

# Used in standard deviation
from math import sqrt


class Statistics:
    def __init__(self, data):
        if type(data) != list:
            raise ValueError("Datatype has to be a list")

        if len(data) < 2:
            raise TypeError("Data set has to have at least 2 data points")

        self.data = data
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

        frequencies = [0 for _ in range(num_classes)]

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
        return sum(self.data) / len(self.data)

    def mode(self):
        """
        :return: Returns a list of all the highest frequency items.
        """
        # First we count the frequency of our data
        freq = {}
        for i in self.data:

            try:
                freq[i] += 1
            except KeyError:
                freq[i] = 1

        highest_freq = 0
        value = []

        for key, item in freq.items():
            if item == highest_freq:
                highest_freq = item
                value.append(key)
            elif item > highest_freq:
                value = [key]
                highest_freq = item
        if len(value) == len(self.data):
            return "This Data set does not have mode"
        return value[0] if len(value) == 1 else value

    def median(self):
        # First sort our data, then get the middle point
        new_array = sorted(self.data)
        middle_point = int(len(self.data) / 2)

        if len(self.data) % 2 == 0:
            return (new_array[middle_point] + new_array[middle_point - 1]) / 2
        else:
            return new_array[middle_point]

    def hildebrand_rule(self):
        """
        :return: This function returns true or false based on whether the data is symmetrical enough
        """
        ratio = (self.mean(-1) - self.median()) / self.standard_deviation(self.data)
        return True if abs(ratio) < 0.2 else False

    def variance(self, sample=False):
        data = copy.deepcopy(self.data)
        mean = self.mean()

        var = 1 if sample else 0

        return sum(list(map(lambda x: (x - mean) ** 2, data))) / (len(data) - var)

    def standard_deviation(self, sample=False):
        return sqrt(self.variance(sample=sample))

    def coeffiecient_of_variation(self, sample=False):
        return self.standard_deviation(sample=sample) / self.mean()

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

        sorted_data = sorted(self.data)

        if len(self.data) % 2 == 0:
            middle_point, upper_point = len(self.data) / 2, len(self.data) / 2
        else:
            middle_point, upper_point = len(self.data) / 2, len(self.data) / 2 + 1

        middle_point, upper_point = int(middle_point), int(upper_point)

        minn = min(self.data)
        q1 = Statistics(sorted_data[:middle_point]).median()
        med = self.median()
        q3 = Statistics(sorted_data[upper_point:]).median()
        maxx = max(self.data)

        return[minn, q1, med, q3, maxx]

    def z_score(self, value, sample=False):
        """
        Calculate the Z scores
        :return: the score
        """
        return (value - self.mean()) / self.standard_deviation(sample=sample)

    def describe_set(self):
        """
        This functions purpose is to describe the dataset to us by calculating all the different
        features of that data set. It prints all the values to console.
        """
        print(f"Length of the set: {len(self.data)}\n")
        print(f"Mean: {self.mean()}")
        print(f"Median: {self.median()}")
        print(f"Mode: {self.mode()}\n")
        print(f"Variance: {round(self.variance(), 2)}")
        print(f"Standard Deviation: {round(self.standard_deviation(), 2)}")
        print(f"Coefficient of Variance: {round(self.coeffiecient_of_variation(), 2)}\n")
        print(f"Five number summary: {self.five_number_summary()}")

    def __repr__(self):
        if len(self.data) < 11:
            return f"Statistics[{self.data}]"
        else:
            return f"Statistics[{self.data[0]}, {self.data[1]}, ... {self.data[-2]}, {self.data[-1]}]"

    def __add__(self, obj):
        if type(obj) == list:
            return Statistics(self.data + obj)
        elif type(obj) == Statistics:
            return Statistics(self.data + obj.data)
        else:
            raise TypeError(f"Type has to be list or Statistics, not {type(obj)}")
