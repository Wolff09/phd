#!/usr/bin/env python2
#-*- coding: utf-8 -*-


STATES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16]

FINAL = 16

TRANS = [
	# upper part
	(0, "enter protect1(T, P)", 1),
	(1, "exit protect1(T)", 2),
	(1, "enter protect2(T, P)", 4),
	(2, "enter protect2(T, P)", 5),
	(3, "enter protect2(T, P)", 6),
	(4, "exit protect1(T)", 5),
	(4, "exit protect2(T)", 13),
	(5, "exit protect2(T)", 7),
	(6, "exit protect2(T)", 8),
	(2, "enter retire(*, P)", 3),
	(5, "enter retire(*, P)", 6),
	(7, "enter retire(*, P)", 8),

	# lower part
	(0, "enter protect2(T, P)", 9),
	(9, "exit protect2(T)", 10),
	(9, "enter protect1(T, P)", 4),
	(10, "enter protect1(T, P)", 13),
	(11, "enter protect1(T, P)", 14),
	(13, "exit protect1(T)", 7),
	(14, "exit protect1(T)", 15),
	(10, "enter retire(*, P)", 11),
	(13, "enter retire(*, P)", 14),

	# unprotects
	(2, "enter protect1(T, !P)", 0),
	(3, "enter protect1(T, !P)", 0),
	(7, "enter protect1(T, !P)", 10),
	(8, "enter protect1(T, !P)", 11),
	(7, "enter protect2(T, !P)", 2),
	(8, "enter protect2(T, !P)", 3),
	(10, "enter protect2(T, !P)", 0),
	(11, "enter protect2(T, !P)", 0),
	(15, "enter protect2(T, !P)", 2),
	(15, "enter protect1(T, !P)", 11),

	# frees
	(3, "free(*, P)", 16),
	(6, "free(*, P)", 16),
	(8, "free(*, P)", 16),
	(11, "free(*, P)", 16),
	(14, "free(*, P)", 16),
	(15, "free(*, P)", 16),
	

	# both fully protected, then retired
	(15, "enter retire(*, P)", 8),

	# reset when re-protected # atomic protection (without) vs non-atomic protection (with)
	# (2, "enter protect1(T, P)", 1),
	# (3, "enter protect1(T, P)", 1),
	# (7, "enter protect2(T, P)", 5),
	# (8, "enter protect2(T, P)", 6),
	# (7, "enter protect1(T, P)", 13),
	# (8, "enter protect1(T, P)", 14),
	# (10, "enter protect2(T, P)", 9),
	# (11, "enter protect2(T, P)", 9),
	# (13, "enter protect2(T, P)", 4),
	# (14, "enter protect2(T, P)", 4),
	# (15, "enter protect2(T, P)", 5),
	# (15, "enter protect1(T, P)", 14),

	# reset in the middle
	(1, "enter protect1(T, !P)", 0),
	(4, "enter protect1(T, !P)", 9),
	(4, "enter protect2(T, !P)", 1),
	(5, "enter protect1(T, !P)", 9),
	(6, "enter protect1(T, !P)", 9),
	(5, "enter protect2(T, !P)", 2),
	(6, "enter protect2(T, !P)", 3),
	(9, "enter protect2(T, !P)", 0),
	(13, "enter protect2(T, !P)", 1),
	(14, "enter protect2(T, !P)", 1),
	(13, "enter protect1(T, !P)", 10),
	(14, "enter protect1(T, !P)", 11),
]

SYMBOLS = [
	"enter protect1(T, P)",
	"exit protect1(T)",
	"enter protect2(T, P)",
	"exit protect2(T)",
	"enter retire(*, P)",
	"enter protect1(T, !P)",
	"enter protect2(T, !P)",
	"free(*, P)"
]

SIM = []


def get_next(n, sym):
	for (pre, lab, post) in TRANS:
		if pre == n and lab == sym:
			return post
	return n

def check_sim(x, y):
	if x != FINAL and y == FINAL:
		# print "not in simulation: ", x, ",", y, "  because of acceptance"
		return False
	for symbol in SYMBOLS:
		next_x = get_next(x, symbol)
		next_y = get_next(y, symbol)
		if not (next_x, next_y) in SIM:
			# print "not in simulation: ", x, ",", y, "  because of: ", next_x, ",", next_y, "  via ", symbol
			return False
	return True

def compute_sim():
	# all combinations
	for x in STATES:
		for y in STATES:
			SIM.append((x, y))
	print("starting...")

	# filter
	while True:
		removed = False
		for (x, y) in SIM:
			if not check_sim(x, y):
				SIM.remove((x, y))
				removed = True
			if removed: break
		if not removed: break

	# print
	print "done... ", len(SIM)
	for (x, y) in SIM:
		print x, " < ", y

if __name__ == '__main__':
	compute_sim()

