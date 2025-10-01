from flask import url_for
from werkzeug.utils import secure_filename
import smtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText #Email body
import datetime #System date and time manipulation

def send_reset_email(user):
    token = user.get_token()

# send the email

    print('Composing Email.......')

    SERVER = 'smtp.gmail.com' #smtp server
    PORT=587 #mail port number
    FROM ='hellouser2914@gmail.com' # sender Mail
    TO=user.email #receiver mail
    PASS = 'fmmifbmgqenfrjkv'   #Sender Mail Password#

    msg=MIMEMultipart()

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
                                                                    <a href="{url_for('admin_auth.reset_token', token=token, _external=True)}" itemprop="url" style="font-family: 'Roboto', sans-serif; box-sizing: border-box; font-size: .8125rem; color: #FFF; text-decoration: none; font-weight: 400; text-align: center; cursor: pointer; display: inline-block; border-radius: .25rem; text-transform: capitalize; background-color: #405189; margin: 0; border-color: #405189; border-style: solid; border-width: 1px; padding: .5rem .9rem;">Reset Password</a>
                                                                </td>
                                                            </tr>
                                                        </tbody></table>
                                                    </div> '''

#    content=f'''<B>To reset your password, visit the following link:</B></br>
#                 <a href="{url_for('user_auth.user_reset_token', token=token, _external=True)}"> Click me  </a> ''' 
    msg['Subject']='Reset Password'
    msg['From'] = FROM
    msg['To'] = TO

    msg.attach(MIMEText(content,'html'))

    print('Initiating server ...')

    server = smtplib.SMTP(SERVER,PORT)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.login(FROM,PASS)
    server.sendmail(FROM,TO,msg.as_string()) 
    print('Email Sent...')
    server.quit()