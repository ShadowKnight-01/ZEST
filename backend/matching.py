from Database.db_connect import supabase

# define matching system
def find_matches(user_id):

    try:
        # get information on interest from the users
        user_res = supabase.table("users").select("interest").eq("user_id", user_id).execute()
        if not user_res.data or not user_res.data[0].get("interests"):
            return []
        
        user_interest ={
            i.strip().lower() for i in user_res.data[0]["interests"].split(",") if i.strip()
        }

        all_res = supabase.table("users").select("user_id, username, interests").ne("user_id", user_id).execute()
        if not all_res.data:
            return []

        matches = []
        for r in all_res.data:
            if not r.get("interests"):
                continue

            other_interest = {
                i.strip().lower() for i in r["interests"].split(",") if i.strip()
            }

            common = user_interest.intersection(other_interest)
            if common:
                matches.append({
                    "user_id"  : r["user_id"],
                    "username" : r["username"],
                    "score"    : len(common),
                    "common_interest" : list(common)
                })

        matches.sort(key=lambda x: x["score"], reverse=True)
        return matches

    except Exception as e:
        return f"Database Error: {e}"