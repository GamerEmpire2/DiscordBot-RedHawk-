CREATE TABLE IF NOT EXISTS [version] (
    [version] INTEGER
);

CREATE TABLE IF NOT EXISTS [users] (
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [username] TEXT NOT NULL,
    [email] TEXT NOT NULL,
    [hashed_password] TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS [roles] (
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [role] TEXT NOT NULL,
    [description] TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS [user_roles] (
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [userId] INTEGER NOT NULL,
    [roleId] TEXT NOT NULL,
    [value] INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS [tokens] (
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [userId] TEXT NOT NULL,
    [token] TEXT,
    [token_created_at] DATETIME,
    [token_expires_at] DATETIME
);
