from dorm_rooms import DormRooms
from students import Students, Student
from lottery import DormLottery
from report import ReportGenerator


def get_lottery_runs():
    """
    Ask user how many times to run the lottery using menu choices.
    1 = 100, 2 = 1,000, 3 = 10,000, 4 = 100,000
    """
    options = {"1": 100, "2": 1000, "3": 10000, "4": 100000}

    print("\nHow many times would you like to run the lottery?")
    print("1 = 100")
    print("2 = 1,000")
    print("3 = 10,000")
    print("4 = 100,000")

    while True:
        choice = input("Enter your choice (default 2): ").strip()
        if choice == "":
            return options["2"]
        if choice in options:
            return options[choice]
        print("❌ Invalid input. Please select 1, 2, 3, or 4.")


def generate_students(students_generator):
    """Helper to create all Student objects with random GPA"""
    students = []
    for i in range(1, students_generator.female_students + 1):
        students.append(Student(f"F{i:03}", "F"))
    for i in range(1, students_generator.male_students + 1):
        students.append(Student(f"M{i:03}", "M"))
    return students


def main():
    print("🎓 Welcome to the Dorm Room Builder System\n")

    # Step 1: Create dorm rooms
    dorm = DormRooms()
    dorm.create_rooms()

    # Step 2: Create students
    students_generator = Students(dorm.single_rooms, dorm.double_rooms)
    students_generator.create_students()

    while True:
        print("\n===== Lottery Menu =====")
        print("1. Run random lottery / generate report")
        print("2. Run GPA-influenced lottery / generate report")
        print("3. Adjust dorm rooms (auto adjusts students)")
        print("4. Quit")

        choice = input("Select an option: ").strip()

        # === Option 1: Regular random lottery ===
        if choice == "1":
            runs = get_lottery_runs()
            students = generate_students(students_generator)
            lottery = DormLottery(students, dorm.single_rooms, dorm.double_rooms)

            singles, doubles = lottery.run_lottery()
            lottery.print_lottery(singles, doubles)

            report = ReportGenerator(lottery, runs=runs)
            report.run_simulation()

        # === Option 2: GPA-weighted lottery ===
        elif choice == "2":
            runs = get_lottery_runs()
            students = generate_students(students_generator)
            lottery = DormLottery(students, dorm.single_rooms, dorm.double_rooms)

            singles, doubles = lottery.run_gpa_weighted_lottery()
            lottery.print_lottery(singles, doubles)

            report = ReportGenerator(lottery, runs=runs)
            report.run_gpa_weighted_simulation()

        # === Option 3: Adjust rooms ===
        elif choice == "3":
            dorm.create_rooms()
            students_generator.max_capacity = dorm.single_rooms + dorm.double_rooms * 2
            print("\n🔄 Auto-adjusting students for new dorm setup...")
            students_generator.create_students()

        # === Option 4: Quit ===
        elif choice == "4":
            print("👋 Exiting Dorm Lottery System. Goodbye!")
            break

        else:
            print("❌ Invalid option, please choose 1–4.")


if __name__ == "__main__":
    main()