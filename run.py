import pdfkit
from flask import Flask, request, render_template
from datetime import datetime
#from twilio.rest import Client
app = Flask(__name__)
#account_sid = "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
#auth_token = "your_auth_token"
#client = Client(account_sid, auth_token)
# INSTAGRAM FAX:
#  FACEBOOK FAX:
# --------------
#  SNAPCHAT FAX:
#   TWITTER FAX:

@app.route("/", methods=['POST', 'GET'])
def hello():
    if request.method == 'POST':
        print request.form
        rendered = ''
        posts = organizeItems(request.form)
        print "\n\n\n"
        name  = request.form['name']
        email = request.form['email']
        for post in posts:
            #print post
            if len(post['posts']) > 0:
                td      = datetime.now()
                today   = td.strftime("%m/%d/%Y")
                social  = post['name']
                render  = render_template('pdf.html',
                    posts         = post['posts']                 ,
                    postcount     = len(post['posts'])            ,
                    invoice       = td.strftime("%Y%m%d%H%M%S")   ,
                    company       = post['company']               ,
                    name          = request.form['name']          ,
                    email         = request.form['email']         ,
                    tel           = request.form['phone']         ,
                    social        = social                        ,
                    today         = today                         ,
                    address_line1 = request.form['address-line1'] ,
                    address_line2 = request.form['address-line2'] ,
                    country       = request.form['country']       ,
                    city          = request.form['city']          ,
                    region        = request.form['region']        ,
                    postal_code   = request.form['postal-code']   ,  
                    venmo         = request.form['venmo']         ,
                    paypal        = request.form['paypal']        )
                pdfname = td.strftime("%Y%m%d%H%M%S.pdf") # figure out how to format
                filepdf = renderPDF(render, pdfname)
                #fax = client.fax.v1.faxes.create(
                #    from_="+15017250604", #our number
                #    to=post['fax'], # whatever number
                #    media_url="")
        # FAX SHIT HERE
        # WAIT FOR RESPONSE & THEN DELETE PDF (THIS IS A SAFE SPACE BITCH!!!!!)'''
        return render
    return render_template('form.html')

@app.route("/yerp/", methods=['POST', 'GET'])
def woof():
    return "yerp"

if __name__ == "__main__":
    app.run()

def renderPDF(render, filename):
    options = {
            'print-media-type': '',
            'page-size': 'A4',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'margin-right': '0.75in',
            'margin-top': '0.75in',
            'dpi': 1920
        }
    pdfkit.from_string(render, filename, options=options)
    return filename

def organizeItems(form):
    print "organizing....."
    sites = dict()
    for key in request.form.keys():
        if "_" in key:
            yerp = key.split("_")
            if yerp[0] not in sites.keys():
                sites[yerp[0]] = dict()
            sites[yerp[0]][yerp[1]] = request.form[key] 

    facebook  = []
    twitter   = []
    snapchat  = []
    instagram = []

    for key in sites.keys():
        network = sites[key]['site']
        if   network == 'facebook' :
            facebook.append(sites[key])
        elif network == 'twitter'  :
            twitter.append(sites[key])
        elif network == 'snapchat' :
            snapchat.append(sites[key])
        elif network == 'instagram':
            instagram.append(sites[key])
    posts = [{'name':'Facebook', 'company': 'Facebook Inc.', 'fax':'+16505434801', 'posts': facebook}, 
             {'name':'Twitter',  'company': 'Twitter Inc.', 'fax':'+1xxxxxxxxxx', 'posts': twitter }, 
             {'name':'Snapchat', 'company': 'Snap Inc.', 'fax':'+1xxxxxxxxxx', 'posts': snapchat}, 
             {'name':'Instagram','company': 'Facebook Inc.', 'fax':'+16505434801', 'posts': instagram}]
    print posts
    print "....organized!"
    return posts