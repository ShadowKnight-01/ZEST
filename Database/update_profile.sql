BEGIN
    -- Validation Check: Ensure the new username isn't already taken by another user
    IF p_username IS NOT NULL AND EXISTS (
        SELECT 1 FROM "user" WHERE username = p_username AND id != p_user_id
    ) THEN
        RETURN 'Error: Username is already taken.';
    END IF;
 -- Update User Profile Data
    -- COALESCE(input, existing) ensures that if a parameter is passed as NULL,
    -- the column retains its current value instead of overwriting it with blank data.
    UPDATE "user"
    SET 
        full_name = COALESCE(p_full_name, full_name),
        username = COALESCE(p_username, username),
        gender = COALESCE(p_gender, gender),
        age = COALESCE(p_age, age),
        course = COALESCE(p_course, course),
        education = COALESCE(p_education, education),
        profile_pic = COALESCE(p_profile_pic, profile_pic)
    WHERE id = p_user_id;
-- Error Handling: If the WHERE clause didn't match any rows, the user ID doesn't exist
    IF NOT FOUND THEN
        RETURN 'Error: User not found.';
    END IF;

    RETURN 'Profile updated successfully';
END;