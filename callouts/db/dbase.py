import json
import pymysql.cursors

from db.migrator import Migrator


############################################################################################################################
class DBase:

    ####################################################################################################################
    def __init__(self, credentials_file):
        with open(credentials_file) as f:
            credentials = json.load(f)
        info = (credentials["dbhost"], credentials["dbuser"],
                credentials["dbpass"], credentials["dbname"])

        self.migrator = Migrator(self)
        self.connection = pymysql.connect(host=info[0],
                                          user=info[1],
                                          password=info[2],
                                          db=info[3],
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)

    ####################################################################################################################
    def add_guild(self, guild_id):
        self.connection.ping(reconnect=True)
        with self.connection.cursor() as cursor:
            sql = """
                  INSERT INTO guilds (guild_id)
                  VALUES (%s)
                  ON DUPLICATE KEY UPDATE guild_id = %s;
                  """
            affected_count = cursor.execute(sql, (guild_id, guild_id))
        self.connection.commit()
        return affected_count

    ####################################################################################################################
    def add_migration_log(self, migration_name):
        self.connection.ping(reconnect=True)
        with self.connection.cursor() as cursor:
            sql = """
                  INSERT INTO migrations(script_name)
                  VALUES (%s);
                  """
            affected_count = cursor.execute(sql, (migration_name,))
        self.connection.commit()
        return affected_count

    ####################################################################################################################
    def add_user(self, user_id):
        self.connection.ping(reconnect=True)
        with self.connection.cursor() as cursor:
            sql = """
                  INSERT INTO users (user_id)
                  VALUES (%s)
                  ON DUPLICATE KEY UPDATE user_id = %s;
                  """
            affected_count = cursor.execute(sql, (user_id, user_id))
        self.connection.commit()
        return affected_count

    ####################################################################################################################
    def create_event(self, title, start_time, timezone, guild_id, description, max_members, user_id, utctime):
        self.connection.ping(reconnect=True)
        with self.connection.cursor() as cursor:
            sql = """
                  INSERT INTO events (title, start_time, timezone, guild_id, description, max_members, user_id, utctime)
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                  ON DUPLICATE KEY UPDATE title = %s;
                  """
            affected_count = cursor.execute(sql, (title, start_time, timezone, guild_id, description, max_members, user_id, utctime, title))
        self.connection.commit()
        return affected_count

    ####################################################################################################################
    def create_migrations_table(self):
        self.connection.ping(reconnect=True)
        with self.connection.cursor() as cursor:
            sql = """
                  CREATE TABLE migrations (
                  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                  executed_on timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                  script_name VARCHAR(80) NOT NULL);
                  """
            cursor.execute(sql)
        self.connection.commit()

    ####################################################################################################################
    def delete_event(self, guild_id, title):
        self.connection.ping(reconnect=True)
        with self.connection.cursor() as cursor:
            sql = """
                  DELETE FROM events
                  WHERE guild_id = %s
                  AND title = %s;
                  """
            affected_count = cursor.execute(sql, (guild_id, title))
        self.connection.commit()
        return affected_count

    ####################################################################################################################
    def execute_sql(self, sql):
        self.connection.ping(reconnect=True)
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
        self.connection.commit()

    ####################################################################################################################
    def get_cleanup(self, guild_id):
        self.connection.ping(reconnect=True)
        with self.connection.cursor() as cursor:
            sql = """
                  SELECT clear_spam
                  FROM guilds
                  WHERE guild_id = %s
                  """
            cursor.execute(sql, (guild_id,))
            result = cursor.fetchone()
        return result

    ####################################################################################################################
    def get_d2_info(self, user_id):
        self.connection.ping(reconnect=True)
        with self.connection.cursor() as cursor:
            sql = """
                  SELECT platform, bliz_id, xbox_id, psn_id, bliz_name, xbox_name, psn_name
                  FROM users
                  WHERE user_id = %s
                  """
            cursor.execute(sql, (user_id,))
            result = cursor.fetchone()
        return result

    ####################################################################################################################
    def get_event(self, guild_id, title):
        self.connection.ping(reconnect=True)
        with self.connection.cursor() as cursor:
            sql = """
                  SELECT title as event_title, description, start_time, timezone, user_id, (
                    SELECT GROUP_CONCAT(DISTINCT user_id ORDER BY last_updated)
                    FROM user_event
                    WHERE user_event.guild_id = %s
                    AND user_event.title = %s
                    AND user_event.attending = 1)
                    AS accepted, (
                    SELECT GROUP_CONCAT(DISTINCT user_id ORDER BY last_updated)
                    FROM user_event
                    WHERE user_event.guild_id = %s
                    AND user_event.title = %s
                    AND user_event.attending = 0)
                    AS declined, (
                    SELECT GROUP_CONCAT(DISTINCT user_id ORDER BY last_updated)
                    FROM user_event
                    WHERE user_event.guild_id = %s
                    AND user_event.title = %s
                    AND user_event.attending = 2)
                    AS maybe, (
                    SELECT GROUP_CONCAT(DISTINCT user_id ORDER BY last_updated)
                    FROM user_event
                    WHERE user_event.guild_id = %s
                    AND user_event.title = %s
                    AND user_event.confirmed = 1)
                    AS confirmed, (
                    SELECT GROUP_CONCAT(DISTINCT user_id ORDER BY last_updated)
                    FROM user_event
                    WHERE user_event.guild_id = %s
                    AND user_event.title = %s
                    AND user_event.confirmed = 2)
                    AS rejected,
                    max_members
                  FROM events
                  WHERE guild_id = %s
                  AND title = %s;
                  """
            cursor.execute(sql, (guild_id, title, guild_id, title, guild_id, title, guild_id, title, guild_id, title, guild_id, title))
            result = cursor.fetchone()
        return result

    ####################################################################################################################
    def get_event_creator(self, guild_id, title):
        self.connection.ping(reconnect=True)
        with self.connection.cursor() as cursor:
            sql = """
                  SELECT user_id
                  FROM events
                  WHERE guild_id = %s
                  AND title = %s;
                  """
            cursor.execute(sql, (guild_id, title))
            result = cursor.fetchone()
        return result

    ####################################################################################################################
    def get_event_delete_role_id(self, guild_id):
        self.connection.ping(reconnect=True)
        with self.connection.cursor() as cursor:
            sql = """
                  SELECT event_delete_role_id
                  FROM guilds
                  WHERE guild_id = %s
                  """
            cursor.execute(sql, (guild_id,))
            result = cursor.fetchone()
        return result

    ####################################################################################################################
    def get_event_role_id(self, guild_id):
        self.connection.ping(reconnect=True)
        with self.connection.cursor() as cursor:
            sql = """
                  SELECT event_role_id
                  FROM guilds
                  WHERE guild_id = %s
                  """
            cursor.execute(sql, (guild_id,))
            result = cursor.fetchone()
        return result

    ####################################################################################################################
    def get_events(self, guild_id):
        self.connection.ping(reconnect=True)
        with self.connection.cursor() as cursor:
            sql = """
                  SELECT title as event_title, description, start_time, timezone, user_id, (
                    SELECT GROUP_CONCAT(DISTINCT user_id ORDER BY last_updated)
                    FROM user_event
                    WHERE user_event.guild_id = %s
                    AND user_event.title = event_title
                    AND user_event.attending = 1)
                    AS accepted, (
                    SELECT GROUP_CONCAT(DISTINCT user_id ORDER BY last_updated)
                    FROM user_event
                    WHERE user_event.guild_id = %s
                    AND user_event.title = event_title
                    AND user_event.attending = 0)
                    AS declined, (
                    SELECT GROUP_CONCAT(DISTINCT user_id ORDER BY last_updated)
                    FROM user_event
                    WHERE user_event.guild_id = %s
                    AND user_event.title = event_title
                    AND user_event.attending = 2)
                    AS maybe,
                    max_members,
                    utctime
                  FROM events
                  WHERE events.guild_id = %s
                  GROUP BY title, description, start_time, timezone
                  ORDER BY start_time DESC;
                  """
            cursor.execute(sql, (guild_id, guild_id, guild_id, guild_id))
            result = cursor.fetchall()
        return result

    ####################################################################################################################
    def get_guilds(self):
        self.connection.ping(reconnect=True)
        with self.connection.cursor() as cursor:
            sql = """
                  SELECT * FROM guilds;
                  """
            cursor.execute(sql)
            result = cursor.fetchall()
        return result

    ####################################################################################################################
    def get_last_executed_migration(self):
        self.connection.ping(reconnect=True)
        with self.connection.cursor() as cursor:
            sql = """
                  SELECT script_name FROM migrations ORDER BY `id` DESC
                  """
            cursor.execute(sql)
            result = cursor.fetchone()
        return result

    ####################################################################################################################
    def get_platform(self, user_id):
        self.connection.ping(reconnect=True)
        with self.connection.cursor() as cursor:
            sql = """
                  SELECT platform
                  FROM users
                  WHERE user_id = %s
                  """
            cursor.execute(sql)
            result = cursor.fetchone()
        return result

    ####################################################################################################################
    def get_prefix(self, guild_id):
        self.connection.ping(reconnect=True)
        with self.connection.cursor() as cursor:
            sql = """
                  SELECT prefix
                  FROM guilds
                  WHERE guild_id = %s;
                  """
            cursor.execute(sql, (guild_id,))
            result = cursor.fetchone()
        return result

    ####################################################################################################################
    def get_roster(self, guild_id):
        self.connection.ping(reconnect=True)
        with self.connection.cursor() as cursor:
            sql = """
                  SELECT user_id, role, timezone
                  FROM roster
                  WHERE (role != '' OR timezone != '')
                  AND guild_id = %s
                  ORDER BY role;
                  """
            cursor.execute(sql, (guild_id,))
            result = cursor.fetchall()
        return result

    ####################################################################################################################
    def remove_guild(self, guild_id):
        self.connection.ping(reconnect=True)
        with self.connection.cursor() as cursor:
            sql = """
                  DELETE FROM guilds
                  WHERE guild_id = %s;
                  """
            affected_count = cursor.execute(sql, (guild_id,))
        self.connection.commit()
        return affected_count

    ####################################################################################################################
    def remove_user(self, user_id):
        self.connection.ping(reconnect=True)
        with self.connection.cursor() as cursor:
            sql = """
                  DELETE FROM users
                  WHERE user_id = %s;
                  """
            affected_count = cursor.execute(sql, (user_id,))
        self.connection.commit()
        return affected_count

    ####################################################################################################################
    def set_event_delete_role_id(self, guild_id, event_delete_role_id):
        self.connection.ping(reconnect=True)
        with self.connection.cursor() as cursor:
            sql = """
                  UPDATE guilds
                  SET event_delete_role_id = %s
                  WHERE guild_id = %s;
                  """
            affected_count = cursor.execute(sql, (event_delete_role_id, guild_id))
        self.connection.commit()
        return affected_count

    ####################################################################################################################
    def set_event_role_id(self, guild_id, event_role_id):
        self.connection.ping(reconnect=True)
        with self.connection.cursor() as cursor:
            sql = """
                  UPDATE guilds
                  SET event_role_id = %s
                  WHERE guild_id = %s;
                  """
            affected_count = cursor.execute(sql, (event_role_id, guild_id))
        self.connection.commit()
        return affected_count

    ####################################################################################################################
    def set_prefix(self, guild_id, prefix):
        self.connection.ping(reconnect=True)
        with self.connection.cursor() as cursor:
            sql = """
                  UPDATE guilds
                  SET prefix = %s
                  WHERE guild_id = %s;
                  """
            affected_count = cursor.execute(sql, (prefix, guild_id))
        self.connection.commit()
        return affected_count

    ####################################################################################################################
    def table_exists(self, table_name):
        self.connection.ping(reconnect=True)
        with self.connection.cursor() as cursor:
            sql = """
                  SHOW TABLES LIKE %s;
                  """
            affected_count = cursor.execute(sql, (table_name,))
        self.connection.commit()
        return affected_count

    ####################################################################################################################
    def toggle_cleanup(self, guild_id):
        self.connection.ping(reconnect=True)
        with self.connection.cursor() as cursor:
            sql = """
                  UPDATE guilds
                  SET clear_spam = !clear_spam
                  WHERE guild_id = %s
                  """
            affected_count = cursor.execute(sql, (guild_id,))
        self.connection.commit()
        return affected_count

    ####################################################################################################################
    def update_attendance(self, user_id, guild_id, attending, title, last_updated, confirmed):
        affected_count = 0
        self.connection.ping(reconnect=True)
        with self.connection.cursor() as cursor:
            check_attend = """SELECT attending, confirmed
                              FROM user_event
                              WHERE guild_id = %s
                              AND user_id = %s
                              AND title = %s;"""
            cursor.execute(check_attend, (guild_id, user_id, title))
            current_attending = cursor.fetchone()
            if current_attending is None or current_attending["attending"] != attending:
                sql = """
                      INSERT INTO user_event (user_id, guild_id, title, attending, last_updated, confirmed)
                      VALUES (%s, %s, %s, %s, %s, %s)
                      ON DUPLICATE KEY UPDATE attending = %s, last_updated = %s, confirmed = %s;
                      """
                affected_count = cursor.execute(sql, (user_id, guild_id, title, attending, last_updated, confirmed, attending, last_updated, confirmed))
                self.connection.commit()
            elif current_attending is not None and current_attending["attending"] == 1 and confirmed != 0:
                update_confirm = """UPDATE user_event
                                    SET confirmed = %s
                                    WHERE guild_id = %s
                                    AND user_id = %s
                                    AND title = %s;"""
                affected_count = cursor.execute(update_confirm, (confirmed, guild_id, user_id, title))
                self.connection.commit()
        return affected_count

    ####################################################################################################################
    def get_user_event_attendance(self, user_id, guild_id, title):
        self.connection.ping(reconnect=True)
        with self.connection.cursor() as cursor:
            sql = """SELECT *
                     FROM user_event
                     WHERE guild_id = %s
                     AND user_id = %s
                     AND title = %s;"""
            cursor.execute(sql, (guild_id, user_id, title))
            current_attending = cursor.fetchone()
            return current_attending

    ####################################################################################################################
    def add_user_event_attempt(self, user_id, guild_id, title, reset=False):
        self.connection.ping(reconnect=True)
        current = 1
        if reset is False:
            current = self.get_user_event_attendance(user_id, guild_id, title)
            current = current.get("attempts") + 1
        with self.connection.cursor() as cursor:
            sql = """UPDATE user_event
                     SET attempts = %s
                     WHERE guild_id = %s
                     AND user_id = %s
                     AND title = %s;"""
            affected_count =cursor.execute(sql, (current, guild_id, user_id, title))
            self.connection.commit()
            return affected_count

    ####################################################################################################################
    def get_user_by_discord_id(self, user_id):
        self.connection.ping(reconnect=True)
        with self.connection.cursor() as cursor:
            sql = "select * from users WHERE user_id = %s;"
            cursor.execute(sql, (user_id))
            user = cursor.fetchone()
            return user

    ####################################################################################################################
    def get_user_by_platform_id(self, platform, user_id):
        self.connection.ping(reconnect=True)
        id_type = ""
        if platform == 1:
            id_type = "xbox_id"  
        elif platform == 2:
            id_type = "psn_id" 
        elif platform == 3:
            id_type = "steam_id" 
        elif platform == 5:
            id_type = "stadia_id" 
        sql = f"select * from users where platform=%s and {id_type}=%s"
        with self.connection.cursor() as cursor:
            # sql = "select * from users WHERE user_id = %s;"
            cursor.execute(sql, (platform, user_id))
            user = cursor.fetchone()
            return user

    ####################################################################################################################
    def update_display_names(self, user_id, bungie_name, steam_name, xbox_name, psn_name, stadia_name):
        self.connection.ping(reconnect=True)
        with self.connection.cursor() as cursor:
            sql = """
                  UPDATE users
                  SET bungie_name = %s, steam_name = %s, xbox_name = %s, psn_name = %s, stadia_name = %s
                  WHERE user_id = %s;
                  """
            affected_count = cursor.execute(sql, (bungie_name, steam_name, xbox_name, psn_name, stadia_name, user_id))
        self.connection.commit()
        return affected_count

    ####################################################################################################################
    def update_membership_ids(self, user_id, steam_id, xbox_id, psn_id, stadia_id):
        self.connection.ping(reconnect=True)
        with self.connection.cursor() as cursor:
            sql = """
                  UPDATE users
                  SET steam_id = %s, xbox_id = %s, psn_id = %s, stadia_id = %s
                  WHERE user_id = %s;
                  """
            affected_count = cursor.execute(sql, (steam_id, xbox_id, psn_id, stadia_id, user_id))
        self.connection.commit()
        return affected_count

    ####################################################################################################################
    def update_platform(self, user_id, platform):
        self.connection.ping(reconnect=True)
        with self.connection.cursor() as cursor:
            sql = """
                  UPDATE users
                  SET platform = %s
                  WHERE user_id = %s;
                  """
            affected_count = cursor.execute(sql, (platform, user_id))
        self.connection.commit()
        return affected_count

    ####################################################################################################################
    def update_registration(self, bungie_id, user_id):
        self.connection.ping(reconnect=True)
        with self.connection.cursor() as cursor:
            sql = """
                  INSERT into users (bungie_id, user_id)
                  VALUES (%s, %s)
                  ON DUPLICATE KEY UPDATE bungie_id = %s;
                  """
            affected_count = cursor.execute(sql, (bungie_id, user_id, bungie_id))
        self.connection.commit()
        return affected_count

    ####################################################################################################################
    def update_role(self, user_id, role, guild_id):
        self.connection.ping(reconnect=True)
        with self.connection.cursor() as cursor:
            sql = """
                   INSERT INTO roster (user_id, role, guild_id)
                   VALUES (%s, %s, %s)
                   ON DUPLICATE KEY UPDATE role = %s;
                   """
            affected_count = cursor.execute(sql, (user_id, role, guild_id, role))
        self.connection.commit()
        return affected_count

    ####################################################################################################################
    def update_timezone(self, user_id, timezone, guild_id):
        self.connection.ping(reconnect=True)
        with self.connection.cursor() as cursor:
            sql = """
                   INSERT INTO roster (user_id, timezone, guild_id)
                   VALUES (%s, %s, %s)
                   ON DUPLICATE KEY UPDATE timezone = %s;
                   """
            affected_count = cursor.execute(sql, (user_id, timezone, guild_id, timezone))
        self.connection.commit()
        return affected_count
