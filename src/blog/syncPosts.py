import vk_api

from datetime import datetime, timedelta, timezone

from .models import BlogPost
from .safe import vk_auth_data

vk_session = vk_api.VkApi(vk_auth_data['login'], vk_auth_data['password'])
vk_session.auth()


def _secsDifference(d1):
    return (datetime.now(timezone.utc) - d1).seconds


def syncPosts():
    allPosts = BlogPost.objects.all()
    if len(allPosts) > 0:
        exPost = allPosts[0]
        secsLeft = _secsDifference(exPost.date_time)
        print(f"{secsLeft}s. left from the previous update =>")
        if secsLeft < 3600:
            print("Using cached posts")
            return
            print("This will not be executed =) ")

    print("Updating posts in DB - more than an hour left from the previous update!")

    try:
        posts = vk_session.method('wall.get', {'owner_id': 518803197, "type": "text"})['items']
    except:
        try:
            syncPosts()
            return
        except Exception as exc:
            print("Could not sync VK posts due to:", exc)
            return

    for post in posts:
        vk_text = str(post['text'])
        post_title = vk_text.split('\n')[0]
        post_text = vk_text[vk_text.find('\n'):]
        post_id = post['id']

        try:
            PostObject = BlogPost.objects.get(id=post_id)
        except BlogPost.DoesNotExist as e:
            PostObject = BlogPost(id=post_id)

        PostObject.title = post_title
        PostObject.body = post_text

        # print(post_id)
        try:
            post_attachments = post['attachments']
            post_photo_url = post_attachments[0]['photo']['sizes'][-1]['url']
            PostObject.icon = post_photo_url
        except:
            pass

        PostObject.save()


if __name__ == "__main__":
    syncPosts()
