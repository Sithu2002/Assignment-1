from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from reactpy.backend.fastapi import configure
from reactpy import component, html, use_state, event
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = FastAPI()

# MongoDB connection URI
mongo_uri = "mongodb+srv://sithu:sithu123@cluster0.g1utvb8.mongodb.net/"

# Create a new client and connect to the server
client = MongoClient(mongo_uri, server_api=ServerApi("1"))
db = client["reactpy"]
collection = db["users"]

# Send a ping to confirm a successful connection
try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Function to validate email format
def is_valid_email(email):
    return email.endswith("@gmail.com")

# Component for Sign Up Page
@component
def SignUp():
    # State variables for form fields
    first_name, set_first_name = use_state("")
    last_name, set_last_name = use_state("")
    username, set_username = use_state("")
    email, set_email = use_state("")
    password, set_password = use_state("")
    gender, set_gender = use_state("")

    def handle_signup(event, request):
        if not is_valid_email(email):
            return "Invalid email format. Please use an @gmail.com email address."
        
        user_data = {
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "email": email,
            "password": password,
            "gender": gender,
        }
        # Insert user data into MongoDB
        result = collection.insert_one(user_data)
        print("result")
        # Redirect to the images page after successful registration
        return RedirectResponse("/images", status_code=303)

    return html.div(
        {"style": 
            {
                "display": "flex",
                "flexDirection": "column",
                "justify-content": "center",  # Centering horizontally
                "align-items": "center",      # Centering vertically
                "background-image": "url(https://c4.wallpaperflare.com/wallpaper/239/328/6/nature-landscape-lake-island-wallpaper-preview.jpg)",
                "background-size": "cover",
                "height": "100vh",
                "width": "100vw",
                "margin": "12px",
                "padding": "12px",
            }
        },
        html.form(
            {"on_submit": event(lambda event, request: handle_signup(event, request))},
            html.h1(
                {"style": {"font-family": "Arial", "font-size": "45px", "alignItems": "center", "flexDirection": "column", "color": "rgba(250, 250, 250, 1)"}},
                "Welcome to Sri Lanka 😎",
            ),
            html.h1("Sign Up"),
            html.input(
                {
                    "type": "text",
                    "placeholder": "First Name",
                    "on_change": lambda event: set_first_name(event["target"]["value"]),
                }
            ),
            html.br(),
            html.p(""),
            html.input(
                {
                    "type": "text",
                    "placeholder": "Last Name",
                    "on_change": lambda event: set_last_name(event["target"]["value"]),
                }
            ),
            html.br(),
            html.p(""),
            html.input(
                {
                    "type": "text",
                    "placeholder": "Username",
                    "on_change": lambda event: set_username(event["target"]["value"]),
                }
            ),
            html.br(),
            html.p(""),
            html.input(
                {
                    "type": "text",
                    "placeholder": "Email",
                    "on_change": lambda event: set_email(event["target"]["value"]),
                    "style": {
                        "border": "1px solid red" if not is_valid_email(email) else "1px solid black",
                    },
                }
            ),
            html.br(),
            html.p(""),
            html.input(
                {
                    "type": "password",
                    "placeholder": "Password",
                    "on_change": lambda event: set_password(event["target"]["value"]),
                }
            ),
            html.br(),
            html.p(""),
            html.label(
                {
                    "style": {
                        "font-family": "Arial",
                        "font-size": "20px",
                        "color": "#000000",
                    }
                },
                "Gender:",
            ),
            html.br(),
            html.p(""),
            html.input(
                {
                    "type": "radio",
                    "name": "gender",
                    "value": "Male",
                    "on_change": lambda event: set_gender(event["target"]["value"]),
                },
            ),
            "Male",
            html.input(
                {
                    "type": "radio",
                    "name": "gender",
                    "value": "Female",
                    "on_change": lambda event: set_gender(event["target"]["value"]),
                },
            ),
            "Female",
            html.input(
                {
                    "type": "radio",
                    "name": "gender",
                    "value": "Other",
                    "on_change": lambda event: set_gender(event["target"]["value"]),
                },
            ),
            "Other",
            html.br(),
            html.p(""),
            html.button(
                {
                    "type": "Create an Account",
                    "on_click": event(lambda event, request: handle_signup(event, request)),
                },
                "Create an Account",
            ),
        ),
    )

# Component for Sign In Page
@component
def SignIn():
    # State variables for form fields
    username, set_username = use_state("")
    password, set_password = use_state("")

    def handle_signin(event, request):
        # Validate user credentials (You should add proper validation and authentication logic here)
        user_data = collection.find_one({"username": username, "password": password})
        if user_data:
            # Redirect to the images page after successful login
            return RedirectResponse("/images", status_code=303)
        else:
            return "Invalid credentials. Please try again."

    return html.div(
        {"style": 
            {
                "display": "flex",
                "flexDirection": "column",
                "justify-content": "center",  # Centering horizontally
                "align-items": "center",      # Centering vertically
                "background-image": "url(https://c4.wallpaperflare.com/wallpaper/239/328/6/nature-landscape-lake-island-wallpaper-preview.jpg)",
                "background-size": "cover",
                "height": "100vh",
                "width": "100vw",
                "margin": "15px",
                "padding": "15px",
            }
        },
        html.form(
            {"on_submit": event(lambda event, request: handle_signin(event, request))},
            html.h1("Sign In"),
            html.input(
                {
                    "type": "text",
                    "placeholder": "Username",
                    "on_change": lambda event: set_username(event["target"]["value"]),
                }
            ),
            html.br(),
            html.p(""),
            html.input(
                {
                    "type": "password",
                    "placeholder": "Password",
                    "on_change": lambda event: set_password(event["target"]["value"]),
                }
            ),
            html.br(),
            html.p(""),
            html.button(
                {
                    "type": "Submit",
                    "on_click": event(lambda event, request: handle_signin(event, request)),
                },
                "Sign In",
            ),
        ),
    )

# Component for Images Page (display images after sign-in)
@component
def Images():
    return html.div(
        {"style":
            {
                "display": "flex",
                "flex-direction": "column",
                "justify-content": "center",
                "align-items": "center",
                "background-color": "#f0f0f0",
                "height": "100vh",
            }
        },
        html.h1("Welcome to the Image Gallery"),
        html.img(src="https://c4.wallpaperflare.com/wallpaper/110/856/52/landscape-fantasy-art-cherry-blossom-digital-art-wallpaper-preview.jpg", alt="A beautiful landscape"),
        html.img(src="https://c4.wallpaperflare.com/wallpaper/444/479/808/flowers-yellow-flowers-black-background-digital-art-wallpaper-preview.jpg", alt="A beautiful landscape")

    )

# Component for Home Page with Sign Up and Sign In buttons
@component
def Home():
    show_signup, set_show_signup = use_state(False)
    show_signin, set_show_signin = use_state(False)

    def show_signup_page(event):
        set_show_signup(True)
        set_show_signin(False)

    def show_signin_page(event):
        set_show_signup(False)
        set_show_signin(True)

    return html.div(
        {"style": {"font-family": "Arial", "font-size": "16px", "text-align": "center"}},
        html.h1("Welcome All"),
        html.button(
            {"on_click": event(lambda event: show_signup_page(event))},
            "Sign Up",
        ),
        html.p(),
        html.button(
            {"on_click": event(lambda event: show_signin_page(event))},
            "Sign In",
        ),
        SignUp() if show_signup else SignIn(),
    )

# Configure the FastAPI app
configure(app, Home)





