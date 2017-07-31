from django import forms
from models import UserModel,Post_Model,Like_Model,Comment_Model

class SignUpForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ["email","username","name","password"]


class Log_in_Form(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ["username","password"]


class Postform(forms.ModelForm):
    class Meta:
        model = Post_Model
        fields = ['image','caption']

class Like_Unlike(forms.ModelForm):
    class Meta:
        model= Like_Model
        fields=["post"]

class Commentform(forms.ModelForm):
    class Meta:
        model = Comment_Model
        fields = ["post","comment_text"]