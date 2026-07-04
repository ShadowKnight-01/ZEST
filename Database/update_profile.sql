BEGIN
    
    IF p_username IS NOT NULL AND EXISTS (
        SELECT 1 FROM "user" WHERE username = p_username AND id != p_user_id
    ) THEN
        RETURN 'Error: Username is already taken.';
    END IF;
 
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

    IF NOT FOUND THEN
        RETURN 'Error: User not found.';
    END IF;

    RETURN 'Profile updated successfully';
END;