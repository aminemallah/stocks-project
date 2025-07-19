import requests
import json
import time

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config import cookies_headers

def get_followers(user_id, headers, max_usernames=100):
    # Initialize variables
    usernames = []
    cursor = None
    base_url = 'https://x.com/i/api/graphql/k8IHkYttROUDoDNevQ7Ehw/Followers'
    
    while len(usernames) < max_usernames:
        # Prepare parameters
        variables = {
            "userId": user_id,
            "count": 20,
            "includePromotedContent": False,
            "withSuperFollowsUserFields": True,
			"withDownvotePerspective": False,
			"withReactionsMetadata": False,
			"withReactionsPerspective": False,
			"withSuperFollowsTweetFields": True
        }
        features = {
            "rweb_video_screen_enabled": False,
            "payments_enabled": False,
            "profile_label_improvements_pcf_label_in_post_enabled": True,
            "rweb_tipjar_consumption_enabled": True,
            "verified_phone_label_enabled": False,
            "creator_subscriptions_tweet_preview_api_enabled": True,
            "responsive_web_graphql_timeline_navigation_enabled": True,
            "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
            "premium_content_api_read_enabled": False,
            "communities_web_enable_tweet_community_results_fetch": True,
            "c9s_tweet_anatomy_moderator_badge_enabled": True,
            "responsive_web_grok_analyze_button_fetch_trends_enabled": False,
            "responsive_web_grok_analyze_post_followups_enabled": True,
            "responsive_web_jetfuel_frame": True,
            "responsive_web_grok_share_attachment_enabled": True,
            "articles_preview_enabled": True,
            "responsive_web_edit_tweet_api_enabled": True,
            "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
            "view_counts_everywhere_api_enabled": True,
            "longform_notetweets_consumption_enabled": True,
            "responsive_web_twitter_article_tweet_consumption_enabled": True,
            "tweet_awards_web_tipping_enabled": False,
            "responsive_web_grok_show_grok_translated_post": False,
            "responsive_web_grok_analysis_button_from_backend": True,
            "creator_subscriptions_quote_tweet_preview_enabled": False,
            "freedom_of_speech_not_reach_fetch_enabled": True,
            "standardized_nudges_misinfo": True,
            "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
            "longform_notetweets_rich_text_read_enabled": True,
            "longform_notetweets_inline_media_enabled": True,
            "responsive_web_grok_image_annotation_enabled": True,
            "responsive_web_grok_community_note_auto_translation_is_enabled": False,
            "responsive_web_enhance_cards_enabled": False
		}
        if cursor:
            print(f"CURSSOOOOOOORRR : {cursor}")
            variables["cursor"] = cursor
            
        params = {
            'variables': json.dumps(variables),
            'features': json.dumps(features)
        }

        try:
            # Make API request
            response = requests.get(base_url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()

            import sys
            import os
            sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
            sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
            from common import common_utils
            common_utils.save_json_file_to_disk("test.json", data)

            # Extract followers from response
            try:
                instructions = data['data']['user']['result']['timeline']['timeline']['instructions']
                for instruction in instructions:
                    if instruction['type'] == 'TimelineAddEntries':
                        for entry in instruction['entries']:
                            if entry['content']['entryType'] == 'TimelineTimelineItem':
                                username = entry['content']['itemContent']['user_results']['result']['core']['screen_name']
                                name = entry['content']['itemContent']['user_results']['result']['core']['name']
                                usernames.append(username)
                                print(f"Username {len(usernames)}: {username}")
                                # Break if we reached max_usernames
                                if len(usernames) >= max_usernames:
                                    return usernames

                            # Get next cursor
                            if entry['content']['entryType'] == 'TimelineTimelineCursor' and entry['content']['cursorType'] == 'Bottom':
                                cursor = entry['content']["value"]
                                print(cursor)
            
            except (KeyError, TypeError) as e:
                print(f"Error parsing response: {e}")
                break

            # If no more cursor, break the loop
            if not cursor:
                break

            # Rate limiting: sleep to avoid hitting API limits
            time.sleep(300)

        except requests.RequestException as e:
            print(f"Request failed: {e}")
            break

    return usernames

# Example usage
if __name__ == "__main__":
    cookies = cookies_headers.API_COOKIES
    headers = cookies_headers.API_HEADERS

    user_id = "1468103131737247748"  # Amit
    followers = get_followers(user_id, headers)
    print(f"\nTotal followers retrieved: {len(followers)}")