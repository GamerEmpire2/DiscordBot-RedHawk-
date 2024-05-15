CREATE TABLE IF NOT EXISTS [version] (
    [version] INTEGER
);

CREATE TABLE IF NOT EXISTS [users] (
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [username] TEXT NOT NULL,
    [email] TEXT NOT NULL,
    [discriminator] TEXT NOT NULL,
    [hashed_password] TEXT,
    [salt] TEXT,
    [token] TEXT,
    [token_created_at] DATETIME,
    [token_expires_at] DATETIME
);

CREATE TABLE IF NOT EXISTS [tokens] (
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [userId] TEXT NOT NULL,
    [token] TEXT,
    [token_created_at] DATETIME,
    [token_expires_at] DATETIME
);