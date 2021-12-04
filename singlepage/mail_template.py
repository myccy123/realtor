# -*- coding:utf-8 -*-
from email.mime.text import MIMEText
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import smtplib





def welcome_for_signup(userid):
    # 第三方 SMTP 服务
    mail_host="smtp.realtoraccess.com"  #设置服务器
    mail_user="clientservice@realtoraccess.com"    #用户名
    mail_pass="Ra123456"   #口令 
    sender = 'clientservice@realtoraccess.com'
    receivers = [userid,'clientservice@realtoraccess.com','chenli@realtoraccess.com','dxc@realtoraccess.com','yujh@realtoraccess.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    #正文
    message = MIMEMultipart('related')
    message['From'] = Header("clientservice@realtoraccess.com", 'utf-8')
    message['To'] =  Header(userid, 'utf-8')
    message['Bcc'] = 'clientservice@realtoraccess.com,chenli@realtoraccess.com,dxc@realtoraccess.com,yujh@realtoraccess.com'
    #标题
    subject = 'Welcome to Realtoraccess!'
    message['Subject'] = Header(subject, 'utf-8')
    msgAlternative = MIMEMultipart('alternative')
    message.attach(msgAlternative)
    body = '''
    <body style="margin: 0px;">
    <div style="margin: 8px;">
        <div style="height: 120px;width: 195px; margin: auto;"><img style="width: 100%%; object-fit: cover;" src="cid:image1"></div>
        <div style="border-radius: 5px;border-top: 3px solid rgba(0, 205 ,0,0.7); box-shadow: 0px 0px 5px 0px rgba(153,153,153,0.4); max-width: 800px; margin: auto; padding: 20px;">
            <p>Dear <b>%s</b></p>
            <p>Welcome to Realtoraccess and thank you for signing up!</p>
            <p>Realtoraccess is a membership-based global realtor club, dedicated to facilitating global realtors’ access to the Chinese buyers.</p>
            <p>Wechat Marketing & Listing Promotion；Online Branding & Chinese SEOs；Blogging & Email Campaigns; Realtoraccess provides total Chinese marketing solution, which will bring your business to the next level.</p>
            <p>Please feel free to complete information on your dashboard. We will promote your branding by displaying your profile page at <a href="http://www.realtoraccess.com/web/agentlist" style="text-decoration: none; color: #70b1e7!important;">www.realtoraccess.com</a>. The powerful SEO feature brings traffic to your own landing page, and it is free. Hooray!</p>
            <br>
            <p>Complete your profile, maintain your listings or subscribe services with us,<a href="http://www.realtoraccess.com/web/console/" style="text-decoration: none; color: #70b1e7!important;">Sign in here</a> </p>
            <p>If you have any questions or need help with anything, don't hesitate to shoot us an email at <a href="mailto:clientservice@realtoraccess.com" style="text-decoration: none; color: #70b1e7!important;">clientservice@realtoraccess.com</a> </p>
            <br>
        </div>
    </div>
    <div style="width: 20%%; border-bottom: 1px solid #333;margin-top: 100px; margin-left: 8px;"></div>
    <div style="">
        <p style="font-size: 14px; padding: 8px; margin: 0px;">This email was sent to you by <a href="www.realtoraccess.com/" style="text-decoration: none; color: #70b1e7!important;">Realtoraccess.com</a></p>
        <p style="font-size: 14px; padding: 8px; margin: 0px;">Headquarter: B-2003-033, 17th floor, Building 1, #18 East Road Zhongguancun, Haidian District, Beijing, China 100083</p>
        <p style="font-size: 14px; padding: 8px; margin: 0px;">Vancouver: 1788 Ontario St.Vancouver. BC V5T OG3 Canada</p>
    </div>
    </body>
    ''' % userid
    msgAlternative.attach(MIMEText(body, 'html', 'utf-8'))
    fp = open(r'/root/myweb/static/web/img/email_logo.png', 'rb')
#     fp = open(r'C:\Users\myccy\Desktop\email_logo.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '<image1>')
    message.attach(msgImage)
    try:
        smtpObj = smtplib.SMTP() 
    #     smtpObj = SMTP_SSL(mail_host)
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "send mail successfully!"
    except smtplib.SMTPException as e:
        print e,"Error: send mail failed!"

def send_password_code(userid,token):
    # 第三方 SMTP 服务
    mail_host="smtp.mxhichina.com"  #设置服务器
    mail_user="clientservice@realtoraccess.com"    #用户名
    mail_pass="Ra123456"   #口令 
    sender = 'clientservice@realtoraccess.com'
    receivers = [userid]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    #正文
    message = MIMEMultipart('related')
    message['From'] = Header("clientservice@realtoraccess.com", 'utf-8')
    message['To'] =  Header(userid, 'utf-8')
    #标题
    subject = 'Password Reset Link-Realtoraccess'
    message['Subject'] = Header(subject, 'utf-8')
    msgAlternative = MIMEMultipart('alternative')
    message.attach(msgAlternative)
    body = '''
            <body style="margin: 0px;">
            <div style="margin: 8px;">
            <p>Dear   <b>%s</b></p>
            <br>
            <p>A request has been made to reset your password for your account with Realtoraccess.com. Please input the following verification code to continue.</p>
            <p>Verification Code:</p>
            <h1>%s</h1>
            <br>
            <br>
            </div>
            <div style="width: 20%%; border-bottom: 1px solid #333;margin-top: 100px; margin-left: 8px;"></div>
            <div style="">
                <p style="font-size: 14px; padding: 8px; margin: 0px;">This email was sent to you by <a href="www.realtoraccess.com/" style="text-decoration: none; color: #70b1e7!important;">Realtoraccess.com</a></p>
                <p style="font-size: 14px; padding: 8px; margin: 0px;">Headquarter: B-2003-033, 17th floor, Building 1, #18 East Road Zhongguancun, Haidian District, Beijing, China 100083</p>
                <p style="font-size: 14px; padding: 8px; margin: 0px;">Vancouver: 1788 Ontario St.Vancouver. BC V5T OG3 Canada</p>
            </div>
            </body>
    ''' % (userid,token)
    try:
        msgAlternative.attach(MIMEText(body, 'html', 'utf-8'))
        smtpObj = smtplib.SMTP() 
    #     smtpObj = SMTP_SSL(mail_host)
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "send mail successfully!"
    except smtplib.SMTPException as e:
        print e,"Error: send mail failed!"

def ask_for_voince(userid,ivc):
    # 第三方 SMTP 服务
    mail_host="smtp.mxhichina.com"  #设置服务器
    mail_user="clientservice@realtoraccess.com"    #用户名
    mail_pass="Ra123456"   #口令 
    sender = 'clientservice@realtoraccess.com'
    receivers = [userid,'chenli@realtoraccess.com','finance@realtoraccess.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    #正文
    message = MIMEMultipart('related')
    message['From'] = Header("clientservice@realtoraccess.com", 'utf-8')
    message['To'] =  Header(userid, 'utf-8')
    message['Bcc'] = 'chenli@realtoraccess.com,finance@realtoraccess.com'
    #标题
    subject = 'Your invoice will be sent to you soon!'
    message['Subject'] = Header(subject, 'utf-8')
    msgAlternative = MIMEMultipart('alternative')
    message.attach(msgAlternative)
    body = '''
            <body style="margin: 0px;">
            <div style="margin: 8px;">
            <p>Dear   <b>%s</b></p>
            <br>
            <p>We have received your request of sending in your invoice - (Type: %s/ Fee:%s/ Token ID: %s). </p>
            <p>Our finance will prepare your invoice and send it to your email. </p>
            <a href="http://www.realtoraccess.com/web/console/" style="text-decoration: none; color: #70b1e7!important;">Visit your dashboard to chat with us for any questions!</a>
            <br>
            <br>
            <p>Regards,</p>
            </div>
            <div style="width: 20%%; border-bottom: 1px solid #333;margin-top: 100px; margin-left: 8px;"></div>
            <div style="">
                <p style="font-size: 14px; padding: 8px; margin: 0px;">This email was sent to you by <a href="www.realtoraccess.com/" style="text-decoration: none; color: #70b1e7!important;">Realtoraccess.com</a></p>
                <p style="font-size: 14px; padding: 8px; margin: 0px;">Headquarter: B-2003-033, 17th floor, Building 1, #18 East Road Zhongguancun, Haidian District, Beijing, China 100083</p>
                <p style="font-size: 14px; padding: 8px; margin: 0px;">Vancouver: 1788 Ontario St.Vancouver. BC V5T OG3 Canada</p>
            </div>
            </body>
    ''' % (userid,ivc.get('service'),ivc.get('fee'),ivc.get('token'))
    try:
        msgAlternative.attach(MIMEText(body, 'html', 'utf-8'))
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "send mail successfully!"
    except smtplib.SMTPException as e:
        print e,"Error: send mail failed!"

def cust_msg(userid,msg):
    # 第三方 SMTP 服务
    mail_host="smtp.mxhichina.com"  #设置服务器
    mail_user="clientservice@realtoraccess.com"    #用户名
    mail_pass="Ra123456"   #口令 
    sender = 'clientservice@realtoraccess.com'
    receivers = [userid,'clientservice@realtoraccess.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    #正文
    message = MIMEMultipart('related')
    message['From'] = Header("clientservice@realtoraccess.com", 'utf-8')
    message['To'] =  Header(userid, 'utf-8')
    message['Bcc'] = 'clientservice@realtoraccess.com'
    #标题
    subject = 'new message!'
    message['Subject'] = Header(subject, 'utf-8')
    msgAlternative = MIMEMultipart('alternative')
    message.attach(msgAlternative)
    body = '''
            <body style="margin: 0px;">
            <div style="margin: 8px;">
            <p>Dear   <b>%s</b></p>
            <br>
            <p>A lead just left a message on your feature property URL <a href="%s">%s</a>. Here is the message:</p>
            <p>Name: %s</p>
            <p>E-mail: %s</p>
            <p>TEL: %s</p>
            <p>Message: %s</p>
            <br>
            <br>
            <p>We wish you all the success of your business!</p>
            </div>
            <div style="width: 20%%; border-bottom: 1px solid #333;margin-top: 100px; margin-left: 8px;"></div>
            <div style="">
                <p style="font-size: 14px; padding: 8px; margin: 0px;">This email was sent to you by <a href="www.realtoraccess.com/" style="text-decoration: none; color: #70b1e7!important;">Realtoraccess.com</a></p>
                <p style="font-size: 14px; padding: 8px; margin: 0px;">Headquarter: B-2003-033, 17th floor, Building 1, #18 East Road Zhongguancun, Haidian District, Beijing, China 100083</p>
                <p style="font-size: 14px; padding: 8px; margin: 0px;">Vancouver: 1788 Ontario St.Vancouver. BC V5T OG3 Canada</p>
            </div>
            </body>
    ''' % (userid,msg.get('url'),msg.get('url'),msg.get('name'),msg.get('email'),msg.get('tel'),msg.get('msg'))
    try:
        msgAlternative.attach(MIMEText(body, 'html', 'utf-8'))
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "send mail successfully!"
    except smtplib.SMTPException as e:
        print e,"Error: send mail failed!"
