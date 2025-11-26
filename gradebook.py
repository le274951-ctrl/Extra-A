import json
import os

FILENAME = "gradebook.json"


# -----------------------------
# Helpers
# -----------------------------
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def load_data():
    if not os.path.exists(FILENAME):
        return {}
    with open(FILENAME, "r") as f:
        return json.load(f)


def save_data(data):
    with open(FILENAME, "w") as f:
        json.dump(data, f, indent=4)


# -----------------------------
# Main Gradebook Functions
# -----------------------------
class Gradebook:
    def __init__(self):
        self.courses = load_data()

    def add_course(self):
        code = input("Course code: ").upper()
        if code in self.courses:
            print("❌ Course already exists!")
            return

        name = input("Course name: ")
        credit = int(input("Credits: "))
        semester = input("Semester (e.g. 2024A): ")
        score = float(input("Score (0–10): "))

        if not (0 <= score <= 10):
            print("❌ Invalid score!")
            return

        self.courses[code] = {
            "name": name,
            "credit": credit,
            "semester": semester,
            "score": score
        }
        print("✔ Course added!")

    def update_course(self):
        code = input("Enter course code to update: ").upper()
        if code not in self.courses:
            print("❌ Course not found!")
            return

        course = self.courses[code]

        print("Leave blank to keep current value.\n")
        name = input(f"Name ({course['name']}): ") or course["name"]
        credit = input(f"Credits ({course['credit']}): ")
        semester = input(f"Semester ({course['semester']}): ") or course["semester"]
        score = input(f"Score ({course['score']}): ")

        course["name"] = name
        if credit:
            course["credit"] = int(credit)
        course["semester"] = semester
        if score:
            course["score"] = float(score)

        print("✔ Course updated!")

    def delete_course(self):
        code = input("Enter course code to delete: ").upper()
        if code in self.courses:
            del self.courses[code]
            print("✔ Course deleted!")
        else:
            print("❌ Course not found!")

    def view_courses(self):
        if not self.courses:
            print("No courses yet.")
            return

        print("\n=== GRADEBOOK ===")
        print(f"{'Code':<10} {'Name':<25} {'Cr':<5} {'Semester':<10} {'Score':<5}")
        print("-" * 60)

        for code, c in self.courses.items():
            print(f"{code:<10} {c['name']:<25} {c['credit']:<5} {c['semester']:<10} {c['score']:<5}")

    def gpa_summary(self):
        if not self.courses:
            print("No courses available.")
            return

        total_points = 0
        total_credits = 0
        semester_data = {}

        for c in self.courses.values():
            pts = c["score"] * c["credit"]
            total_points += pts
            total_credits += c["credit"]

            sem = c["semester"]
            if sem not in semester_data:
                semester_data[sem] = {"pts": 0, "cr": 0}

            semester_data[sem]["pts"] += pts
            semester_data[sem]["cr"] += c["credit"]

        print("\n=== GPA SUMMARY ===")
        print(f"Overall GPA: {total_points / total_credits:.2f}")

        print("\nBy Semester:")
        for sem, d in semester_data.items():
            print(f"  {sem}: {d['pts'] / d['cr']:.2f}")


# -----------------------------
# Menu
# -----------------------------
def menu():
    print("\n====== STUDENT GRADEBOOK ======")
    print("1. Add course")
    print("2. Update course")
    print("3. Delete course")
    print("4. View gradebook")
    print("5. GPA summary")
    print("6. Exit")
    return input("Choose 1–6: ")


def main():
    gb = Gradebook()

    while True:
        clear_screen()
        choice = menu()

        if choice == "1":
            gb.add_course()
        elif choice == "2":
            gb.update_course()
        elif choice == "3":
            gb.delete_course()
        elif choice == "4":
            gb.view_courses()
        elif choice == "5":
            gb.gpa_summary()
        elif choice == "6":
            save_data(gb.courses)
            print("Goodbye!")
            break
        else:
            print("Invalid option!")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
