class Quantity_Date(object):
    Month = ""
    Year = ""
    Topics = []

    # The class "constructor" - It's actually an initializer 
    def __init__(self, month, year,no_topics):
        self.Month = month
        self.Year = year    
        self.Topics = [0] * no_topics