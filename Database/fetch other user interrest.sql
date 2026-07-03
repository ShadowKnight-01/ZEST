
CREATE OR REPLACE FUNCTION public.fetch_all_other_users(p_current_user_id VARCHAR(20))
RETURNS TABLE(
    user_id VARCHAR(20), 
    username VARCHAR(50), 
    interests TEXT
) 
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT u.user_id, u.username, u.interests
    FROM public.users u
    WHERE u.user_id != p_current_user_id 
    AND u.interests IS NOT NULL 
    AND u.interests IS NOT NULL 
    AND u.interests != ''; -- Only return users who actually have interests listed
END;
$$;