# Getting Started with the Wanderwise Travel Planning CLI App

Welcome to Wanderwise! This interactive command-line app is designed to help you organize travel destinations, track activities, and manage travel-related expenses, offering a streamlined experience for travel planning and budgeting.

---

## Features

- **View Destinations, Activities, and Expenses**: Browse a list of destinations, view associated activities, and track expenses by activity.
- **Add New Destinations, Activities, and Expenses**: Easily create new entries for each category, with data saved in an SQLite database.
- **Edit and Update Details**: Modify details of any destination, activity, or expense entry.
- **Delete Entries**: Remove destinations, activities, or expenses, with changes reflected in real time.
- **Input Validation and Feedback**: Ensures accurate data entry and provides guidance for corrections if needed.

---

## Installation

To run this project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/wanderwise.git
   ```

2. **Install dependencies**:
   ```bash
   pipenv install
   ```

3. **Run the CLI**:
   ```bash
   python cli.py
   ```
---

## Class Structure and Relationships

Wanderwise is built with object-oriented design and includes the following primary classes:

- **Destination**: Represents travel destinations, bridging activities and expenses.
- **Activity**: Represents events or plans tied to a destination.
- **Expense**: Tracks expenses associated with each activity.
- **User**: Manages user details and links to destinations for personalized trip management.

### Relationships

- **User → Destination**: One user can have multiple destinations.
- **Destination → Activity**: Each destination can include multiple activities.
- **Activity → Expense**: Each activity can have multiple related expenses.

---

## Credits

- **SQLAlchemy**: For ORM and database management.
- **click**: For CLI framework.
- **Faker**: For generating sample data.
- **sqlite3**: For lightweight database management.
- **rich**: For enhanced CLI visuals and formatting.

If you find this project helpful or want to learn more about its development, check out our team’s project journey!



