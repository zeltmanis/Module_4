from dorm_rooms import DormRooms
from students import Students, Student
from lottery import DormLottery
from report import ReportGenerator
import pandas as pd
from rich.table import Table
from rich.console import Console
import random

def get_lottery_runs():
    """Ask user how many times to run the lottery using menu choices."""
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

    dorm = DormRooms()
    dorm.create_rooms()

    students_generator = Students(dorm.single_rooms, dorm.double_rooms)
    students_generator.create_students()

    last_random_results = None
    last_gpa_results = None
    console = Console()

    while True:
        print("\n===== Lottery Menu =====")
        print("1. Run random lottery / generate report")
        print("2. Run GPA-influenced lottery / generate report")
        print("3. Adjust dorm rooms (auto adjusts students)")
        print("4. Compare last random vs GPA-weighted lottery runs")
        print("5. Quit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            runs = get_lottery_runs()
            students = [Student(f"F{i:03}", "F") for i in range(1, students_generator.female_students + 1)]
            students += [Student(f"M{i:03}", "M") for i in range(1, students_generator.male_students + 1)]
            lottery = DormLottery(students, dorm.single_rooms, dorm.double_rooms)
            report = ReportGenerator(lottery, runs=runs)
            last_random_results = report.run_simulation()  # list of tuples for comparison

        elif choice == "2":
            runs = get_lottery_runs()
            students = [Student(f"F{i:03}", "F") for i in range(1, students_generator.female_students + 1)]
            students += [Student(f"M{i:03}", "M") for i in range(1, students_generator.male_students + 1)]
            for s in students:
                s.gpa = round(random.uniform(0.0, 10.0), 2)
            lottery = DormLottery(students, dorm.single_rooms, dorm.double_rooms)
            report = ReportGenerator(lottery, runs=runs)
            last_gpa_results = report.run_gpa_weighted_simulation()  # list of tuples

        elif choice == "3":
            dorm.create_rooms()
            students_generator.max_capacity = dorm.single_rooms + dorm.double_rooms * 2
            print("\n🔄 Auto-adjusting students for new dorm setup...")
            students_generator.create_students()

        elif choice == "4":
            if last_random_results is None or last_gpa_results is None:
                print("❌ Please run both random and GPA-weighted lotteries first!")
                continue

            # Convert lists of tuples to DataFrames for comparison
            df_random = pd.DataFrame(last_random_results, columns=["Student ID", "Gender", "Times Won", "Percentage"])
            df_gpa = pd.DataFrame(last_gpa_results, columns=["Student ID", "Gender", "GPA", "Tickets", "Times Won", "Percentage"])

            comparison = pd.merge(df_random, df_gpa, on="Student ID", suffixes=("_random", "_gpa"))
            comparison["Times Won Diff"] = comparison["Times Won_gpa"] - comparison["Times Won_random"]
            comparison["Percentage Diff"] = comparison["Percentage_gpa"] - comparison["Percentage_random"]
            comparison_sorted = comparison.sort_values(by="Times Won Diff", ascending=False)

            # Save nicely formatted TXT
            with open("lottery_comparison.txt", "w") as f:
                f.write(f"{'Student ID':<12} {'GPA':>6} {'Times Won (R)':>15} {'Times Won (GPA)':>18} "
                        f"{'Diff':>10} {'% Diff':>10}\n")
                f.write("-"*75 + "\n")
                for _, row in comparison_sorted.iterrows():
                    f.write(f"{row['Student ID']:<12} {row['GPA']:>6.2f} {row['Times Won_random']:>15} "
                            f"{row['Times Won_gpa']:>18} {row['Times Won Diff']:>10} "
                            f"{row['Percentage Diff']:>10.2f}\n")

            print("\n📊 Comparison complete! Report saved to lottery_comparison.txt\n")

            # Display with Rich
            table = Table(title="🎯 Lottery Comparison: Random vs GPA-weighted")
            table.add_column("Student ID", justify="center", style="cyan")
            table.add_column("Times Won (R)", justify="right", style="green")
            table.add_column("Times Won (GPA)", justify="right", style="blue")
            table.add_column("Diff", justify="right", style="magenta")
            table.add_column("% Diff", justify="right", style="yellow")

            for _, row in comparison_sorted.iterrows():
                table.add_row(
                    str(row["Student ID"]),
                    str(row["Times Won_random"]),
                    str(row["Times Won_gpa"]),
                    str(row["Times Won Diff"]),
                    f"{row['Percentage Diff']:.2f}"
                )

            console.print(table)

        elif choice == "5":
            print("👋 Exiting Dorm Lottery System. Goodbye!")
            break

        else:
            print("❌ Invalid option, please choose 1–5.")

if __name__ == "__main__":
    main()