PLOT_DPI = 100

# Backend to use for plotting.  After using the bt library, which somehow changes the
# backend to 'agg' it raises an error.  Set this to avoid.
"""
More information:
https://matplotlib.org/stable/tutorials/introductory/usage.html#the-builtin-backends

Common ones:
module://backend_interagg   : This is what pycharm defaults to in Scientific Mode
MacOSX   : Mac default.  Does not work with backtesting
tkAgg : This uses the tkinter library.
Qt5Agg  : This requires the PyQt5 package is installed
"""
backend = None

# Used when USE_PLOT_AUTOSCALING is set to False
PLOT_HEIGHT = 500
PLOT_WIDTH = 800

# Used when USE_PLOT_AUTOSCALING is set to True
PLOT_HEIGHT_PERCENTAGE = 50
PLOT_WIDTH_PERCENTAGE = 70

# When autoscaling is True, choose which monitor to scale to
# Primary monitor = 0, secondary monitor use 1
MONITOR = 0
