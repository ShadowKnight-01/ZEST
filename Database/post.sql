-- =====================================================================
-- 1. CREATE POST (Insert a new post into the feed)
-- =====================================================================
CREATE OR REPLACE FUNCTION public.create_post(
    p_user_id VARCHAR(20),
    p_content TEXT,
    p_image VARCHAR(255) DEFAULT NULL    
)
RETURNS TEXT
LANGUAGE plpgsql AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM public.users WHERE user_id = p_user_id) THEN
        RETURN 'Error: User profile not found.';
    END IF;

    INSERT INTO public.posts (user_id, content, image)
    VALUES (p_user_id, p_content, p_image);

    RETURN 'Success: Post created successfully.';
END;
$$;


-- =====================================================================
-- 2. READ POSTS (Retrieve all posts sequentially for the social feed)
-- =====================================================================
CREATE OR REPLACE FUNCTION public.get_social_feed()
RETURNS TABLE(
    post_id INT,
    user_id VARCHAR(20),
    author_name VARCHAR(100),
    author_username VARCHAR(50),
    profile_pic VARCHAR(255),
    content TEXT,
    image VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT p.post_id, p.user_id, u.full_name, u.username, u.profile_pic, p.content, p.image, p.created_at
    FROM public.posts p
    JOIN public.users u ON p.user_id = u.user_id
    ORDER BY p.created_at DESC; 
END;
$$;


-- =====================================================================
-- 3. UPDATE POST (Modify existing post content)
-- =====================================================================
CREATE OR REPLACE FUNCTION public.update_post(
    p_post_id INT,
    p_user_id VARCHAR(20),               
    p_new_content TEXT,
    p_new_image VARCHAR(255) DEFAULT NULL
)
RETURNS TEXT
LANGUAGE plpgsql AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM public.posts WHERE post_id = p_post_id AND user_id = p_user_id) THEN
        RETURN 'Error: Unauthorized action or post does not exist.';
    END IF;

    UPDATE public.posts
    SET content = p_new_content,
        image = p_new_image
    WHERE post_id = p_post_id;

    RETURN 'Success: Post updated successfully.';
END;
$$;


-- =====================================================================
-- 4. DELETE POST (Remove a specific post from existence)
-- =====================================================================
CREATE OR REPLACE FUNCTION public.delete_post(
    p_post_id INT,
    p_user_id VARCHAR(20)                 
)
RETURNS TEXT
LANGUAGE plpgsql AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM public.posts WHERE post_id = p_post_id AND user_id = p_user_id) THEN
        RETURN 'Error: Unauthorized action or post does not exist.';
    END IF;

    DELETE FROM public.posts WHERE post_id = p_post_id;

    RETURN 'Success: Post deleted successfully.';
END;
$$;