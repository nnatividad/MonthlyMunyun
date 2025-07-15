CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
);

CREATE TABLE Budgets (
    budget_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    auto_budget NUMERIC,
    entertainment NUMERIC,
    bills NUMERIC,
    saving NUMERIC,
    debt NUMERIC,
    transportation NUMERIC,
    other NUMERIC,
    FOREIGN KEY(user_id) REFERENCES Users(id)
);

CREATE TABLE Activity (
    activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    amount NUMERIC,
    category TEXT,
    date DATETIME,
    FOREIGN KEY(user_id) REFERENCES Users(id)
);
