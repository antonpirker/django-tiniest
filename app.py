import sys

from django.conf import settings
from django.urls import path
from django.http import HttpResponse, HttpResponseRedirect
from django.core.asgi import get_asgi_application
from django.core.wsgi import get_wsgi_application
from django.template import RequestContext, Template
from django import forms


### SETTINGS

settings.configure(
    DEBUG=True,
    # TODO: set your allowed hosts accordingly. See https://docs.djangoproject.com/en/5.0/ref/settings/#allowed-hosts
    # ALLOWED_HOSTS=[],
    ROOT_URLCONF=__name__,
    SECRET_KEY="this.is.insecure.please.change!",  # SECURITY WARNING: keep the secret key used in production secret!
    MIDDLEWARE_CLASSES=(
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ),
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
        }
    ],
)


### FORMS

class NewsletterForm(forms.Form):
    email = forms.EmailField(
        required=True,
        label=False,
        widget=forms.EmailInput(attrs={"placeholder": "Email"}),
    )


### VIEWS 

def home(request):
    if request.method == "POST":
        form = NewsletterForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]

            # TODO: store your new signup somewhere
            print(f"New signup: {email}")

            return HttpResponseRedirect("/success/")

    else:
        form = NewsletterForm()

        context = RequestContext(
            request, 
            {
                "content": "Sign up to the newsletter", 
                "form": form, 
            },
        )

    return HttpResponse(MAIN_HTML.render(context))


def success(request):
    context = RequestContext(
        request, 
        {
            "content": "Thanks for signing up to the newsletter!",
        },
    )
    return HttpResponse(MAIN_HTML.render(context))


### URLS

urlpatterns = [
    path("", home),
    path("success/", success),
]


### APPLICATION

application = get_wsgi_application()

### NOTE: If you want to run your application with ASGI then change this to
### application = get_asgi_application()


### TEMPLATES

MAIN_HTML = Template("""
<html>
<head>
    <title>MyProject</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        *{
            color: #525252;
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        html,body{
            display: grid;
            height: 100%;
            width: 100%;
            place-items: center;
        }
        .content{
            max-width: 900px;
            text-align: center;
            padding: 0 50px;
        }
    </style>
</head>
<body>
    <div class="content">
        <h1>django-tinier</h1>
        <h3>The install worked successfully! Congratulations!</h3>
        <br/><br/>
                     
        <h3>Here a demo form:</h3> 
        <br/><br/>
                     
        {{ content }}
                    
        {% if form %}
            <form action="." method="post">
                {% csrf_token %}
                {{ form.non_field_errors }}
                {{ form.email.errors }}
                {{ form.email }}
                <button type="submit">Sign Me Up</button>
            </form>
        {% endif %}                     
    </div>
</body>
</html>
""")


if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
