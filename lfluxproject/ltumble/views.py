# Create your views here.

from tumblelog.views import PostListView, PostDetailView
from models import LPost

class LPostListView(PostListView):
    def __init__(self, story, *args, **kwargs):
        self.queryset = LPost.objects.get_for_story(story)
        super(self, PostListView).__init__(*args, **kwargs)
