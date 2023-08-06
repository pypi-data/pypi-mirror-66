# -----------------------------------------------------------------
# -----------------------------------------------------------------
#
#  Mandrake lib (mlib) for displaying ASCII progress bars
#
# -----------------------------------------------------------------
# -----------------------------------------------------------------

import progressbar as PROG


# Wrapper for progress bar with nice default options:
# bar = mlib.progressbar.ProgressBar(maxval = 120)
# bar.start()
# bar.update(current_value)
# bar.finish()
def ProgressBar(maxval=None):
    widgets = [PROG.Bar(), ' ', PROG.Counter(), " = ", PROG.Percentage(), ' ', PROG.ETA(), ' ', PROG.Timer()]
    return PROG.ProgressBar(widgets=widgets, max_value=maxval)


def bar_nospam(iterative, maxval=None, enum=False):
    """A very nice wrapper to progressbar that only writes out occasional updates to the progressbar.
    This prevents a bar spanning millions of entries updating the screen millions of times, generated GB of logfiles.

    maxval: sets the total number of iterations upon which to base the bar (default: len(iterative))
    enum  : don't just yield the iterative elements but also the enumerated count as per the enumerate() wrapper

    TODO: Rename local module to some other than globally installed
          "progressbar" name as local module takes precedence.
    >>> values = bar_nospam(range(0, 3))
    >>> for each in values:
    ...     print(each)
    0
    1
    2
    >>> values = bar_nospam(range(0, 3), enum=True)
    >>> for each in values:
    ...     print(each)
    (0, 0)
    (1, 1)
    (2, 2)
    """

    if maxval is None: maxval = len(iterative)

    # Now figure out how often to update the bar
    # This is done to prevent multi-Gig log files containing millions of bar updates

    NUM_FULL_RES = 200
    NUM_STEPS = float(1000)

    # First NUM_FULL_RES iterations are automatically included fully
    update_iterations = list(range(NUM_FULL_RES))
    # Second, sub-sample remaining iterations to ensure only NUM_STEPS more updates max
    update_iterations += list(range(NUM_FULL_RES, maxval, max(1, int((maxval - NUM_FULL_RES) / NUM_STEPS))))

    # Construct bar
    bar = ProgressBar(maxval)
    bar.start()

    # Walk the list of iterables, updating bar when appropriate
    for c, item in enumerate(iterative):
        if (len(update_iterations)) > 0 and (c == update_iterations[0]):
            bar.update(c)
            update_iterations.pop(0)
        if enum:
            yield c, item
        else:
            yield item

    bar.finish()
    print

if __name__ == "__main__":
    import doctest
    import numpy as N

    N.set_printoptions(linewidth=130, legacy='1.13')
    doctest.testmod()
