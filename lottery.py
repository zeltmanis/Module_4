import random

class DormLottery:
    def __init__(self, students, single_rooms, double_rooms):
        """
        students: list of Student objects with id and gender
        single_rooms: number of single rooms
        double_rooms: number of double rooms
        """
        self.students = students
        self.single_rooms = single_rooms
        self.double_rooms = double_rooms

    def run_lottery(self):
        total_students = len(self.students)
        if self.single_rooms + self.double_rooms * 2 != total_students:
            raise ValueError("Room capacity does not match total students!")

        # Step 1: Shuffle students for fairness
        random.shuffle(self.students)

        # Step 2: Assign single rooms
        single_winners = self.students[:self.single_rooms]
        remaining_students = self.students[self.single_rooms:]

        # Step 3: Assign double rooms
        males = [s for s in remaining_students if s.gender == "M"]
        females = [s for s in remaining_students if s.gender == "F"]

        double_room_pairs = []

        # Pair females
        while len(females) >= 2:
            double_room_pairs.append([females.pop(), females.pop()])

        # Pair males
        while len(males) >= 2:
            double_room_pairs.append([males.pop(), males.pop()])

        # Step 4: Handle leftover students
        leftovers = males + females  # at most 1 male or 1 female
        if leftovers:
            for leftover in leftovers:
                swap_found = False
                # Try to swap with a single of opposite gender
                for i, s in enumerate(single_winners):
                    if s.gender != leftover.gender:
                        single_winners[i], leftover = leftover, single_winners[i]
                        double_room_pairs.append([leftover])
                        swap_found = True
                        break
                if not swap_found:
                    # Rare edge case: assign leftover as single
                    single_winners.append(leftover)

        return single_winners, double_room_pairs

    def print_lottery(self, single_winners, double_room_pairs):
        print("\n🎲 Lottery Results:")
        print("\nSingle room assignments:")
        for s in single_winners:
            print(f"{s.id} ({s.gender})")

        print("\nDouble room assignments:")
        for i, pair in enumerate(double_room_pairs, 1):
            pair_str = ", ".join(f"{s.id} ({s.gender})" for s in pair)
            print(f"Double Room {i}: {pair_str}")