#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename:XX.py

from django import forms
from .models import Comment


# 由于表单对应了comment实体模型 故选择继承ModelForm
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'url', 'text']
