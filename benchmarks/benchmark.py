import time


def benchmark(f, n=1000, args=(), name=None):
    """ Custom benchmark function. Times how long f takes to complete n times and prints the average """
    # get the start time. time.perf_counter() returns the value of "a clock with the highest available resolution to measure a short duration"
    start_time = time.perf_counter()
    # call the function n times which the arguments
    for i in range(n):
        f(*args)
    # get the end time
    end_time = time.perf_counter()
    # get the delta time in milliseconds
    delta_ms = (end_time - start_time) * 1000
    # calculate average time in milliseconds
    average_ms = delta_ms / n
    # the name to be printed can be provided as a parameter or got from the function's name
    if name is None:
        name = f.__name__
    # print the name, left aligned within 40 characters and then the time right aligned within 8 characters
    print("{:<40} - {:>8.4f}ms".format(name, average_ms))
