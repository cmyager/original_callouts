CREATE TABLE guilds (
	guild_id BIGINT NOT NULL,
	prefix VARCHAR(5) NOT NULL DEFAULT '!',
	clear_spam BOOLEAN NOT NULL DEFAULT 0,
	event_role_id BIGINT,
	event_delete_role_id BIGINT,
	PRIMARY KEY(guild_id)
);

CREATE TABLE users (
	user_id BIGINT NOT NULL,
	bungie_id BIGINT,
	steam_id BIGINT,
	xbox_id BIGINT,
	psn_id BIGINT,
	stadia_id BIGINT,
	bungie_name VARCHAR(40),
	steam_name VARCHAR(40),
	xbox_name VARCHAR(40),
	psn_name VARCHAR(40),
	stadia_name VARCHAR(40),
	platform INT,
	PRIMARY KEY (user_id)
);

CREATE TABLE events (
	guild_id BIGINT NOT NULL,
	start_time DATETIME NOT NULL,
	timezone VARCHAR(20) NOT NULL,
	title VARCHAR(256) NOT NULL,
	description VARCHAR(1000),
	max_members INT NOT NULL DEFAULT 0,
	user_id BIGINT,
	utctime DATETIME NOT NULL,
	PRIMARY KEY (guild_id, title),
	FOREIGN KEY (guild_id) REFERENCES guilds(guild_id)
		ON DELETE CASCADE
);

CREATE TABLE user_event (
	user_id BIGINT NOT NULL,
	guild_id BIGINT NOT NULL,
	title VARCHAR(256) NOT NULL,
	attending INT NOT NULL,
	last_updated DATETIME NOT NULL,
	confirmed INT NOT NULL DEFAULT 0,
	attempts INT NOT NULL DEFAULT 1,
	PRIMARY KEY (user_id, guild_id, title),
	FOREIGN KEY (guild_id, title) REFERENCES events(guild_id, title)
		ON DELETE CASCADE,
	FOREIGN KEY (user_id) REFERENCES users(user_id)
	  ON DELETE CASCADE
);

CREATE TABLE roster (
	user_id BIGINT NOT NULL,
	guild_id BIGINT NOT NULL,
	role VARCHAR(10),
	timezone VARCHAR(6),
	PRIMARY KEY (user_id, guild_id),
	FOREIGN KEY (user_id) REFERENCES users(user_id)
	  ON DELETE CASCADE,
	FOREIGN KEY (guild_id) REFERENCES guilds(guild_id)
		ON DELETE CASCADE
);

-- FOR DEBUGGING
insert into guilds (guild_id, prefix, clear_spam, event_delete_role_id) values (765038177605386240, '!', 1, 772177221153849384);
insert into guilds (guild_id, prefix, clear_spam) values (772224269865320470, '!', 1);