
class Result:

    def __init__(self):
        self.beta_hat = None
        self.y = None
        self.x = None
        self.coefficient = None
        self.residual = None
        self.y_name = None
        self.x_name = None

    def summary(self, tol=3):
        print('The coefficients are: ')
        for name, value in zip(self.x_name, self.coefficient):
            print('%20s%10.4f' % (name, value))
