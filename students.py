import random
import re

class Students:
    def __init__(self, single_rooms, double_rooms):
        # Total dorm capacity: single rooms + 2 * double rooms
        self.max_capacity = single_rooms + (double_rooms * 2)
        self.female_students = 0
        self.male_students = 0

    def get_student_input(self, gender, max_allowed, auto_random=False):
        """
        Ask user for number of students by gender.
        If auto_random=True, returns a random number without asking user.
        """
        while True:
            try:
                if auto_random:
                    # Pick random number between 0 and max_allowed
                    value = random.randint(0, max_allowed)
                    return value

                value = input(f"Enter number of {gender} students (0–{max_allowed}) or press Enter for auto-random: ")

                # ✅ If blank → random
                if value.strip() == "":
                    value = random.randint(0, max_allowed)
                    print(f"Using random value: {value}")
                    return value

                # 🚫 Validate input
                if not re.fullmatch(r"\d{1,3}", value.strip()):
                    raise ValueError("Input must be a whole number (0–999, no letters, symbols, negatives, decimals).")

                value = int(value)

                # ✅ Range check
                if value < 0 or value > max_allowed:
                    raise ValueError(f"Value must be between 0 and {max_allowed}.")

                return value

            except ValueError as e:
                print(f"❌ Invalid input: {e}\nPlease try again.\n")

    def create_students(self):
        """
        Ask user for female/male counts.
        If no values entered, auto-generate exactly total capacity
        and randomly assign male/female split.
        """
        print(f"\n👩‍🎓👨‍🎓 Student setup (max total: {self.max_capacity})")

        # Ask female count first
        female_input = input(f"Enter number of female students (0–{self.max_capacity}) or press Enter for auto-random: ")
        male_input = input(f"Enter number of male students (0–{self.max_capacity}) or press Enter for auto-random: ")

        # If BOTH are blank, generate exact total capacity
        if female_input.strip() == "" and male_input.strip() == "":
            # Random split of total students
            self.female_students = random.randint(0, self.max_capacity)
            self.male_students = self.max_capacity - self.female_students
            print(f"Randomly generated total {self.max_capacity} students:")
            print(f"Female: {self.female_students}, Male: {self.male_students}")
            return

        # Else, get female students
        self.female_students = self.get_student_input(
            "female",
            self.max_capacity
            if female_input.strip() == "" else int(female_input),
            auto_random=(female_input.strip() == "")
        )

        # Remaining capacity for males
        remaining = self.max_capacity - self.female_students
        if remaining < 0:
            print("❌ Total exceeds capacity. Restart student creation.\n")
            return self.create_students()

        # Get male students
        self.male_students = self.get_student_input(
            "male",
            remaining,
            auto_random=(male_input.strip() == "")
        )

        total = self.female_students + self.male_students
        if total > self.max_capacity:
            print(f"❌ Total students ({total}) exceed capacity ({self.max_capacity}). Restart student creation.\n")
            return self.create_students()

        print(f"\n✅ Student setup complete!")
        print(f"Female students: {self.female_students}")
        print(f"Male students: {self.male_students}")
        print(f"Total students: {total} / {self.max_capacity}")

class Student:
    def __init__(self, student_id, gender):
        self.id = student_id
        self.gender = gender
