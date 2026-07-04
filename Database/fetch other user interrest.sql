-- =====================================================================
-- Function: fetch_all_other_users
-- Purpose: Retrieves a list of all users in the system, excluding the 
--          currently logged-in user, who have valid interests listed.
-- Parameters:
--   - p_current_user_id: The ID of the user requesting the data (to be excluded)
-- Returns: A table containing user_id, username, and interests.
-- =====================================================================
CREATE OR REPLACE FUNCTION public.fetch_all_other_users(p_current_user_id VARCHAR(20))
RETURNS TABLE(
    user_id VARCHAR(20), 
    username VARCHAR(50), 
    interests TEXT
) 
LANGUAGE plpgsql AS $$
BEGIN
-- Execute and return the result of the query
    RETURN QUERY
    SELECT u.user_id, u.username, u.interests
    FROM public.users u
    WHERE u.user_id != p_current_user_id         -- Exclude the current user from the results
    AND u.interests IS NOT NULL                  -- Ensure the interests field is not null          
    AND u.interests != ''; -- Only return users who actually have interests listed
END;
$$;