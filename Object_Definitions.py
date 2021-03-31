### Person Object
class Person:
	def __init__(self, name, cant_list, weekday_given, email='test@email.com'):
		self.name = name
		self.cant_list = cant_list
		self.thursdays_assigned = []
		self.weekends_assigned = []
		self.weekdays_assigned = []
		self.weekday_given = weekday_given
		self.email = email

	def assign_thursday(self, day):
		self.thursdays_assigned.append(day)
	def assign_weekends(self, day):
		self.weekends_assigned.append(day)
	def assign_weekday(self,day):
		self.weekdays_assigned.append(day)
	def assign_given(self,weekday):
		self.weekday_given = weekday


class day:
	def __init__(self, date):
		self.date = date
		self.date_name = None
		self.person_assigned = 'NO'
	
	def assign_person(self, person):
		self.person_assigned = person

	def assign_name(self, name):
		self.date_name = name