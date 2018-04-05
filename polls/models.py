# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils import timezone
from operator import attrgetter


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def get_choices(self):
        """Returns a list of choice objects associated with this question."""
        return list(self.choice_set.all())

    def get_leading_choice(self):
        """Returns the choice object with the most votes."""
        choice_list = list(self.choice_set.all())

        max_choice = max(choice_list,key=attrgetter('votes'))

        return max_choice

    def get_leading_choice_pct(self):
        """Returns the percentage of votes for the leading choice."""
        total_votes = 0.0

        for choice in self.get_choices():
            total_votes += choice.votes
        
        leader = self.get_leading_choice()
        return leader.votes / total_votes

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
