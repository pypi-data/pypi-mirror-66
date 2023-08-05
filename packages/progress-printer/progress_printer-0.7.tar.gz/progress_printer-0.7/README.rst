progress_printer
-----

The progress_printer package provides an easy way to output the progress and estimated finish time for a for loop.

To use, do:
	>>> import progress_printer as pp
	>>> import datetime

    >>> t0 = datetime.datetime.now() # this sets the reference time
	>>> for i, list_item in enumerate(list):
	>>>     pp.ProgressStatus(i, len(list)) # here the progress printer is called and the command line is updated with current percentage and completion time
	>>>     # do something

