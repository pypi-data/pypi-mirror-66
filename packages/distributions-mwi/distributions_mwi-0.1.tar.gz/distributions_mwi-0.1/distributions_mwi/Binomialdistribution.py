from .Generaldistribution import Distribution
import matplotlib.pyplot as plt
import math

class Binomial(Distribution):

    def __init__(self, prob=.5, size=20):
        """ Binomial distribution class for calculating and 
        visualizing a Binomial distribution.
    
        Attributes:
            mean (float): representing the mean value of the distribution
            stdev (float): representing the standard deviation of the 
            distribution
            data_list (list of floats): a list of floats to be extracted from 
            the data file
            p (float): representing the probability of an event occurring
            n (int): the number of trials    
        """

        self.p = prob
        self.n = size
        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()
        self.data = []
    

    def calculate_mean(self):
        """Function to calculate the mean of the Binomial distribution

        Args:
            None
        
        Returns:
            float: mean of the Binomial distribution
        """

        self.mean = self.p * self.n

        return self.mean

    
    def calculate_stdev(self):
        """Function to calculate the standard deviation of the Binomial 
        distribution

        Args:
            None
        
        Returns:
            float: standard deviation of the Binomial distribution
        """

        self.stdev = math.sqrt( self.n * self.p * (1 - self.p) )

        return self.stdev


    def read_data(self, file_name):
        """Function to read in data from a txt file. The text file should have
        one number (float) per line. The numbers are stored in the data 
        attribute.

        Args:
            file_name (str): name of a file to read from
                
        Returns:
            None
        """

        Distribution.read_data(self, file_name)
        self.replace_stats_with_data()


    def replace_stats_with_data(self):
        """Function to update the distribution parameters based on a provided
        dataset

        Args:
            None

        Returns:
            None
        """
        
        self.n = len(self.data)
        self.p = sum(self.data) / len(self.data)

        self.calculate_mean()
        self.calculate_stdev()

    
    def plot_bar(self):
        """Function to output a histogram of the values from the data attribute
        
        Args:
            None
            
        Returns:
            None
        """

        x = [0, 1]
        height = [len(self.data) - sum(self.data), sum(self.data)]
        plt.bar(x, height)
        plt.title('Histogram of values')
        plt.xlabel('values')
        plt.ylabel('count')
        plt.xticks(x)
        plt.show()
    

    def pdf(self, k):
        """Probability density function calculator for the Binomial 
        distribution.
        
        Args:
            k (float): point for calculating the probability density function
            
        
        Returns:
            float: probability density function output
        """

        n = self.n
        p = self.p

        return math.comb(n, k) * (p ** k) * ((1 - p) ** (n-k))


    def plot_bar_pdf(self):
        """Function to plot the pdf of the binomial distribution
        
        Args:
            None
        
        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot  
        """

        x, y = [], []

        for k in range(self.n+1):
            x.append(k)
            y.append(self.pdf(k))
        
        plt.plot(x, y)
        plt.title(self.__repr__())
        plt.xlabel('k')
        plt.ylabel('prob')
        plt.show()

        return x, y


    def __add__(self, other):
        """Function to add together two Binomial distributions with equal p
        
        Args:
            other (Binomial): Binomial instance
            
        Returns:
            Binomial: Binomial distribution  
        """

        try:
            assert self.p == other.p, 'p values are not equal'
        except AssertionError as error:
            raise

        return Binomial(self.p, self.n + other.n)
    

    def __repr__(self):
        """Function to output the characteristics of the Binomial instance
        
        Args:
            None
        
        Returns:
            string: characteristics of the Binomial
        """

        return "Binomial(p={:.2f}, n={:.2f})".format(self.p, self.n)