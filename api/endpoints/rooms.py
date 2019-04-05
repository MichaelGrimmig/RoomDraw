#!/usr/bin/python

import private.sql as sql
import private.constants as constants
import private.stored_procs as procs
import classes.rooms
import session

from utils import *

class Room:
	def on_get(self, request, response):
		response.media = {}
		session_token = get_session(request)
		if not authenticated(session_token):
			response.media = "Not authenticated"
			return

		k_dorm            = "dorm"
		k_number          = "number"
		k_capacity        = "capacity"
		k_available_spots = "spots_left"
		k_floor           = "floor"

		room_number = get_val(request.params, k_number)
		spots_left = get_val(request.params, k_available_spots)
		floor = get_val(request.params, k_floor)
		dorm = get_val(request.params, k_dorm)

		# look for rooms in a certain dorm
		# TODO send correct status code, etc
		if dorm is None:
			response.media = "I need a dorm id to continue"
			return

		try:
			room_number = int(room_number)
			spots_left  = int(spots_left)
			floor       = int(floor)
		except (TypeError, ValueError):
			response.media = "Bad or missing parameter somewhere"
			return

		# TODO add option to search for a particular room (not a priority)
		connection = sql.SQL()
		results = connection.run_stored_proc_for_multiple_items(procs.get_rooms,
				dorm, room_number, spots_left, floor)
		room_list = []
		if results:
			for room in results:
				room_list.append(classes.rooms.Room(room))
			response.media = room_list
