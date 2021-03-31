import pandas as pd
import Object_Definitions as od
import random as rd
from person_list import person_list, color_dict

### Days (inclusive) : YYYY-MM-DD
def span_days(first_day, last_day):
	days = pd.date_range(start=first_day, end=last_day)

	### Convert days to mutable objects
	day_object_list = []
	for i in days:
		day_object_list.append(od.day(i.to_pydatetime().date()))
	for i in day_object_list:
		weekday = i.date.weekday()
		i.assign_name(weekday)


	return day_object_list

def filter_days(weekday_list, days):
	filtered_list = []
	for i in days:
		if i.date_name in weekday_list:
			filtered_list.append(i)
		else:
			pass
	return filtered_list

def selection_func(person, days, iterator = 0):
	select = rd.choice(days)
	if iterator == 50:
		return None
	if select in person.cant_list or select in person.thursdays_assigned or select in person.weekends_assigned or select in person.weekdays_assigned:
		iterator+=1
		return selection_func(person, days, iterator)
	else:
		iterator+=1
		return select

def main_weekends_thursday(person_list, start_day, last_day, shuffle_iterator):
	### Shuffle List
	for i in range(shuffle_iterator):
		rd.shuffle(person_list)
	### filter days	
	raw_days1 = span_days(start_day, last_day)
	raw_days = []
	for i in raw_days1:
		raw_days.append(i)
		raw_days.append(i)
	thursdays = filter_days([3], raw_days)
	weekends = filter_days([4,5], raw_days)
	thursdays = [i.date.isoformat() for i in thursdays]
	weekends = [i.date.isoformat() for i in weekends]

	### Select thursdays
	iterator = 0
	iterator_max= len(person_list)
	while len(thursdays) != 0:
		current = person_list[iterator]
		selection = selection_func(current, thursdays)
		if selection == None:
			iterator+=1
			if iterator >= iterator_max:
				iterator=0
		else:
			current.assign_thursday(selection)
			thursdays.remove(selection)
			iterator+=1
			if iterator >= iterator_max:
				person_list.reverse()
				iterator=0
	### Select weekends
	for i in range(shuffle_iterator):
		rd.shuffle(person_list)
	while len(weekends) != 0:
		current = person_list[iterator]
		selection = selection_func(current, weekends)
		if selection == None:
			iterator+=1
			if iterator >= iterator_max:
				person_list.reverse()
				iterator=0
		else:
			current.assign_weekends(selection)
			weekends.remove(selection)
			iterator+=1
			if iterator >= iterator_max:
				person_list.reverse()
				iterator=0

	return person_list

def select_weekdays(person, days, iterator = 0):
	day_choice = []
	it = 0
	while len(day_choice)==0 and it<=len(person.weekday_picks):
		day_choice = filter_days([person.weekday_picks[it]], days)
		it+=1
	select1 = rd.choice(day_choice)
	select = select1.date.isoformat()
	if iterator == 100:
		return None
	if select in person.cant_list:
		iterator+=1
		return select_weekdays(person, days, iterator)
	elif select in person.weekdays_assigned:
		iterator+=1
		return select_weekdays(person, days, iterator)
	else:
		iterator+=1
		return select1

def main_weekdays_optimized(person_list, start_day, last_day, shuffle_iterator):
	### Find Weekdays
	raw_days1 = span_days(start_day, last_day)
	raw_days = []
	for i in raw_days1:
		raw_days.append(i)
		raw_days.append(i)
	weekdays = filter_days([6,0,1,2], raw_days)

	### Shuffle List
	for i in range(shuffle_iterator):
		rd.shuffle(person_list)
	### Select weekends
	iterator=0
	iterator_max= len(person_list)
	while len(weekdays) != 0:
		current = person_list[iterator]
		selection = select_weekdays(current, weekdays)
		if selection == None:
			iterator+=1
			if iterator >= iterator_max:
				person_list.reverse()
				iterator=0
		else:
			current.assign_weekday(selection.date.isoformat())
			weekdays.remove(selection)
			iterator+=1
			if iterator >= iterator_max:
				person_list.reverse()
				iterator=0

	return person_list


def main_weekdays_snake(person_list, start_day, last_day, shuffle_iterator, weekdays_list):

	### Shuffle List
	for i in range(shuffle_iterator):
		rd.shuffle(person_list)

	### Filter days
	raw_days1 = span_days(start_day, last_day)
	raw_days = []
	for i in raw_days1:
		raw_days.append(i)
		raw_days.append(i)
	weekdays_full1 = [] # Each item in list is a list of days for each day in weekdays list
	for i in weekdays_list:
		weekdays_full1.append(filter_days([i], raw_days))
	weekdays_full = []
	for i in weekdays_full1:
		weekdays_full.append([j.date.isoformat() for j in i])
	
	### Assign Days
	Day_dict = {i : [] for i in weekdays_list}
	for i in person_list:
		Day_dict[i.weekday_given].append(i)

	### weekdays except shared
	for day_meta, day_list in zip(weekdays_list, weekdays_full):
		if day_meta == 0:
			pass
		else:
			people = Day_dict[day_meta]
			iterator=0
			iterator_max=len(people)
			while len(day_list) != 0:
				current = people[iterator]
				selection = selection_func(current, day_list)
				if selection == None:
					iterator+=1
					if iterator >= iterator_max:
						person_list.reverse()
						iterator=0
				else:
					current.assign_weekday(selection)
					day_list.remove(selection)
					iterator+=1
					if iterator >= iterator_max:
						people.reverse()
						iterator=0

	### Weekday shared
	people = Day_dict[0]
	day_list = weekdays_full[1]
	people.append(od.Person('Random1', [],0))
	people.append(od.Person('Random1', [], 0))
	storage = []
	iterator=0
	iterator_max=len(people)
	while len(day_list) != 0:
		current = people[iterator]
		selection = selection_func(current, day_list)
		if selection == None:
			iterator+=1
			if iterator >= iterator_max:
				person_list.reverse()
				iterator=0
		else:
			if current.name == 'Random1':
				storage.append(selection)
			current.assign_weekday(selection)
			day_list.remove(selection)
			iterator+=1
			if iterator >= iterator_max:
				people.reverse()
				iterator=0
	
	people = []
	rd.shuffle(person_list)
	for i in person_list:
		if i.weekday_given != 0:
			people.append(i)
		else:
			pass
	iterator=0
	iterator_max=len(people)
	while len(storage) != 0:
		current = people[iterator]
		selection = selection_func(current, storage)
		if selection == None:
			iterator+=1
			if iterator >= iterator_max:
				person_list.reverse()
				iterator=0
		else:
			current.assign_weekday(selection)
			storage.remove(selection)
			iterator+=1
			if iterator >= iterator_max:
				people.reverse()
				iterator=0

	return person_list
	
		
	

#print(main_weekdays_snake(person_list, '2020-08-28', '2020-11-21', 1000, [6,0,1,2], [4,4,4,2]))




weekends = main_weekends_thursday(person_list, '2021-02-11', '2021-04-10', 1000)
full = main_weekdays_snake(weekends, '2021-02-11', '2021-04-10', 1000, [6,0,1,2])

### Print Days
def results(full):
	for i in full:
		print(i.name, ' - ', len(i.weekends_assigned)+len(i.weekdays_assigned)+len(i.thursdays_assigned))
		print('Weekends: ', i.weekends_assigned)
		print('Weekdays: ', i.weekdays_assigned)
		print('Thursdays: ', i.thursdays_assigned)

	print('-----------------------------------')
	print('-----------------------------------')
	print('-----------------------------------')

	### Print by Day
	days_dict = dict()
	for i in full:
		for j in i.weekends_assigned:
			if j in days_dict:
				point = days_dict[j]
				days_dict[j] = point + ', ' + i.name 
			else:
				days_dict[j] = i.name
		for j in i.weekdays_assigned:
			if j in days_dict:
				point = days_dict[j]
				days_dict[j] = point + ', ' + i.name 
			else:
				days_dict[j] = i.name
		for j in i.thursdays_assigned:
			if j in days_dict:
				point = days_dict[j]
				days_dict[j] = point + ', ' + i.name 
			else:
				days_dict[j] = i.name
	for i in sorted(days_dict.keys()):
		print(i, days_dict[i])


def get_days(person_list, first_day, last_day, iteration_random_size):
	weekends_thursdays = main_weekends_thursday(person_list, first_day, last_day, iteration_random_size)
	weekdays = main_weekdays_snake(weekends_thursdays, first_day, last_day, iteration_random_size, [6,0,1,2])
	return weekdays

def convert_to_events(weekdays_list):
	event_list = []
	for person in weekdays_list:
		for j in person.weekdays_assigned:
			event_list.append((j, person.name, person.email, color_dict[person.name]))
		for j in person.weekends_assigned:
			event_list.append((j, person.name, person.email, color_dict[person.name]))
		for j in person.thursdays_assigned:
			event_list.append((j, person.name, person.email, color_dict[person.name]))
	event_list.sort()
	return event_list

results(full)
