# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.utils import timezone
from django.test import TestCase

from .models import Question, Choice


class QuestionModelTests(TestCase):

	fixtures = ['polls_testdata.json']

	def test_fixture(self):
		self.assertEqual(Question.objects.all().count(), 1)
		self.assertEqual(Choice.objects.all().count(), 6)

	def test_was_published_recently_with_future_question(self):
		"""
		returns False for questions whose pub_date is in the future
		"""
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date=time)

		self.assertIs(future_question.was_published_recently(), False)

	def test_was_published_recently_with_old_question(self):
		"""
		was_published_recently() returns False for questions whose pub_date is older than 1 day
		"""
		time = timezone.now() - datetime.timedelta(days=1,seconds=1)
		old_question = Question(pub_date=time)
		self.assertIs(old_question.was_published_recently(), False)

	def test_was_published_recently_with_recent_question(self):
		"""
		was_published_recently() returns True for questions whose pub_date is within the last day
		"""
		time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
		recent_question = Question(pub_date=time)
		self.assertEqual(recent_question.was_published_recently(), True)


	def test_get_choices(self):
		"""
		returns True if number of choices is six
		"""
		question_object = Question.objects.get(pk=2)
		choices = question_object.get_choices()
		self.assertEqual(len(choices), 6)
		self.assertEqual


	def test_leading_choice(self):
		"""
		returns True if the leading choice is Mickey Mouse
		"""
		question_object = Question.objects.get(pk=2)
		leader = question_object.get_leading_choice()
		self.assertEqual(leader.choice_text, 'Mickey Mouse')


	def test_leading_choice_pct(self):
		"""
		returns True if the percentage of leading votes is .3125
		"""
		question_object = Question.objects.get(pk=2)
		percent = question_object.get_leading_choice_pct()
		self.assertEqual(percent, 0.3125)