from rich.table import Table
from rich.console import Console

class ReportGenerator:
    def __init__(self, lottery, runs=1000):
        self.lottery = lottery
        self.runs = runs
        self.console = Console()

    def run_simulation(self):
        """Run normal random lottery and generate report."""
        win_counts = {s.id: 0 for s in self.lottery.students}

        for _ in range(self.runs):
            singles, _ = self.lottery.run_lottery()
            for s in singles:
                win_counts[s.id] += 1

        # Build sorted results
        results = sorted(
            [(s.id, s.gender, win_counts[s.id], round((win_counts[s.id]/self.runs)*100,2))
             for s in self.lottery.students],
            key=lambda x: x[2], reverse=True
        )

        # Save nicely formatted text file
        with open("lottery_report_nice.txt", "w") as f:
            f.write(f"{'Student ID':<10} {'Gender':<6} {'Times Won':>10} {'Percentage':>10}\n")
            f.write("-"*40 + "\n")
            for sid, gender, times, perc in results:
                f.write(f"{sid:<10} {gender:<6} {times:>10} {perc:>10.2f}\n")

        # Print using rich
        table = Table(title=f"🎲 Lottery Results ({self.runs} runs)")
        table.add_column("Student ID", justify="center", style="cyan", no_wrap=True)
        table.add_column("Gender", justify="center", style="magenta")
        table.add_column("Times Won", justify="right", style="green")
        table.add_column("Percentage %", justify="right", style="yellow")
        for sid, gender, times, perc in results:
            table.add_row(sid, gender, str(times), str(perc))
        self.console.print(table)
        return results

    def run_gpa_weighted_simulation(self):
        """Run GPA-weighted lottery and generate report."""
        win_counts = {s.id: 0 for s in self.lottery.students}

        for _ in range(self.runs):
            singles, _ = self.lottery.run_gpa_weighted_lottery()
            for s in singles:
                win_counts[s.id] += 1

        # Build sorted results
        results = sorted(
            [(s.id, s.gender, round(s.gpa,2), int(s.gpa*10), win_counts[s.id],
              round((win_counts[s.id]/self.runs)*100,2))
             for s in self.lottery.students],
            key=lambda x: x[4], reverse=True
        )

        # Save nicely formatted text file
        with open("lottery_report_gpa_nice.txt", "w") as f:
            f.write(f"{'Student ID':<10} {'Gender':<6} {'GPA':>5} {'Tickets':>7} "
                    f"{'Times Won':>10} {'Percentage':>10}\n")
            f.write("-"*60 + "\n")
            for sid, gender, gpa, tickets, times, perc in results:
                f.write(f"{sid:<10} {gender:<6} {gpa:>5.2f} {tickets:>7} {times:>10} {perc:>10.2f}\n")

        # Print using rich
        table = Table(title=f"🎯 GPA-Weighted Lottery Results ({self.runs} runs)")
        table.add_column("Student ID", justify="center", style="cyan", no_wrap=True)
        table.add_column("Gender", justify="center", style="magenta")
        table.add_column("GPA", justify="right", style="green")
        table.add_column("Tickets", justify="right", style="blue")
        table.add_column("Times Won", justify="right", style="green")
        table.add_column("Percentage %", justify="right", style="yellow")
        for sid, gender, gpa, tickets, times, perc in results:
            table.add_row(sid, gender, str(gpa), str(tickets), str(times), str(perc))
        self.console.print(table)
        return results