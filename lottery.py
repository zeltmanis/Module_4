import random

class DormLottery:
    def __init__(self, students, single_rooms, double_rooms):
        self.students = students
        self.single_rooms = single_rooms
        self.double_rooms = double_rooms

    # Standard random lottery
    def run_lottery(self):
        total_students = len(self.students)
        if self.single_rooms + self.double_rooms * 2 != total_students:
            raise ValueError("Room capacity does not match total students!")

        random.shuffle(self.students)
        single_winners = self.students[:self.single_rooms]
        remaining_students = self.students[self.single_rooms:]

        males = [s for s in remaining_students if s.gender == "M"]
        females = [s for s in remaining_students if s.gender == "F"]

        double_room_pairs = []

        while len(females) >= 2:
            double_room_pairs.append([females.pop(), females.pop()])
        while len(males) >= 2:
            double_room_pairs.append([males.pop(), males.pop()])

        leftovers = males + females
        if leftovers:
            for leftover in leftovers:
                swap_found = False
                for i, s in enumerate(single_winners):
                    if s.gender != leftover.gender:
                        single_winners[i], leftover = leftover, single_winners[i]
                        double_room_pairs.append([leftover])
                        swap_found = True
                        break
                if not swap_found:
                    single_winners.append(leftover)

        return single_winners, double_room_pairs

    # GPA-weighted lottery
    def run_gpa_weighted_lottery(self):
        total_students = len(self.students)
        if self.single_rooms + self.double_rooms * 2 != total_students:
            raise ValueError("Room capacity does not match total students!")

        # Create tickets based on GPA
        ticket_pool = []
        for s in self.students:
            tickets = max(1, int(s.gpa * 10))  # minimum 1 ticket
            ticket_pool.extend([s] * tickets)

        # Randomly pick single room winners from tickets
        single_winners = []
        selected_ids = set()
        while len(single_winners) < self.single_rooms:
            s = random.choice(ticket_pool)
            if s.id not in selected_ids:
                single_winners.append(s)
                selected_ids.add(s.id)

        remaining_students = [s for s in self.students if s.id not in selected_ids]

        males = [s for s in remaining_students if s.gender == "M"]
        females = [s for s in remaining_students if s.gender == "F"]

        double_room_pairs = []

        while len(females) >= 2:
            double_room_pairs.append([females.pop(), females.pop()])
        while len(males) >= 2:
            double_room_pairs.append([males.pop(), males.pop()])

        leftovers = males + females
        if leftovers:
            for leftover in leftovers:
                swap_found = False
                for i, s in enumerate(single_winners):
                    if s.gender != leftover.gender:
                        single_winners[i], leftover = leftover, single_winners[i]
                        double_room_pairs.append([leftover])
                        swap_found = True
                        break
                if not swap_found:
                    single_winners.append(leftover)

        return single_winners, double_room_pairs

    def print_lottery(self, single_winners, double_room_pairs):
        print("\n🎲 Lottery Results:")
        print("\nSingle room assignments:")
        for s in single_winners:
            gpa_str = f" - GPA: {s.gpa:.2f}" if hasattr(s, "gpa") else ""
            print(f"{s.id} ({s.gender}){gpa_str}")

        print("\nDouble room assignments:")
        for i, pair in enumerate(double_room_pairs, 1):
            pair_str = ", ".join(f"{s.id} ({s.gender})" + (f" - GPA: {s.gpa:.2f}" if hasattr(s, "gpa") else "")
                                 for s in pair)
            print(f"Double Room {i}: {pair_str}")