from Database.connection import connection 

# define matching system
def find_matches(user_id):

    conn = connection()
    cursor = conn.cursor()

    try:
        # get information on interest from the user
        cursor.execute("SELECT interests FROM user WHERE user_id = %s", (user_id,)) # so the interest and the location can be get from the user
        result = cursor.fetchone()

        if not result or not result[0]: 
            return []   # because the matches is in tuple so when return even if it empty must be tuple then stop the function
        
        user_interest = {   # make the interest to set
            i.strip().lower()      # remove space make all small letter
            for i in result[0].split(",")  # split by comma 
        }

        cursor.execute("SELECT user_id, username, interests FROM user WHERE user_id != %s", (user_id,))   # find all other people other then ourself
        results = cursor.fetchall()

        matches = []

        for r in results:
            if not r[2]:  # if the other people was found but not with interest it will skip them
                continue

            other_interest = {  # make other people interest seperet
                i.strip().lower()
                for i in r[2].split(",")
            }

            common = user_interest.intersection(other_interest)    # common is like checking if me and other got any common interest that intersect ourself

            if common:
                matches.append({
                    "user_id"  : r[0],  # first one 
                    "username" : r[1],  # second one
                    "score"    : len(common),   # score like how many interest got intersect
                    "common_interest" : list(common)  # list of the interest []
                })

        matches.sort(  # rearrange them according higher score or the more interest got intersect
            key = lambda x: x["score"],  # lambda is like get score and put it on 
            reverse = True   # highest goest first like deseding normally accending
        )

    except Exception as e:
        return f"Database Error: {e}"
        
    finally:
        cursor.close()
        conn.close()

    return matches