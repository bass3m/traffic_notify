import smtplib
from email.mime.text import MIMEText
from traffic_notify.settings import TRAFFIC_NOTIFY

def get_notification_env(notif_env):
    sender_email = TRAFFIC_NOTIFY['subscriber']['email']
    sender_passwd = TRAFFIC_NOTIFY['subscriber']['passwd']
    notif_env.setdefault('sender',sender_email)
    notif_env.setdefault('sender_passwd',sender_passwd)
    return notif_env

def construct_notification_body(email_delivery_time, traffic_dict_list):
    traffic_notification_body = [e['name'] + ". Current Speed: " + \
            e.get('speed','') + ". % of speed limit: " + e.get('limit','')\
            if 'speed' in e.keys() else e['name'] + '' \
            for e in traffic_dict_list[1:]]
    # Header {'highway': highway, 'direction': 'direction', 'id': 'hwy_id'}
    # include the time when the traffic snapshot was taken
    traffic_header = "Traffic Conditions for " +\
                traffic_dict_list[0]['highway'] +"-"+\
                traffic_dict_list[0]['direction'] +\
                " @Time: {0}\n".format(email_delivery_time)
    # now add the header to the list
    traffic_notification_body.insert(0,traffic_header)
    return traffic_notification_body

def notify_subscriber(email,email_delivery_time,traffic_dict_list):
    # will plan to clean this up and provide different
    # notification mechanisms, for now just email
    traffic_notification_body = construct_notification_body(email_delivery_time,
                                                            traffic_dict_list)
    notify_subscriber_by_email(email,traffic_notification_body)

def notify_subscriber_by_email(email,traffic_update) :
    notif_env = {}
    get_notification_env(notif_env)
    # make sure configuration is valid
    if notif_env['sender'] and notif_env['sender_passwd']:
        msg = MIMEText('\n'.join(traffic_update))
        msg['Subject'] = traffic_update[0]
        msg['From'] = notif_env['sender']
        msg['To'] = email

        server = smtplib.SMTP('smtp.gmail.com',587) #port 465 or 587
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(notif_env['sender'],notif_env['sender_passwd'])
        server.sendmail(notif_env['sender'],email,msg.as_string())
        server.quit()
