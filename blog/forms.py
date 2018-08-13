from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        min_length=4,
        error_messages={
            "required": "用户名不能为空",
            "min_length": "用户名不能少于4位"
        },
        widget=forms.widgets.TextInput(
            attrs={"class": "form-control"}
        )
    )
    password = forms.CharField(
        label="密码",
        min_length=6,
        error_messages={
            "required": "密码不能为空",
            "min_length": "密码不能少于6位"
        },
        widget=forms.widgets.PasswordInput(
            attrs={"class": "form-control"}
        )
    )

