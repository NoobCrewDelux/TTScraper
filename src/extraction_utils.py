def extract_valuable_info(entry, tag):
    author = entry.get("author", {})
    stats = entry.get("stats", {})
    music = entry.get("music", {})
    hashtags = [
        hashtag.get("hashtagName")
        for hashtag in entry.get("textExtra", [])
        if hashtag.get("type") == 1
    ]

    return {
        # Video info
        "tag": tag,
        "video_id": entry.get("id"),
        "created_at": entry.get("createTime"), # UNIX timestamp
        "description": entry.get("desc"),
        "hashtags": hashtags,

        # Author info
        "author_id": author.get("id"), # Unique Author ID
        "author_secuid": author.get("secUid"), # Constant Account ID
        "author_unique": author.get("uniqueId"), # Public Username
        "author_name": author.get("nickname"), # Display Name
        "author_verified": author.get("verified"), 
        "author_bio": author.get("signature"), 
        "author_followers": author.get("followerCount"),
        "author_following": author.get("followingCount"),
        "author_likes": author.get("heartCount"),
        "author_video_count": author.get("videoCount"),

        # Engagement info
        "video_plays": stats.get("playCount"),
        "video_likes": stats.get("diggCount"),
        "video_comments": stats.get("commentCount"),
        "video_shares": stats.get("shareCount"),
        "video_favorites": stats.get("collectCount"),

        # Music info
        "music_id": music.get("id"),
        "music_title": music.get("title"),
        "music_author": music.get("authorName"),

        # Features
        "duet_enabled": entry.get("duetEnabled"),
        "stitch_enabled": entry.get("stitchEnabled"),
    }