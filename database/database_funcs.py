import aiosqlite


class Database:
    _instance = None

    def __new__(cls, db_name):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.db_name = db_name
            cls._instance.connection = None
            cls._instance.cursor = None
        return cls._instance

    async def init(self):
        if self.connection is None:
            self.connection = await aiosqlite.connect(self.db_name)
            self.cursor = await self.connection.cursor()
            await self.create_users_table()

    async def create_users_table(self):
        await self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                city TEXT NOT NULL,
                is_ban TEXT NOT NULL
            )
            """
        )
        await self.connection.commit()

    async def add_user(self, user_id, city):
        if self.cursor is None:
            raise Exception("Database not initialized. Call 'init' method first.")
        await self.cursor.execute(
            "INSERT INTO users (user_id, city, is_ban) VALUES (?, ?, ?)",
            (user_id, city, "no"),
        )
        await self.connection.commit()

    async def get_user(self, user_id):
        if self.cursor is None:
            raise Exception("Database not initialized. Call 'init' method first.")
        await self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = await self.cursor.fetchone()
        if user:
            return {
                "id": user[0],
                "user_id": user[1],
                "city": user[2],
                "is_ban": user[3],
            }
        return None

    async def delete_user(self, user_id):
        if self.cursor is None:
            raise Exception("Database not initialized. Call 'init' method first.")
        await self.cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        await self.connection.commit()

    async def ban_user(self, user_id):
        if self.cursor is None:
            raise Exception("Database not initialized. Call 'init' method first.")
        await self.cursor.execute(
            "UPDATE users SET is_ban = 'yes' WHERE user_id = ?", (user_id,)
        )
        await self.connection.commit()

    async def unban_user(self, user_id):
        if self.cursor is None:
            raise Exception("Database not initialized. Call 'init' method first.")
        await self.cursor.execute(
            "UPDATE users SET is_ban = 'no' WHERE user_id = ?", (user_id,)
        )
        await self.connection.commit()

    async def get_all_user_ids(self):
        if self.cursor is None:
            raise Exception("Database not initialized. Call 'init' method first.")
        await self.cursor.execute("SELECT user_id FROM users")
        rows = await self.cursor.fetchall()
        return [row[0] for row in rows]

    async def close(self):
        if self.connection:
            await self.connection.close()
