from jinja2 import Template
from db import get_emails
from logger import logger
import os
import resend


SENDPULSE_API_URL = "https://api.sendpulse.com"


def generate_html_content(movies):

    template_str = """
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <title>🎬 Now Showing at Scope Cinemas</title>
      <style>
        body {
          font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
          background-color: #f5f5f5;
          margin: 0;
          padding: 20px;
          color: #333;
        }
        .container {
          max-width: 700px;
          margin: auto;
          background: #ffffff;
          border-radius: 10px;
          box-shadow: 0 4px 10px rgba(0,0,0,0.1);
          overflow: hidden;
        }
        .header {
          background: linear-gradient(135deg, #e50914, #b20710);
          color: white;
          padding: 20px;
          text-align: center;
        }
        .movie {
          display: flex;
          flex-direction: row;
          border-bottom: 1px solid #eee;
          padding: 15px;
        }
        .movie:last-child {
          border-bottom: none;
        }
        .movie img {
          width: 140px;
          height: 200px;
          object-fit: cover;
          border-radius: 8px;
          margin-right: 15px;
        }
        .details {
          flex: 1;
        }
        .title {
          font-size: 18px;
          font-weight: bold;
          margin: 5px 0;
        }
        .genre {
          font-size: 14px;
          color: #888;
          margin-bottom: 10px;
        }
        .description {
          font-size: 14px;
          line-height: 1.5;
          margin-bottom: 10px;
        }
        .actions a {
          text-decoration: none;
          color: white;
          background: #e50914;
          padding: 8px 14px;
          border-radius: 5px;
          font-size: 14px;
          margin-right: 10px;
        }
        .footer {
          background: #fafafa;
          text-align: center;
          padding: 15px;
          font-size: 12px;
          color: #777;
        }
        @media (max-width: 600px) {
          .movie {
            flex-direction: column;
            align-items: center;
          }
          .movie img {
            width: 100%;
            height: auto;
            margin-bottom: 10px;
          }
        }
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <h1>🍿 Now Showing at Scope Cinemas</h1>
          <p>Grab your popcorn and enjoy the latest hits!</p>
        </div>

        {% for movie in movies %}
        <div class="movie">
          <img src="{{ movie.image }}" alt="{{ movie.name }}">
          <div class="details">
            <div class="title">{{ movie.name }}</div>
            {% if movie.genre %}
            <div class="genre">{{ movie.genre }}</div>
            {% endif %}
            <div class="description">{{ movie.description }}</div>
            <div class="actions">
              <a href="{{ movie.link }}">View Details</a>
              <a href="{{ movie.buy_link }}">Buy Tickets</a>
            </div>
          </div>
        </div>
        {% endfor %}
      </div>
    </body>
    </html>
    """

    # Render template
    template = Template(template_str)
    html_content = template.render(movies=movies)

    # You can now attach `html_content` to your email as HTML.
    return html_content

def get_recipients():
    emails_list = get_emails()
    emails_list_str = [email_user["email"] for email_user in emails_list]
    return emails_list_str


def send_email(movies):
    resend.api_key = os.getenv("RESEND_API_KEY")

    recipients = get_recipients()

    try:
        r = resend.Emails.send({
            "from": "New Movie Notifer <onboarding@resend.dev>",
            "to": recipients,
            "subject": "Now Showing at Scope Cinemas",
            "html": generate_html_content(movies),
        })
        logger.info(f"Email sent to {recipients}")
    except Exception as e:
        logger.error(f"Error sending email: {e}")







