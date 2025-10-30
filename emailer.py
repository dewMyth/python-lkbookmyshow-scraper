from jinja2 import Template
from db import get_emails
from logger import logger
import os
import resend


SENDPULSE_API_URL = "https://api.sendpulse.com"


def generate_html_content(movies):

    template_str = """
    {% for movie in movies %}
<tr>
  <td style="padding:15px; border-bottom:1px solid #eee;">
    <table width="100%" cellpadding="0" cellspacing="0" border="0">
      <tr>
        <td class="movie" style="vertical-align:top;">
          <img src="{{ movie.image }}" alt="{{ movie.name }}" width="140" style="width:140px; height:auto; border-radius:8px; margin-right:15px; display:inline-block; vertical-align:top;">
          <div class="details" style="display:inline-block; max-width:500px; vertical-align:top;">
            <div class="title" style="font-size:18px; font-weight:bold; margin:5px 0;">{{ movie.name }}</div>
            {% if movie.genre %}
            <div class="genre" style="font-size:14px; color:#888; margin-bottom:10px;">{{ movie.genre }}</div>
            {% endif %}
            <div class="description" style="font-size:14px; line-height:1.5; margin-bottom:10px;">{{ movie.description }}</div>
            <div class="actions">
              <a href="{{ movie.link }}" style="text-decoration:none; color:#fff; background:#e50914; padding:8px 14px; border-radius:5px; font-size:14px; margin-right:10px; display:inline-block;">View Details</a>
              <a href="{{ movie.buy_link }}" style="text-decoration:none; color:#fff; background:#b20710; padding:8px 14px; border-radius:5px; font-size:14px; display:inline-block;">Buy Tickets</a>
            </div>
          </div>
        </td>
      </tr>
    </table>
  </td>
</tr>
{% endfor %}

<tr>
  <td style="background:#fafafa; text-align:center; padding:15px; font-size:12px; color:#777;">
    © 2025 Scope Cinemas. All rights reserved.
  </td>
</tr>
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







