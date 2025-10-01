from flask import url_for
import smtplib
from email.mime.multipart import MIMEMultipart
# Email bodystem date and time manipulation
from email.mime.text import MIMEText

def send_reset_email(user):
    token = user.get_token()

# send the email

    print('Composing Email.......')

    SERVER = 'smtp.gmail.com'  # smtp server
    PORT = 587  # mail port number
    FROM = 'hellouser2914@gmail.com'  # sender Mail
    TO = user.email  # receiver mail
    PASS ='fmmifbmgqenfrjkv'  # Sender Mail Password

    msg = MIMEMultipart()
    content = f'''<div class="content-wrap" style="font-family: 'Roboto', sans-serif; box-sizing: border-box; color: #495057; font-size: 14px; vertical-align: top; margin: 0;padding: 30px; box-shadow: 0 3px 15px rgba(30,32,37,.06); ;border-radius: 7px; background-color: #fff;" valign="top">
                                                        <meta itemprop="name" content="Confirm Email" style="font-family: 'Roboto', sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                        <table width="100%" cellpadding="0" cellspacing="0" style="font-family: 'Roboto', sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                            <tbody><tr style="font-family: 'Roboto', sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                                <td class="content-block" style="font-family: 'Roboto', sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;" valign="top">
                                                                    <div style="text-align: center;">
                                                                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-lock" style="color: #0ab39c;fill: rgba(10,179,156,.16); height: 30px; width: 30px;"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                            <tr style="font-family: 'Roboto', sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                                <td class="content-block" style="font-family: 'Roboto', sans-serif; box-sizing: border-box; font-size: 24px; vertical-align: top; margin: 0; padding: 0 0 10px;  text-align: center;" valign="top">
                                                                    <h4 style="font-family: 'Roboto', sans-serif; margin-bottom: 0px;font-weight: 500; line-height: 1.5;">Change or reset your password</h4>
                                                                </td>
                                                            </tr>
                                                            <tr style="font-family: 'Roboto', sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                                <td class="content-block" style="font-family: 'Roboto', sans-serif; color: #878a99; box-sizing: border-box; font-size: 15px; vertical-align: top; margin: 0; padding: 0 0 12px; text-align: center;" valign="top">
                                                                    <p style="margin-bottom: 13px; line-height: 1.5;">Click below button to reset your Password :</p>
                                                                </td>
                                                            </tr>
                                                            <tr style="font-family: 'Roboto', sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                                <td class="content-block" itemprop="handler" itemscope="" itemtype="http://schema.org/HttpActionHandler" style="font-family: 'Roboto', sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 22px; text-align: center;" valign="top">
                                                                    <a href="{url_for('user_auth.user_reset_token', token=token, _external=True)}" itemprop="url" style="font-family: 'Roboto', sans-serif; box-sizing: border-box; font-size: .8125rem; color: #FFF; text-decoration: none; font-weight: 400; text-align: center; cursor: pointer; display: inline-block; border-radius: .25rem; text-transform: capitalize; background-color: #405189; margin: 0; border-color: #405189; border-style: solid; border-width: 1px; padding: .5rem .9rem;">Reset Password</a>
                                                                </td>
                                                            </tr>
                                                        </tbody></table>
                                                    </div> '''

    msg['Subject'] = 'Reset Password - MUTE'
    msg['From'] = FROM
    msg['To'] = TO

    msg.attach(MIMEText(content, 'html'))

    print('Initiating server ...')

    server = smtplib.SMTP(SERVER, PORT)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.login(FROM, PASS)
    server.sendmail(FROM, TO, msg.as_string())
    print('Email Sent...')
    server.quit()

# def welcome_mail(user,code):
#     # send the email

#     print('Composing Email.......')

#     SERVER = 'smtp.gmail.com'  # smtp server
#     PORT = 587  # mail port number
#     FROM = 'hellouser2914@gmail.com'  # sender Mail
#     TO = user.email  # receiver mail
#     PASS = 'fmmifbmgqenfrjkv'  # Sender Mail Password

#     msg = MIMEMultipart()

#     content = '''
#     <!DOCTYPE html>
# <html>

# <head>
#     <title></title>
#     <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
#     <meta name="viewport" content="width=device-width, initial-scale=1">
#     <meta http-equiv="X-UA-Compatible" content="IE=edge" />
#     <style type="text/css">
#         @media screen { 
#             @font-face {
#                 font-family: 'Lato';
#                 font-style: normal;
#                 font-weight: 400;
#                 src: local('Lato Regular'), local('Lato-Regular'), url(https://fonts.gstatic.com/s/lato/v11/qIIYRU-oROkIk8vfvxw6QvesZW2xOQ-xsNqO47m55DA.woff) format('woff');
#             }

#             @font-face {
#                 font-family: 'Lato';
#                 font-style: normal;
#                 font-weight: 700;
#                 src: local('Lato Bold'), local('Lato-Bold'), url(https://fonts.gstatic.com/s/lato/v11/qdgUG4U09HnJwhYI-uK18wLUuEpTyoUstqEm5AMlJo4.woff) format('woff');
#             }

#             @font-face {
#                 font-family: 'Lato';
#                 font-style: italic;
#                 font-weight: 400;
#                 src: local('Lato Italic'), local('Lato-Italic'), url(https://fonts.gstatic.com/s/lato/v11/RYyZNoeFgb0l7W3Vu1aSWOvvDin1pK8aKteLpeZ5c0A.woff) format('woff');
#             }

#             @font-face {
#                 font-family: 'Lato';
#                 font-style: italic;
#                 font-weight: 700;
#                 src: local('Lato Bold Italic'), local('Lato-BoldItalic'), url(https://fonts.gstatic.com/s/lato/v11/HkF_qI1x_noxlxhrhMQYELO3LdcAZYWl9Si6vvxL-qU.woff) format('woff');
#             }
#         }

#         / CLIENT-SPECIFIC STYLES /
#         body,
#         table,
#         td,
#         a {
#             -webkit-text-size-adjust: 100%;
#             -ms-text-size-adjust: 100%;
#         }

#         table,
#         td {
#             mso-table-lspace: 0pt;
#             mso-table-rspace: 0pt;
#         }

#         img {
#             -ms-interpolation-mode: bicubic;
#         }

#         / RESET STYLES /
#         img {
#             border: 0;
#             height: auto;
#             line-height: 100%;
#             outline: none;
#             text-decoration: none;
#         }

#         table {
#             border-collapse: collapse !important;
#         }

#         body {
#             height: 100% !important;
#             margin: 0 !important;
#             padding: 0 !important;
#             width: 100% !important;
#         }
#         a[x-apple-data-detectors] {
#             color: inherit !important;
#             text-decoration: none !important;
#             font-size: inherit !important;
#             font-family: inherit !important;
#             font-weight: inherit !important;
#             line-height: inherit !important;
#         }
#         @media screen and (max-width:600px) {
#             h1 {
#                 font-size: 32px !important;
#                 line-height: 32px !important;
#             }
#         }

#         / ANDROID CENTER FIX /
#         div[style*="margin: 16px 0;"] {
#             margin: 0 !important;
#         }
#     </style>
# </head>

# <body style="background-color: #f4f4f4; margin: 0 !important; padding: 0 !important;">
#     <!-- HIDDEN PREHEADER TEXT -->
#     <div style="display: none; font-size: 1px; color: #fefefe; line-height: 1px; font-family: 'Lato', Helvetica, Arial, sans-serif; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden;"> We're thrilled to have you here! Get ready to dive into your new account.
#     </div>
#     <table border="0" cellpadding="0" cellspacing="0" width="100%">
#         <!-- LOGO -->
#         <tr>
#             <td bgcolor="#40c1ac" align="center">
#                 <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">
#                     <tr>
#                         <td align="center" valign="top" style="padding: 40px 10px 40px 10px;"> </td>
#                     </tr>
#                 </table>
#             </td>
#         </tr>
#         <tr>
#             <td bgcolor="#40c1ac" align="center" style="padding: 0px 10px 0px 10px;">
#                 <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">
#                     <tr>
#                         <td bgcolor="#ffffff" align="center" valign="top" style="padding: 40px 20px 20px 20px; border-radius: 4px 4px 0px 0px; color: #111111; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 48px; font-weight: 400; letter-spacing: 4px; line-height: 48px;">
#                             <h1 style="font-size: 48px; font-weight: 400; margin: 2;">Welcome!</h1> <img src="https://admin.simple-practice.co/simplepractice/base/static/assets/images/logo1.png" width="125" height="120" style="display: block; border: 0px;" />
#                         </td>
#                     </tr>
#                 </table>
#             </td>
#         </tr>
#         <tr>
#             <td bgcolor="#f4f4f4" align="center" style="padding: 0px 10px 0px 10px;">
#                 <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">
#                     <tr>
#                         <td bgcolor="#ffffff" align="left" style="padding: 20px 30px 40px 30px; color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;">
#                             <p style="margin: 0;">We're excited to have you get started. First</p>
#                             <p style="margin: 0;">here is your verification code </p>
#                             <h5>'''+code+'''</h5>
#                         </td>
#                     </tr>
                   
#                     <tr>
#                         <td bgcolor="#ffffff" align="left" style="padding: 0px 30px 20px 30px; color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;">
#                             <p  style="margin: 0;">If you have any questions, just reply to this email&mdash;we're always happy to help out.</p>
#                         </td>
#                     </tr>
#                     <tr>
#                         <td bgcolor="#ffffff" align="left" style="padding: 0px 30px 40px 30px; border-radius: 0px 0px 4px 4px; color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;">
#                             <p style="margin: 0;">Cheers,<br>Simple Practice Team</p>
#                         </td>
#                     </tr>
#                 </table>
#             </td>
#         </tr>
#         <tr>
#             <td bgcolor="#f4f4f4" align="center" style="padding: 30px 10px 0px 10px;">
#                 <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">
#                     <tr>
#                         <td bgcolor="#0086bf" align="center" style="padding: 30px 30px 30px 30px; border-radius: 4px 4px 4px 4px; color: #ffff; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;">
#                             <h2 style="font-size: 20px; font-weight: 400; color: #ffff; margin: 0;">Need more help?</h2>
#                             <p style="margin: 0;"><a href="#" target="_blank" style="color: #fff;">We&rsquo;re here to help you out</a></p>
#                         </td>
#                     </tr>
#                 </table>
#             </td>
#         </tr>
#         <tr>
#             <td bgcolor="#f4f4f4" align="center" style="padding: 0px 10px 0px 10px;">
#             </td>
#         </tr>
#     </table>
# </body>
# </html>
#     '''
#     msg['Subject'] = 'Mute - Email verification'
#     msg['From'] = FROM
#     msg['To'] = TO

#     msg.attach(MIMEText(content, 'html'))

#     print('Initiating server ...')

#     server = smtplib.SMTP(SERVER, PORT)
#     server.set_debuglevel(1)
#     server.ehlo()
#     server.starttls()
#     server.login(FROM, PASS)
#     server.sendmail(FROM, TO, msg.as_string())
#     print('Email Sent...')
#     server.quit()

