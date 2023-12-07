# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    new_dates = [datetime.strptime(old_date,"%Y-%m-%d").strftime("%d %b %Y") for old_date in old_dates]
    return new_dates


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    start_date = datetime.strptime(start,"%Y-%m-%d")
    new_dates = [start_date+timedelta(days=i) for i in range(n)]
    return new_dates


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    start_Date = datetime.strptime(start_date,"%Y-%m-%d")
    new_dates = [(start_date+timedelta(days=pos),val) for pos,val in enumerate(values)]
    return new_dates


def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    late_fees_dict = defaultdict(float)
    with open(infile) as file:
        reader = DictReader(file)
        for row in reader:
            date_due = datetime.strptime(row['date_due'],"%m/%d/%Y")
            date_returned = datetime.strptime(row['date_returned'],"%m/%d/%Y")
            if date_returned > date_due:
                days_late = (date_returned - due_date).days
                late_fee = round(days_late*0.25,2)
                late_fees_dict[row['patron_id']] += late_fee
            else:
                late_fees_dict[row['patron_id']] += 0.00
    fees_dict = [{'patron_id':key,'late_fees':str(value) +'0' if len(str(value).split('.')[-1]) !=2 else str(value)} for key,value in late_fees_dict.items()]
    with open(outfile,'w',newline='') as file:
        cols = ['patron_id','late_fees']
        writer = DictWriter(file,cols)
        writer.writeheader()
        writer.writerows(fees_dict)


# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
