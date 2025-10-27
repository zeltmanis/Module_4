class DormRooms:
    def __init__(self):
        self.single_rooms = 0
        self.double_rooms = 0
        # Default values
        self.default_single = 40
        self.default_double = 30

    def get_room_input(self, room_type, default_value):
        """Ask user for a room number and validate it. Use default if empty."""
        while True:
            try:
                value = input(
                    f"Enter number of {room_type} rooms (0–999) or press Enter for default ({default_value}): ")

                # ✅ If no input → use default
                if value.strip() == "":
                    print(f"Using default value: {default_value}")
                    return default_value

                # ✅ Check if value is a number
                if not value.isdigit():
                    raise ValueError("Value must be a number.")

                value = int(value)

                # ✅ Check valid range
                if value < 0 or value > 999:
                    raise ValueError("Value must be between 0 and 999.")

                return value

            except ValueError as e:
                print(f"❌ Invalid input: {e}")
                print("Please try again.\n")

    def create_rooms(self):
        """Get user inputs for single and double rooms."""
        print("🏠 Room setup:")
        self.single_rooms = self.get_room_input("single", self.default_single)
        self.double_rooms = self.get_room_input("double", self.default_double)
        print(f"\n✅ Room setup complete!")
        print(f"Single rooms: {self.single_rooms}")
        print(f"Double rooms: {self.double_rooms}")


# ▶️ Run the program
if __name__ == "__main__":
    dorm = DormRooms()
    dorm.create_rooms()