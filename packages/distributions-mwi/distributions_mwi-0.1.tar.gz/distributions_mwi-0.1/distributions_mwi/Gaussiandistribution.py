from .Generaldistribution import Distribution
import math
import matplotlib.pyplot as plt

class Gaussian(Distribution):

    def __init__(self, mu=0, sigma=1):
        """Gaussian distribution class for calculating and visualizing a
        Gaussian distribution.

        Attributes:
            mean (float): representing the mean of the distribution
            stdev (float): representing the standard deviation of the 
                distribution
            data (list of floats): a list of float extracted from a data file
        """

        Distribution.__init__(self, mu, sigma)


    def calculate_mean(self):
        """Function to calculate the mean of the data set.
        
        Args: 
            None
        
        Returns: 
            float: mean of the data set
        """
        
        mu = sum(self.data) / len(self.data)

        self.mean = mu
        
        return self.mean


    def calculate_stdev(self, sample=True):
        """Function to calculate the standard deviation of the data set.
        
        Args: 
            sample (bool): whether the data represents a sample or population
        
        Returns: 
            float: standard deviation of the data set
        """

        if sample==True:
            n = len(self.data) - 1
        else:
            n = len(self.data)
        
        mu = self.mean
        sigma = 0

        for x in self.data:
            sigma += (x - mu) ** 2
        
        sigma = math.sqrt(1/n * sigma)

        self.stdev = sigma


    def read_data(self, file_name, sample=True):
        """ Function to read in data from a txt file. The text file should have
        one number (float) per line. The numbers are stored in the data 
        attribute.

        Args:
            file_name (str): name of a file to read from
            sample (bool): whether the data represents a sample or population
        
        Returns:
            None
        """

        Distribution.read_data(self, file_name)
        self.calculate_mean()
        self.calculate_stdev(sample)
    

    def plot_histogram(self):
        """Function to output a histogram of the instance variable data using 
        matplotlib pyplot library.
        
        Args:
            None
            
        Returns:
            None
        """

        plt.hist(self.data)
        plt.title('Histogram of values')
        plt.xlabel('value')
        plt.ylabel('count')
        plt.show()
        
        
    def pdf(self, x):
        """Probability density function calculator for the gaussian 
        distribution.
        
        Args:
            x (float): point for calculating the probability density function
            
        
        Returns:
            float: probability density function output
        """
        
        sigma = self.stdev
        mu = self.mean

        return (1.0 / (sigma * math.sqrt(2*math.pi))) * \
            math.exp(-0.5*((x - mu) / sigma) ** 2)
        
    
    def plot_histogram_pdf(self, n_spaces = 50):
        """Function to plot the normalized histogram of the data and a plot of 
        the probability density function along the same range.
        
        Args:
            n_spaces (int): number of data points 
        
        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot
        """

        sigma = self.stdev
        mu = self.mean

        min_range = min(self.data)
        max_range = max(self.data)
        interval = (max_range - min_range) / n_spaces

        x, y = [], []

        for i in range(n_spaces):
            tmp = min_range + i*interval
            x.append(tmp)
            y.append(self.pdf(tmp))
        
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
        fig.subplots_adjust(hspace=.5)
        ax1.set_title('Normed histogram of values')
        ax1.set_ylabel('density')
        ax1.hist(self.data, density=True)

        ax2.set_title('Normal distribution for mu={:.2f} and sigma={:.2f}'\
            .format(mu, sigma))
        ax2.set_ylabel('density')
        ax2.plot(x, y)
        plt.show()

        return x, y


    def __add__(self, other):
        """Function to add together two Gaussian distributions

        Args:
            other (Gaussian): Gaussian instance
        
        Returns:
            Gaussian: Gaussian distribution
        """

        result = Gaussian()
        result.mean = self.mean + other.mean
        result.stdev = math.sqrt(self.stdev ** 2 + other.stdev ** 2)

        return result
    
    
    def __repr__(self):
        """Function for representation of a Gaussian instance

        Args:
            None
        
        Returns:
            str: representation of Gaussian instance
        """

        return "Gaussian(mu={:.2f}, sigma={:.2f})".format(self.mean, self.stdev)