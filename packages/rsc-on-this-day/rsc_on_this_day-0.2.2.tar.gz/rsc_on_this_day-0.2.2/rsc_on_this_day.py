#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  rsc_on_this_day.py
"""
Displays Royal Society of Chemistry "On This Day In Chemistry" facts in your terminal.
"""
#
#  Copyright © 2019-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Cached copies of the RSC On This Day website Copyright © 2020 Royal Society of Chemistry
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

__author__ = "Dominic Davis-Foster"
__copyright__ = "2019-2020 Dominic Davis-Foster"

__license__ = "GPLv3"
__version__ = "0.2.2"
__email__ = "dominic@davis-foster.co.uk"

# stdlib
import datetime
import pathlib
import sys
import textwrap

# 3rd party
import appdirs
import requests
import requests_cache
from bs4 import BeautifulSoup
from cachier import cachier
from domdf_python_tools.dates import check_date, parse_month

# TODO: Timeout

# Create directory for cache
cache_dir = pathlib.Path(appdirs.user_cache_dir("rsc_on_this_day"))
if not cache_dir.exists():
	cache_dir.mkdir(parents=True, exist_ok=True)

# Today's date
today = datetime.date.today()

date_arg_error_str = "If requesting a specific date both the month and day must be given."


# Cache answers for 5 hours
@cachier(stale_after=datetime.timedelta(hours=5), cache_dir=str(cache_dir))
def get_fact(month=None, day=None):
	if (month and not day) or (day and not month):
		raise SyntaxError(date_arg_error_str)
	
	if not month and not day:
		month = today.strftime("%B")
		day = today.day
	
	date = f"{month}-{day}"
	
	page = requests.get(
			f"https://web.archive.org/web/20190331053029id_/"
			f"http://www.rsc.org/learn-chemistry/collections/chemistry-calendar/{date}")
	
	soup = BeautifulSoup(page.content, "html.parser")
	
	header = soup.find("div", {"class": "description"}).previousSibling.previousSibling.get_text().strip()
	body = soup.find("div", {"class": "description"}).get_text().strip()
	
	return header, body


def clear_cache():
	requests_cache.clear()
	get_fact.clear_cache()
	print("Cache cleared successfully.")
	return 0


def main():
	import argparse
	
	parser = argparse.ArgumentParser(description=__doc__, epilog=date_arg_error_str)
	shared_kwargs = dict(default=None, nargs="?")
	parser.add_argument('month', **shared_kwargs, help='The name or number of the month of the fact to display.')
	parser.add_argument('day', type=int, **shared_kwargs, help='The day number of the fact to display.')
	parser.add_argument(
			"-w", '--width', metavar="WIDTH", type=int, default=80, nargs="?",
			help='The number of characters per line of the output. Default 80. Set to -1 to disable wrapping.')
	
	parser.add_argument(
			'--clear-cache', dest="clear_cache", action="store_true", default=False,
			help='Clears any cached data and exits.')
	
	args = parser.parse_args()
	
	if args.clear_cache:
		sys.exit(clear_cache())
	
	if (args.month and args.day is None) or (args.day and args.month is None):
		parser.error(date_arg_error_str)
	
	month = args.month
	
	if month is not None and args.day is not None:
		try:
			month = parse_month(month)
		except ValueError:
			parser.error(f"Invalid value for month: {month}")
		
		# Check that the date is valid
		if not check_date(month, args.day):
			parser.error(f"{args.day}/{month} is not a valid date.")
	
	header, body = get_fact(month, args.day)
	
	if args.width > 0:
		header = textwrap.fill(header, args.width)
		body = textwrap.fill(body, args.width)
	
	# print(f"{args.day}/{month}")
	print(header)
	print(body)


if __name__ == "__main__":
	# Set up requests_cache and keep cache for about a month
	# We do this here so we don't interfere with programs that import from this program
	requests_cache.install_cache(str(cache_dir / "requests_cache"), expire_after=2500000)
	requests_cache.remove_expired_responses()
	
	main()
