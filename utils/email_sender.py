import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import requests
import markdown

class EmailSender:
    def __init__(self, smtp_config):
        self.smtp_server = smtp_config['server']
        self.smtp_port = smtp_config['port']
        self.from_email = smtp_config['from_email']
        self.password = smtp_config['password']

    def send_report(self, server_name, to_email, subject, body, image_url, report):
        msg = MIMEMultipart()
        msg["From"] = self.from_email
        msg["To"] = to_email
        msg["Subject"] = server_name + ' ' + subject

        # Markdown本文をHTMLに変換
        body_html = markdown.markdown(body)

        # HTMLパートの作成
        html = f"""
        <html>
        <body>
            <img src="cid:image1">
            <br>
            {body_html}
            <br>
            <pre><code>
            {report}
            </pre></code>
        </body>
        </html>
        """
        msg.attach(MIMEText(html, 'html'))

        # 画像を読み込み、添付する
        image_response = requests.get(image_url)
        img_data = image_response.content
        image = MIMEImage(img_data)
        image.add_header('Content-ID', '<image1>')
        msg.attach(image)

        # Send email
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.from_email, self.password)
            server.sendmail(self.from_email, to_email, msg.as_string())
