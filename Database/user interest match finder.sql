-- =====================================================================
-- 1. FUNCTION TO STORE USER INTERESTS
-- =====================================================================
-- This function takes a user's ID and a new string of interests,
-- updates their row, and returns a success text message.
CREATE OR REPLACE FUNCTION public.store_user_interests(
    p_user_id VARCHAR(20), 
    p_interests_string TEXT
)
RETURNS TEXT 
LANGUAGE plpgsql AS $$
BEGIN
    -- Check if the user exists first
    IF NOT EXISTS (SELECT 1 FROM public.users WHERE user_id = p_user_id) THEN
        RETURN 'Error: User not found.';
    END IF;

    -- Update the interests column
    UPDATE public.users
    SET interests = p_interests_string
    WHERE user_id = p_user_id;

    RETURN 'Success: Interests updated.';
END;
$$;


-- =====================================================================
-- 2. FUNCTION TO RETRIEVE USER INTERESTS
-- =====================================================================
-- This function reads the interests string for a user and returns it.
CREATE OR REPLACE FUNCTION public.retrieve_user_interests(p_user_id VARCHAR(20))
RETURNS TEXT 
LANGUAGE plpgsql AS $$
DECLARE
    v_interests TEXT;
BEGIN
    SELECT interests INTO v_interests 
    FROM public.users 
    WHERE user_id = p_user_id;

    -- Handle case where user doesn't exist
    IF NOT FOUND THEN
        RETURN 'Error: User not found.';
    END IF;

    -- Handle case where interests column is completely empty (NULL)
    IF v_interests IS NULL THEN
        RETURN '';
    END IF;

    RETURN v_interests;
END;
$$;