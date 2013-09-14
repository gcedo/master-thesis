import datetime


########################################
## Timeseries toolbox
########################################

class TimeseriesToolbox:
	def __init__(self):
		pass

	def _find_min_max(self, list_of_timeseries):
		min_dates = list()
		max_dates = list()

		for timeseries in list_of_timeseries:
			min_dates.append(timeseries.get_first_date())
			max_dates.append(timeseries.get_last_date())

		return (min(min_dates), max(max_dates))

	def merge(self, list_of_timeseries, merging_function = sum):
		(first_date, last_date) = self._find_min_max(list_of_timeseries)

		new_timeseries = Timeseries()
		current_date = first_date

		while current_date <= last_date:
			values = list()

			for timeseries in list_of_timeseries:
				values.append(timeseries.get_value(current_date))

			computed_value = merging_function(values)

			if computed_value != 0:
				new_timeseries.add_value(current_date, computed_value)

			current_date += datetime.timedelta(days = 1)

		return new_timeseries

	def export_csv(self, list_of_clusters):
		list_of_timeseries = map(lambda x: x.get_timeseries(), list_of_clusters)
		(first_date, last_date) = self._find_min_max(list_of_timeseries)		

		current_date = first_date

		header = ['date']
		for cluster in list_of_clusters:
			header.append(cluster.get_identifier())

		csv_string = [', '.join(header)]

		while current_date <= last_date:
			string = str(current_date)

			for timeseries in list_of_timeseries:
				string += ', ' + str(timeseries.get_value(current_date))

			csv_string.append(string)

			current_date += datetime.timedelta(days = 1)

		return '\n'.join(csv_string)

	def export_google_charts_js(self, list_of_clusters):
		title = list_of_clusters[0].get_identifier().split(':')[0]
		list_of_timeseries = map(lambda x: x.get_timeseries(), list_of_clusters)
		(first_date, last_date) = self._find_min_max(list_of_timeseries)		

		current_date = first_date
		output = list()	

		output.append("function drawVisualization() {")
		output.append("    var data = new google.visualization.DataTable();")
		output.append("    data.addColumn('date', 'Date');")

		for cluster in list_of_clusters:
			output.append("    data.addColumn('number', '" + cluster.get_identifier().split(':')[1] + "');")

		output.append("    data.addRows([")

		output_data = list()

		while current_date <= last_date:
			string = "        [new Date(" + str(current_date.year) + ", " + str(current_date.month - 1) + ", " + str(current_date.day) + ")"

			for timeseries in list_of_timeseries:
				string += ', ' + str(timeseries.get_value(current_date))

			string += ']'
			output_data.append(string)
			current_date += datetime.timedelta(days = 1)

		output.append(',\n'.join(output_data))
		output.append("    ]);")
		output.append("    var annotatedtimeline = new google.visualization.AnnotatedTimeLine(document.getElementById('visualization'));")
		output.append("    annotatedtimeline.draw(data, {'displayAnnotations': true});")
		output.append("    document.getElementById('title').innerHTML = '" + title + "';")
		output.append("}")

		return '\n'.join(output)


########################################
## Timeseries
########################################

class Timeseries:
	def __init__(self):
		self._data = dict()
		self._first_date = None
		self._last_date = None
		self._current_date = None

	def __len__(self):
		return len(self._data)

	def __iter__(self):
		if len(self) == 0:
			raise Exception('The timeseries is empty.')

		return self

	def add_value(self, date, value):
		self._data[date] = value

		if self._first_date == None or self._first_date > date:
			self._first_date = date

		if self._last_date == None or self._last_date < date:
			self._last_date = date

	def get_value(self, date):
		if date in self._data:
			return self._data[date]

		return 0

	def get_first_date(self):
		if len(self) == 0:
			raise Exception('The timeseries is empty.')

		return self._first_date

	def get_last_date(self):
		if len(self) == 0:
			raise Exception('The timeseries is empty.')

		return self._last_date

	def start_over(self):
		self._current_date = None

	def next(self):
		if self._current_date == None:
			self._current_date = self._first_date

		if self._current_date > self._last_date:
			raise StopIteration
		else:
			value_to_return = self.get_value(self._current_date)
			date_to_return = self._current_date
			self._current_date += datetime.timedelta(days = 1)
			return (date_to_return, value_to_return)