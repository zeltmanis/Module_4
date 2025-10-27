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
        print("1. Run lottery / generate report")
        print("2. Adjust dorm rooms (auto adjusts students)")
        print("3. Quit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            # Ask how many runs
            runs = get_lottery_runs()

            # Generate Student objects
            students = []
            for i in range(1, students_generator.female_students + 1):
                students.append(Student(f"F{i:03}", "F"))
            for i in range(1, students_generator.male_students + 1):
                students.append(Student(f"M{i:03}", "M"))

            lottery = DormLottery(students, dorm.single_rooms, dorm.double_rooms)

            # Run single lottery
            singles, doubles = lottery.run_lottery()
            lottery.print_lottery(singles, doubles)

            # Run multiple simulations and generate report
            report = ReportGenerator(lottery, runs=runs, report_file="lottery_report.csv")
            report.run_simulation()

        elif choice == "2":
            # Adjust rooms
            dorm.create_rooms()
            # Update max capacity in Students
            students_generator.max_capacity = dorm.single_rooms + dorm.double_rooms * 2
            print("\n🔄 Auto-adjusting students for new dorm setup...")
            students_generator.create_students()

        elif choice == "3":
            print("👋 Exiting Dorm Lottery System. Goodbye!")
            break

        else:
            print("❌ Invalid option, please choose 1–3.")

if __name__ == "__main__":
    main()