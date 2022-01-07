-- DDL section, PART II

CREATE TABLE "users" (
    "id" SERIAL PRIMARY KEY,
    "username" VARCHAR(25) UNIQUE NOT NULL CHECK (LENGTH(TRIM("username"))<= 25),
    "last_login" TIMESTAMP);

CREATE INDEX ON "users"("username");

CREATE TABLE "topics" (
    "id" SERIAL PRIMARY KEY,
    "user_id" INT REFERENCES "users" ("id") ON DELETE SET NULL,
    "name" VARCHAR(30) UNIQUE NOT NULL CHECK (LENGTH(TRIM("name"))<= 30),
    "description" VARCHAR(500)
);
CREATE INDEX ON "topics"("name");

CREATE TABLE "posts" (
    "id" BIGSERIAL PRIMARY KEY,
    "user_id" INT REFERENCES "users" ("id") ON DELETE SET NULL,
    "topic_id" INT REFERENCES "topics" ("id") ON DELETE CASCADE,
    "title" VARCHAR(100) NOT NULL CHECK ((LENGTH(TRIM("title"))<= 100)),
    "time_posted" TIMESTAMP,
    "url" VARCHAR,
    "content" TEXT,
    CONSTRAINT "url_or_content" CHECK (("url" IS NULL AND "content" IS NOT NULL) OR ("url" IS NOT NULL AND "content" IS NULL))
);

CREATE INDEX ON "posts"("url");


CREATE TABLE "comments" (
    "id" BIGSERIAL PRIMARY KEY,
    "user_id" INT REFERENCES "users"("id") ON DELETE SET NULL,
    "post_id" BIGINT REFERENCES "posts"("id") ON DELETE CASCADE,
    "comment" TEXT NOT NULL,
    "time_commented" TIMESTAMP,
    "parent_comment_id" INT,
    CONSTRAINT "comment_thread" FOREIGN KEY ("parent_comment_id") REFERENCES "comments" ("id") ON DELETE CASCADE
);

CREATE TABLE "votes" (
    "user_id" INT REFERENCES "users"("id") ON DELETE SET NULL,
    "post_id" BIGINT REFERENCES "posts"("id") ON DELETE CASCADE,
    "vote" SMALLINT CHECK ("vote"=1 or "vote"=-1),
    CONSTRAINT "user_votes" PRIMARY KEY ("user_id","post_id")
);



--DML code section, Part III

INSERT INTO "users" ("username") SELECT DISTINCT username FROM bad_posts;

INSERT INTO "users" ("username")
    SELECT DISTINCT username
    FROM bad_comments
    ON CONFLICT ON CONSTRAINT "users_username_key"
    DO NOTHING;

INSERT INTO "topics" ("name") SELECT DISTINCT topic FROM bad_posts;

INSERT INTO "posts" ("title","user_id","topic_id", "url", "content")
    SELECT LEFT (bp.title,100),u.id, t.id, bp.url, bp.text_content
    FROM bad_posts bp
    JOIN users u
    ON bp.username=u.username
    JOIN topics t
    ON t.name=bp.topic;

INSERT INTO "comments" ("user_id", "post_id", "comment")
    SELECT u.id, p.id, bc.text_content
    FROM users u
    JOIN bad_comments bc
    ON u.username=bc.username
    JOIN bad_posts bp
    ON bp.id=bc.post_id
    JOIN posts p
    ON p.title=bp.title;

INSERT INTO "votes" ("user_id","post_id","vote")
    SELECT u.id, p.id, 1 AS upvote
    FROM
        (SELECT id, title, Regexp_split_to_table(upvotes,',') AS upvote_users
        FROM bad_posts)v1
    JOIN users u
    ON u.username = v1.upvote_users
    JOIN posts p
    ON p.title=v1.title
    ON CONFLICT ON CONSTRAINT "user_votes"
    DO NOTHING;

INSERT INTO "votes" ("user_id","post_id","vote")
    SELECT u.id, p.id, -1 AS downvote
    FROM
        (SELECT id, title,Regexp_split_to_table(downvotes,',') AS downvote_users
        FROM bad_posts)v2
    JOIN users u
    ON u.username = v2.downvote_users
    JOIN posts p
    ON p.title=v2.title
    ON CONFLICT ON CONSTRAINT "user_votes"
    DO NOTHING;
