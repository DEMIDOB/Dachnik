import vk_api
from .models import BlogPost
from .safe import vk_auth_data

vk_session = vk_api.VkApi(vk_auth_data['login'], vk_auth_data['password'])
vk_session.auth()

def syncPosts():
    posts = vk_session.method('wall.get', {'owner_id': 518803197, "type": "text"})['items']

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

        print(post_id)
        try:
            post_attachments = post['attachments']
            post_photo_url = post_attachments[0]['photo']['sizes'][-1]['url']
            PostObject.icon = post_photo_url
        except:
            pass

        PostObject.save()

if __name__ == "__main__":
    syncPosts()