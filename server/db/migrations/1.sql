CREATE TABLE IF NOT EXISTS [version] (
    [version] INTEGER
);

CREATE TABLE IF NOT EXISTS [users] (
    [id] INTEGER PRIMARY KEY,
    [username] TEXT NOT NULL,
    [discriminator] TEXT NOT NULL,
    [hashed_password] TEXT,
    [salt] TEXT,
    [token] TEXT,
    [token_created_at] DATETIME,
    [token_expires_at] DATETIME
);

CREATE TABLE IF NOT EXISTS [tokens] (
    [id] INTEGER PRIMARY KEY,
    [userId] TEXT NOT NULL,
    [discriminator] TEXT NOT NULL,
    [token] TEXT,
    [token_created_at] DATETIME,
    [token_expires_at] DATETIME
);