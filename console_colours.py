class ConProgress(object):
    HEADER = '\033[95m'
    blue = '\033[94m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    normal = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def __init__(self, steps):
        self.steps = float(steps)

    def percentage(self, x):
        return (float(x/self.steps) * 100)

    def progress(self, x):
        temp_per = self.percentage(x)
        temp_print= "  X:{}%".format(temp_per)
        if temp_per < 25:
            print (ConProgress.red + temp_print + ConProgress.normal)
        elif temp_per < 50:
            print (ConProgress.yellow + temp_print + ConProgress.normal)
        elif temp_per < 75:
            print (ConProgress.blue + temp_print + ConProgress.normal)
        elif temp_per < 100:
            print (ConProgress.green + ConProgress.BOLD + temp_print + ConProgress.normal)


if __name__ == '__main__':
    steps = 100
    x = 0
    progress = ConProgress(100)

    while x < steps:
        progress.progress(x)
        x+=1
