-- Create the service databases if they do not already exist
DO
$$
BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_database WHERE datname = current_setting('CHATBOT_DB', true)
    ) THEN
        EXECUTE 'CREATE DATABASE ' || quote_ident(current_setting('CHATBOT_DB', true)) || ' OWNER ' || quote_ident(current_user);
    END IF;

    IF NOT EXISTS (
        SELECT FROM pg_database WHERE datname = current_setting('USER_DB', true)
    ) THEN
        EXECUTE 'CREATE DATABASE ' || quote_ident(current_setting('USER_DB', true)) || ' OWNER ' || quote_ident(current_user);
    END IF;

    IF NOT EXISTS (
        SELECT FROM pg_database WHERE datname = current_setting('N8N_DB', true)
    ) THEN
        EXECUTE 'CREATE DATABASE ' || quote_ident(current_setting('N8N_DB', true)) || ' OWNER ' || quote_ident(current_user);
    END IF;
END;
$$;

\connect :"CHATBOT_DB"
CREATE EXTENSION IF NOT EXISTS vector;

\connect :"USER_DB"
CREATE EXTENSION IF NOT EXISTS vector;

\connect :"N8N_DB"
CREATE EXTENSION IF NOT EXISTS vector;
