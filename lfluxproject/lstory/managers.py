from django.db import models

class StoryManager(models.Manager):
    def for_user(self, user):
        return self.get_query_set().filter(authors=user)
