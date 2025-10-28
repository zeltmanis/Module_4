import random
import re


class Students:
    def __init__(self, single_rooms, double_rooms):
        # Total dorm capacity: single rooms + 2 * double rooms
        self.max_capacity = single_rooms + (double_rooms * 2)
        self.female_students = 0
        self.male_students = 0

    def create_students(self):
        """
        Ask only how many female students.
        The rest will be male automatically.
        """
        print(f"\n👩‍🎓👨‍🎓 Student setup (max total students: {self.max_capacity})")

        while True:
            try:
                value = input(
                    f"Enter number of female students (0–{self.max_capacity}) or press Enter for random: ").strip()

                if value == "":
                    self.female_students = random.randint(0, self.max_capacity)
                    print(f"Using random value for female students: {self.female_students}")
                else:
                    if not re.fullmatch(r"\d{1,3}", value):
                        raise ValueError("Input must be a number (0–999).")
                    self.female_students = int(value)
                    if not (0 <= self.female_students <= self.max_capacity):
                        raise ValueError(f"Value must be between 0 and {self.max_capacity}.")

                # Automatically assign the rest as male
                self.male_students = self.max_capacity - self.female_students

                print(f"\n✅ Student setup complete!")
                print(f"Female students: {self.female_students}")
                print(f"Male students: {self.male_students}")
                print(f"Total students: {self.max_capacity} / {self.max_capacity}")
                break  # valid input, exit loop

            except ValueError as e:
                print(f"❌ Invalid input: {e}\nPlease try again.\n")


class Student:
    def __init__(self, student_id, gender):
        self.id = student_id
        self.gender = gender
        self.gpa = round(random.uniform(0.0, 10.0), 2)

        def __repr__(self):
            return f"{self.id} ({self.gender}) - GPA: {self.gpa}"