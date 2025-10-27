import pandas as pd
from rich.table import Table
from rich.console import Console

class ReportGenerator:
    def __init__(self, lottery, runs=1000, report_file="lottery_report.csv"):
        self.lottery = lottery
        self.runs = runs
        self.report_file = report_file
        self.console = Console()

    def run_simulation(self):
        # Count wins
        win_counts = {s.id: 0 for s in self.lottery.students}

        for _ in range(self.runs):
            singles, _ = self.lottery.run_lottery()
            for s in singles:
                win_counts[s.id] += 1

        # Build DataFrame
        data = []
        for s in self.lottery.students:
            times_won = win_counts[s.id]
            percentage = round((times_won / self.runs) * 100, 2)
            data.append([s.id, s.gender, times_won, percentage])

        df = pd.DataFrame(data, columns=["Student ID", "Gender", "Times Won", "Percentage"])
        df = df.sort_values(by="Times Won", ascending=False)

        # Save CSV
        df.to_csv(self.report_file, index=False)
        print(f"\n📊 Simulation complete! Report saved to {self.report_file}\n")

        # Print using rich
        table = Table(title=f"🎲 Lottery Results ({self.runs} runs)")

        table.add_column("Student ID", justify="center", style="cyan", no_wrap=True)
        table.add_column("Gender", justify="center", style="magenta")
        table.add_column("Times Won", justify="right", style="green")
        table.add_column("Percentage %", justify="right", style="yellow")

        for _, row in df.iterrows():
            table.add_row(str(row["Student ID"]),
                          str(row["Gender"]),
                          str(row["Times Won"]),
                          str(row["Percentage"]))

        self.console.print(table)
        return df