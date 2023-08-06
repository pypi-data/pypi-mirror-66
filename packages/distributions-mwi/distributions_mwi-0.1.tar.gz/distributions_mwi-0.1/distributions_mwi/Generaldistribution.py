class Distribution():

    def __init__(self, mu=0, sigma=1):
        """ Generic distribution class for calculating and visualizing a
        probability distribution 

        Attributes:
            mean (float): representing the mean of the distribution
            stdev (float): representing the standard deviation of the 
                distribution
            data (list of floats): a list of float extracted from a data file
        """

        self.mean = mu
        self.stdev = sigma
        self.data = []
   
    
    def read_data(self, file_name):
        """ Function to read in data from a txt file. The text file should have
        one number (float) per line. The numbers are stored in the data 
        attribute.

        Args:
            file_name (str): name of a file to read from
        
        Returns:
            None
        """

        with open(file_name, 'r') as file:
            data = []
            line = file.readline()
            while line:
                data.append(float(line))
                line = file.readline()
            
        self.data = data