from common.util import *
from typing import List, Tuple
from copy import deepcopy

# --- Day 11: Seating System ---
# Your plane lands with plenty of time to spare. The final leg of your journey is a ferry that goes directly
# to the tropical island where you can finally start your vacation. As you reach the waiting area to board the ferry,
# you realize you're so early, nobody else has even arrived yet!

# By modeling the process people use to choose (or abandon) their seat in the waiting area,
# you're pretty sure you can predict the best place to sit. You make a quick map of the seat layout (your puzzle input).

# The seat layout fits neatly on a grid. Each position is either floor (.), an empty seat (L),
# or an occupied seat (#). For example, the initial seat layout might look like this:

# L.LL.LL.LL
# LLLLLLL.LL
# L.L.L..L..
# LLLL.LL.LL
# L.LL.LL.LL
# L.LLLLL.LL
# ..L.L.....
# LLLLLLLLLL
# L.LLLLLL.L
# L.LLLLL.LL
# Now, you just need to model the people who will be arriving shortly.
# Fortunately, people are entirely predictable and always follow a simple set of rules.
# All decisions are based on the number of occupied seats adjacent to a given seat
# (one of the eight positions immediately up, down, left, right, or diagonal from the seat).
# The following rules are applied to every seat simultaneously:

# If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
# If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
# Otherwise, the seat's state does not change.
# Floor (.) never changes; seats don't move, and nobody sits on the floor.

# After one round of these rules, every seat in the example layout becomes occupied:

# #.##.##.##
# #######.##
# #.#.#..#..
# ####.##.##
# #.##.##.##
# #.#####.##
# ..#.#.....
# ##########
# #.######.#
# #.#####.##
# After a second round, the seats with four or more occupied adjacent seats become empty again:

# #.LL.L#.##
# #LLLLLL.L#
# L.L.L..L..
# #LLL.LL.L#
# #.LL.LL.LL
# #.LLLL#.##
# ..L.L.....
# #LLLLLLLL#
# #.LLLLLL.L
# #.#LLLL.##
# This process continues for three more rounds:

# #.##.L#.##
# #L###LL.L#
# L.#.#..#..
# #L##.##.L#
# #.##.LL.LL
# #.###L#.##
# ..#.#.....
# #L######L#
# #.LL###L.L
# #.#L###.##
# #.#L.L#.##
# #LLL#LL.L#
# L.L.L..#..
# #LLL.##.L#
# #.LL.LL.LL
# #.LL#L#.##
# ..L.L.....
# #L#LLLL#L#
# #.LLLLLL.L
# #.#L#L#.##
# #.#L.L#.##
# #LLL#LL.L#
# L.#.L..#..
# #L##.##.L#
# #.#L.LL.LL
# #.#L#L#.##
# ..L.L.....
# #L#L##L#L#
# #.LLLLLL.L
# #.#L#L#.##
# At this point, something interesting happens: the chaos stabilizes and further applications
# of these rules cause no seats to change state! Once people stop moving around, you count 37 occupied seats.

# Simulate your seating area by applying the seating rules repeatedly until no seats change state.
# How many seats end up occupied?


class Seating:
    def __init__(self, seat_map: List[List[str]]):
        self.seat_map = seat_map

    def get_adj_coords(self, x: int, y: int) -> int:
        # Check 8 adjacent
        # (-1, -1) (-1, 0) (-1, 1)
        # (0, -1) (0, 0) (0, 1)
        # (1, -1) (1, 0) (1, 1)

        # Boundaries
        x_min, x_max, y_min, y_max = 0, len(self.seat_map[0]), 0, len(self.seat_map)

        adj_map = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        return [
            (i + x, j + y)
            for i, j in adj_map
            if x_min <= i + x < x_max and y_min <= j + y < y_max
        ]  # Only compute inside the boundary

    @staticmethod
    def count_occupied(seat_map: List[List[str]]) -> int:
        count = 0
        for y, y_list in enumerate(seat_map):
            for x in range(len(y_list)):
                if seat_map[y][x] == "#":
                    count += 1

        return count

    def count_occupied_adj(self, adj_list: List[Tuple[int, int]]) -> int:
        count = 0
        for x, y in adj_list:
            if self.seat_map[y][x] == "#":
                count += 1

        return count

    def step(self) -> List[List[str]]:
        """occupy or empty"""
        result_map = deepcopy(self.seat_map)
        for y, y_list in enumerate(self.seat_map):
            for x in range(len(y_list)):
                if self.seat_map[y][x] == "L":
                    adj_list = self.get_adj_coords(x, y)
                    if self.count_occupied_adj(adj_list) == 0:
                        result_map[y][x] = "#"
                elif self.seat_map[y][x] == "#":
                    adj_list = self.get_adj_coords(x, y)
                    if self.count_occupied_adj(adj_list) >= 4:
                        result_map[y][x] = "L"

        self.seat_map = result_map

        return result_map


def part1(data: List[int]) -> int:
    seating = Seating(data)

    prev_seat_map = None
    while True:
        seating.step()

        if prev_seat_map == seating.seat_map:
            return Seating.count_occupied(prev_seat_map)

        prev_seat_map = seating.seat_map


data = get_data("day11", grid_parser)
print(part1(data))


# TEST
test1 = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
"""
print(part1(grid_parser(test1)))


# --- Part Two ---
# As soon as people start to arrive, you realize your mistake. People don't just care about adjacent seats -
# they care about the first seat they can see in each of those eight directions!

# Now, instead of considering just the eight immediately adjacent seats, consider the first seat in each of those eight directions.
# For example, the empty seat below would see eight occupied seats:

# .......#.
# ...#.....
# .#.......
# .........
# ..#L....#
# ....#....
# .........
# #........
# ...#.....
# The leftmost empty seat below would only see one empty seat, but cannot see any of the occupied ones:

# .............
# .L.L.#.#.#.#.
# .............
# The empty seat below would see no occupied seats:

# .##.##.
# #.#.#.#
# ##...##
# ...L...
# ##...##
# #.#.#.#
# .##.##.
# Also, people seem to be more tolerant than you expected: it now takes five or more visible occupied seats
# for an occupied seat to become empty (rather than four or more from the previous rules). The other rules still apply:
# empty seats that see no occupied seats become occupied, seats matching no rule don't change, and floor never changes.

# Given the same starting layout as above, these new rules cause the seating area to shift around as follows:

# L.LL.LL.LL
# LLLLLLL.LL
# L.L.L..L..
# LLLL.LL.LL
# L.LL.LL.LL
# L.LLLLL.LL
# ..L.L.....
# LLLLLLLLLL
# L.LLLLLL.L
# L.LLLLL.LL

# #.##.##.##
# #######.##
# #.#.#..#..
# ####.##.##
# #.##.##.##
# #.#####.##
# ..#.#.....
# ##########
# #.######.#
# #.#####.##

# #.LL.LL.L#
# #LLLLLL.LL
# L.L.L..L..
# LLLL.LL.LL
# L.LL.LL.LL
# L.LLLLL.LL
# ..L.L.....
# LLLLLLLLL#
# #.LLLLLL.L
# #.LLLLL.L#

# #.L#.##.L#
# #L#####.LL
# L.#.#..#..
# ##L#.##.##
# #.##.#L.##
# #.#####.#L
# ..#.#.....
# LLL####LL#
# #.L#####.L
# #.L####.L#

# #.L#.L#.L#
# #LLLLLL.LL
# L.L.L..#..
# ##LL.LL.L#
# L.LL.LL.L#
# #.LLLLL.LL
# ..L.L.....
# LLLLLLLLL#
# #.LLLLL#.L
# #.L#LL#.L#

# #.L#.L#.L#
# #LLLLLL.LL
# L.L.L..#..
# ##L#.#L.L#
# L.L#.#L.L#
# #.L####.LL
# ..#.#.....
# LLL###LLL#
# #.LLLLL#.L
# #.L#LL#.L#

# #.L#.L#.L#
# #LLLLLL.LL
# L.L.L..#..
# ##L#.#L.L#
# L.L#.LL.L#
# #.LLLL#.LL
# ..#.L.....
# LLL###LLL#
# #.LLLLL#.L
# #.L#LL#.L#

# Again, at this point, people stop shifting around and the seating area reaches equilibrium. Once this occurs, you count 26 occupied seats.

# Given the new visibility method and the rule change for occupied seats becoming empty, once equilibrium is reached, how many seats end up occupied?


# class VisibleSeating(Seating):
#     def __init__(self, seat_map: List[List[str]]):
#         self.seat_map = seat_map
#         self.x_min = 0
#         self.x_max = len(self.seat_map[0])
#         self.y_min = 0
#         self.y_max = len(self.seat_map)

#     def count_visible_occupied(self, visible_list: List[Tuple[int, int]]) -> int:
#         count = 0
#         for x, y in visible_list:
#             if self.seat_map[y][x] == "#":
#                 count += 1

#         return count

#     def get_visible_coords(self, x: int, y: int, multiplier: int) -> int:

#         # Boundaries
#         adj_map = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
#         visible_map = [
#             (adj_x * multiplier, adj_y * multiplier) for adj_x, adj_y in adj_map
#         ]

#         return [
#             (i + x, j + y)
#             for i, j in visible_map
#             if self.x_min <= i + x < self.x_max and self.y_min <= j + y < self.y_max
#         ]  # Only compute inside the boundary

#     def step(self) -> List[List[str]]:
#         """occupy or empty"""
#         result_map = deepcopy(self.seat_map)
#         for y, y_list in enumerate(self.seat_map):
#             for x in range(len(y_list)):

#                 while

#                 if self.seat_map[y][x] == "L":
#                     adj_list = self.get_adj_coords(x, y)
#                     if self.count_occupied_adj(adj_list) == 0:
#                         result_map[y][x] = "#"

#                 elif self.seat_map[y][x] == "#":
#                     adj_list = self.get_adj_coords(x, y)
#                     if self.count_occupied_adj(adj_list) >= 4:
#                         result_map[y][x] = "L"

#         self.seat_map = result_map

#         return result_map


# def part2(data: List[int]) -> int:
#     pass


# data = get_data("day11", grid_parser)
# print(part2(data))
