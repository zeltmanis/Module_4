from dorm_rooms import DormRooms
from students import Students, Student
from lottery import DormLottery

def main():
    print("🎓 Welcome to the Dorm Room Builder System\n")

    # Step 1: Create dorm rooms
    dorm = DormRooms()
    dorm.create_rooms()

    # Step 2: Create students
    students_generator = Students(dorm.single_rooms, dorm.double_rooms)
    students_generator.create_students()

    # Step 3: Generate actual Student objects
    students = []
    for i in range(1, students_generator.female_students + 1):
        students.append(Student(f"F{i:03}", "F"))
    for i in range(1, students_generator.male_students + 1):
        students.append(Student(f"M{i:03}", "M"))

    # Step 4: Run lottery
    lottery = DormLottery(students, dorm.single_rooms, dorm.double_rooms)
    singles, doubles = lottery.run_lottery()

    # Step 5: Print results
    lottery.print_lottery(singles, doubles)

    # Step 6: Optional summary
    print("\n📋 Setup Summary:")
    print(f"Total students: {len(students)}")
    print(f"Single rooms: {dorm.single_rooms}")
    print(f"Double rooms: {dorm.double_rooms}")
    print("✅ Lottery complete!")

if __name__ == "__main__":
    main()