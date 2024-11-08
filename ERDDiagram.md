┌────────────┐         ┌──────────────┐         ┌─────────────┐         ┌───────────────┐
│   Users    │1      ─>│ Destinations │1      ─>│  Activities │1      ─>│   Expenses    │
│────────────│         │──────────────│         │─────────────│         │───────────────│
│ id (PK)    │         │ id (PK)      │         │ id (PK)     │         │ id (PK)       │
│ name       │         │ user_id (FK) │         │ destination │         │ activity_id   │
│ email      │         │ name         │         │ name        │         │ amount        │
│ created_at │         │ location     │         │ date        │         │ description   │
└────────────┘         │ description  │         │ time        │         │ date          │
                       │ created_at   │         │ cost        │         │ category      │
                       └──────────────┘         │ description │         │ created_at    │
                                                │ created_at  │         └───────────────┘
                                                └─────────────┘

## Tables Relationship
- Users → Destinations:

A one-to-many relationship where one user can have multiple destinations. This relationship is established via the user_id foreign key in the Destinations table, linking each destination to a specific user.

- Destinations → Activities:

 one-to-many relationship where each destination can have multiple activities. The destination_id foreign key in the Activities table establishes this link.
- Activities → Expenses:

Similarly, each activity can have multiple associated expenses, forming a one-to-many relationship. This relationship is represented by the activity_id foreign key in the Expenses table.