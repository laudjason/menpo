from collections import deque
from datetime import datetime
import sys
from time import time


def progress_bar_str(percentage, bar_length=20, bar_marker='=', show_bar=True):
    r"""
    Returns an `str` of the specified progress percentage. The percentage is
    represented either in the form of a progress bar or in the form of a
    percentage number. It can be combined with the :func:`print_dynamic`
    function.

    Parameters
    ----------
    percentage : `float`
        The progress percentage to be printed. It must be in the range
        ``[0, 1]``.
    bar_length : `int`, optional
        Defines the length of the bar in characters.
    bar_marker : `str`, optional
        Defines the marker character that will be used to fill the bar.
    show_bar : `bool`, optional
        If ``True``, the `str` includes the bar followed by the percentage,
        e.g. ``'[=====     ] 50%'``

        If ``False``, the `str` includes only the percentage,
        e.g. ``'50%'``

    Returns
    -------
    progress_str : `str`
        The progress percentage string that can be printed.

    Raises
    ------
    ValueError
        ``percentage`` is not in the range ``[0, 1]``
    ValueError
        ``bar_length`` must be an integer >= ``1``
    ValueError
        ``bar_marker`` must be a string of length 1

    Examples
    --------
    This for loop: ::

        n_iters = 2000
        for k in range(n_iters):
            print_dynamic(progress_bar_str(float(k) / (n_iters-1)))

    prints a progress bar of the form: ::

        [=============       ] 68%
    """
    if percentage < 0:
        raise ValueError("percentage is not in the range [0, 1]")
    elif percentage > 1:
        percentage = 1
    if not isinstance(bar_length, int) or bar_length < 1:
        raise ValueError("bar_length must be an integer >= 1")
    if not isinstance(bar_marker, str) or len(bar_marker) != 1:
        raise ValueError("bar_marker must be a string of length 1")
    # generate output string
    if show_bar:
        str_param = "[%-" + str(bar_length) + "s] %d%%"
        bar_percentage = int(percentage * bar_length)
        return str_param % (bar_marker * bar_percentage, percentage * 100)
    else:
        return "%d%%" % (percentage * 100)


def print_dynamic(str_to_print):
    r"""
    Prints dynamically the provided `str`, i.e. the `str` is printed and then
    the buffer gets flushed.

    Parameters
    ----------
    str_to_print : `str`
        The string to print.
    """
    sys.stdout.write("\r%s" % str_to_print)
    sys.stdout.flush()


def print_bytes(num):
    r"""
    Converts bytes to a sensible format to be printed. For example: ::

        print_bytes(12345) returns '12.06 KB'
        print_bytes(123456789) returns '117.74 MB'

    Parameters
    ----------
    num : `int`
        The size in bytes.

    Raises
    ------
    ValueError
        num must be int >= 0
    """
    if not isinstance(num, int) or num < 0:
        raise ValueError("num must be int >= 0")
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "{0:3.2f} {1:s}".format(num, x)
        num /= 1024.0
    return "{0:3.2f} {1:s}".format(num, 'TB')


def print_progress(iterable, n_items=None):
    r"""
    Print the remaining time needed to compute over an iterable.

    To use, wrap an existing iterable with this function before processing in
    a for loop (see example).

    The estimate of the remaining time is based on a moving average of the last
    100 items completed in the loop.

    Parameters
    ----------
    iterator : `iterator`
        An iterator that will be processed. The iterator is passed through by
        this function.
    n_items : `int`, optional
        Allows for ``iterator`` to be a generator whose length will be assumed
        to be `n_items`. If not provided, then ``iterator`` needs to be
        `Sizable`.

    Examples
    --------
    This for loop: ::

        from time import sleep
        for i in print_progress(range(100)):
            sleep(1)

    prints a progress report of the form: ::

        [=============       ] 70% (7/10) 00:00:03 remaining
    """
    n = n_items if n_items is not None else len(iterable)
    timings = deque([], 100)
    time1 = time()
    for i, x in enumerate(iterable):
        yield x
        time2 = time()
        timings.append(time2 - time1)
        time1 = time2
        remaining = n - i - 1
        duration = datetime.utcfromtimestamp(sum(timings) / len(timings) *
                                             remaining)
        remaining_str = duration.strftime('%H:%M:%S')
        bar_str = progress_bar_str((i + 1.0) / n)
        print_dynamic('{} ({}/{}) - {} remaining'.format(bar_str, i + 1, n,
                                                         remaining_str))
    print('')
