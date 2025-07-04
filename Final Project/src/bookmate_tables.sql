CREATE DATABASE IF NOT EXISTS bookmate OWNER postgres;
-- Extensión necesaria para UUIDv7 (PostgreSQL 14+)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tablas de tipos/catálogos
CREATE TABLE "user_type" (
  "user_type_id" SERIAL PRIMARY KEY NOT NULL,
  "description" VARCHAR(40) NOT NULL
);

CREATE TABLE "plan_type" (
  "plan_type_id" SERIAL PRIMARY KEY NOT NULL,
  "description" VARCHAR(40) NOT NULL
);

CREATE TABLE "payment_status_type" (
  "payment_status_type_id" SERIAL PRIMARY KEY NOT NULL,
  "description" VARCHAR(40) NOT NULL
);

CREATE TABLE "notification_type" (
  "notification_type_id" SERIAL PRIMARY KEY NOT NULL,
  "description" VARCHAR(40) NOT NULL
);

CREATE TABLE "genre_type" (
  "genre_type_id" SERIAL PRIMARY KEY NOT NULL,
  "description" VARCHAR(40) NOT NULL
);

CREATE TABLE "country" (
  "country_id" SERIAL PRIMARY KEY,
  "name" VARCHAR(100) NOT NULL,
  "iso_code" CHAR(2)
);

CREATE TABLE "tag" (
  "tag_id" SERIAL PRIMARY KEY,
  "description" VARCHAR(40) NOT NULL
);

-- Tablas principales con UUIDv7
CREATE TABLE "user" (
  "user_id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "password" VARCHAR(40) NOT NULL,
  "name" VARCHAR(255) NOT NULL,
  "profile_picture" BYTEA,
  "is_premium" BOOLEAN NOT NULL,
  "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "user_type" INT NOT NULL,
  FOREIGN KEY ("user_type") REFERENCES "user_type" ("user_type_id")
);

CREATE TABLE "author" (
  "author_id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "name" VARCHAR(255) NOT NULL,
  "biography" TEXT NOT NULL,
  "nationality" INT NOT NULL,
  FOREIGN KEY ("nationality") REFERENCES "country" ("country_id")
);

CREATE TABLE "publisher" (
  "publisher_id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "name" VARCHAR(100) NOT NULL,
  "country_id" INT,
  "founded_year" INT,
  "website" VARCHAR(255),
  "description" TEXT,
  FOREIGN KEY ("country_id") REFERENCES "country" ("country_id")
);

CREATE TABLE "book" (
  "book_id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "title" VARCHAR(40) NOT NULL,
  "author" UUID NOT NULL,
  "synopsis" TEXT NOT NULL,
  "cover_image" BYTEA,
  "language" VARCHAR(20) NOT NULL,
  "is_audiobook" BOOLEAN NOT NULL,
  "file_url" VARCHAR(255) NOT NULL,
  "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP,
  "uploaded_by" UUID NOT NULL,
  "publisher_id" UUID,
  "published_year" TIMESTAMP,
  "isbn" VARCHAR(20),
  FOREIGN KEY ("author") REFERENCES "author" ("author_id"),
  FOREIGN KEY ("uploaded_by") REFERENCES "user" ("user_id"),
  FOREIGN KEY ("publisher_id") REFERENCES "publisher" ("publisher_id")
);

CREATE TABLE "audiobook" (
  "book_id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "duration" INT NOT NULL,
  "narrator" VARCHAR(40) NOT NULL,
  "audio_file_url" VARCHAR(255) NOT NULL,
  FOREIGN KEY ("book_id") REFERENCES "book" ("book_id")
);

CREATE TABLE "review" (
  "review_id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "rating" INT NOT NULL CHECK ("rating" BETWEEN 1 AND 5),
  "comment" VARCHAR(255),
  "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "user_id" UUID NOT NULL,
  "book_id" UUID NOT NULL,
  FOREIGN KEY ("user_id") REFERENCES "user" ("user_id"),
  FOREIGN KEY ("book_id") REFERENCES "book" ("book_id")
);

CREATE TABLE "favorite" (
  "favorite_id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "user_id" UUID NOT NULL,
  "book_id" UUID NOT NULL,
  FOREIGN KEY ("user_id") REFERENCES "user" ("user_id"),
  FOREIGN KEY ("book_id") REFERENCES "book" ("book_id")
);

CREATE TABLE "user_book" (
  "user_id" UUID NOT NULL,
  "book_id" UUID NOT NULL,
  "pages_read" INT NOT NULL DEFAULT 0,
  "minutes_listened" INT NOT NULL DEFAULT 0,
  "last_accessed" TIMESTAMP,
  PRIMARY KEY ("user_id", "book_id"),
  FOREIGN KEY ("user_id") REFERENCES "user" ("user_id"),
  FOREIGN KEY ("book_id") REFERENCES "book" ("book_id")
);

CREATE TABLE "follow" (
  "follow_id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "follower_id" UUID NOT NULL,
  "followed_id" UUID NOT NULL,
  FOREIGN KEY ("follower_id") REFERENCES "user" ("user_id"),
  FOREIGN KEY ("followed_id") REFERENCES "user" ("user_id"),
  CONSTRAINT no_self_follow CHECK ("follower_id" != "followed_id")
);

CREATE TABLE "reading_list" (
  "list_id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "name" VARCHAR(40) NOT NULL,
  "description" VARCHAR(255),
  "created_by" UUID NOT NULL,
  "is_public" BOOLEAN NOT NULL DEFAULT false,
  "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY ("created_by") REFERENCES "user" ("user_id")
);

CREATE TABLE "reading_list_item" (
  "list_id" UUID NOT NULL,
  "book_id" UUID NOT NULL,
  "added_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY ("list_id", "book_id"),
  FOREIGN KEY ("list_id") REFERENCES "reading_list" ("list_id"),
  FOREIGN KEY ("book_id") REFERENCES "book" ("book_id")
);

CREATE TABLE "subscription" (
  "subscription_id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "user_id" UUID NOT NULL,
  "plan_type" INT NOT NULL,
  "start_date" TIMESTAMP NOT NULL,
  "end_date" TIMESTAMP NOT NULL,
  "payment_status" INT NOT NULL,
  FOREIGN KEY ("user_id") REFERENCES "user" ("user_id"),
  FOREIGN KEY ("plan_type") REFERENCES "plan_type" ("plan_type_id"),
  FOREIGN KEY ("payment_status") REFERENCES "payment_status_type" ("payment_status_type_id"),
  CONSTRAINT valid_dates CHECK ("start_date" < "end_date")
);

CREATE TABLE "notification" (
  "notification_id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "message" VARCHAR(40) NOT NULL,
  "is_read" BOOLEAN NOT NULL DEFAULT false,
  "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "user_id" UUID NOT NULL,
  "notification_type" INT NOT NULL,
  FOREIGN KEY ("user_id") REFERENCES "user" ("user_id"),
  FOREIGN KEY ("notification_type") REFERENCES "notification_type" ("notification_type_id")
);

-- Tablas de relación
CREATE TABLE "genre_book" (
  "book_id" UUID NOT NULL,
  "genre_type_id" INT NOT NULL,
  PRIMARY KEY ("book_id", "genre_type_id"),
  FOREIGN KEY ("book_id") REFERENCES "book" ("book_id"),
  FOREIGN KEY ("genre_type_id") REFERENCES "genre_type" ("genre_type_id")
);

CREATE TABLE "book_tag" (
  "book_id" UUID NOT NULL,
  "tag_id" INT NOT NULL,
  PRIMARY KEY ("book_id", "tag_id"),
  FOREIGN KEY ("book_id") REFERENCES "book" ("book_id"),
  FOREIGN KEY ("tag_id") REFERENCES "tag" ("tag_id")
);

CREATE TABLE "book_similarity" (
  "book_id_1" UUID NOT NULL,
  "book_id_2" UUID NOT NULL,
  "similarity_score" FLOAT NOT NULL CHECK ("similarity_score" BETWEEN 0 AND 1),
  PRIMARY KEY ("book_id_1", "book_id_2"),
  FOREIGN KEY ("book_id_1") REFERENCES "book" ("book_id"),
  FOREIGN KEY ("book_id_2") REFERENCES "book" ("book_id"),
  CONSTRAINT no_self_similarity CHECK ("book_id_1" != "book_id_2")
);

-- Tablas de métricas
CREATE TABLE "book_metrics" (
  "book_id" UUID PRIMARY KEY,
  "total_reads" INT NOT NULL DEFAULT 0,
  "total_listens" INT NOT NULL DEFAULT 0,
  "total_favorites" INT NOT NULL DEFAULT 0,
  "total_reviews" INT NOT NULL DEFAULT 0,
  "average_rating" FLOAT NOT NULL DEFAULT 0 CHECK ("average_rating" BETWEEN 0 AND 5),
  "last_read_at" TIMESTAMP,
  "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY ("book_id") REFERENCES "book" ("book_id")
);

CREATE TABLE "user_metrics" (
  "user_id" UUID PRIMARY KEY,
  "books_read" INT NOT NULL DEFAULT 0,
  "minutes_listened" INT NOT NULL DEFAULT 0,
  "reviews_written" INT NOT NULL DEFAULT 0,
  "favorites_count" INT NOT NULL DEFAULT 0,
  "total_pages_read" INT NOT NULL DEFAULT 0,
  "active_days" INT NOT NULL DEFAULT 0,
  "last_active_at" TIMESTAMP,
  "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY ("user_id") REFERENCES "user" ("user_id")
);

-- Tablas de marketing
CREATE TABLE "promotion" (
  "promotion_id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "book_id" UUID NOT NULL,
  "title" VARCHAR(100) NOT NULL,
  "description" TEXT,
  "start_date" TIMESTAMP NOT NULL,
  "end_date" TIMESTAMP NOT NULL,
  "discount_percent" INT CHECK ("discount_percent" BETWEEN 0 AND 100),
  "banner_image_url" VARCHAR(255),
  "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY ("book_id") REFERENCES "book" ("book_id"),
  CONSTRAINT promotion_valid_dates CHECK ("start_date" < "end_date")
);

COMMENT ON COLUMN "promotion"."discount_percent" IS '0-100';

CREATE TABLE "ad_campaign" (
  "ad_id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "title" VARCHAR(100) NOT NULL,
  "image_url" VARCHAR(255),
  "target_url" VARCHAR(255),
  "book_id" UUID,
  "created_by" UUID NOT NULL,
  "visible_to_plan" INT,
  "start_date" TIMESTAMP NOT NULL,
  "end_date" TIMESTAMP NOT NULL,
  "impressions" INT NOT NULL DEFAULT 0,
  "clicks" INT NOT NULL DEFAULT 0,
  "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY ("book_id") REFERENCES "book" ("book_id"),
  FOREIGN KEY ("created_by") REFERENCES "user" ("user_id"),
  FOREIGN KEY ("visible_to_plan") REFERENCES "plan_type" ("plan_type_id"),
  CONSTRAINT ad_valid_dates CHECK ("start_date" < "end_date")
);