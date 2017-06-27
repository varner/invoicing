import os, sys, subprocess
import pdfkit
from flask import Flask, request, render_template
from datetime import datetime

# AMAZON SHIT
import boto
from boto.s3.key import Key
conn = boto.s3.connect_to_region('us-east-2', aws_access_key_id=os.environ['S3_KEY'], aws_secret_access_key=os.environ['S3_SECRET'])

# TWILIO SHIT
#from twilio.rest import Client
#account_sid = "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
#auth_token = "your_auth_token"
#client = Client(account_sid, auth_token)

# FLASK SHIT
app = Flask(__name__)
# INSTAGRAM FAX:
#  FACEBOOK FAX:
# --------------
#  SNAPCHAT FAX:
#   TWITTER FAX:

@app.route("/", methods=['POST', 'GET'])
def hello():
    if request.method == 'POST':
        # Ensure virtualenv path is part of PATH env var
        os.environ['PATH'] += os.pathsep + os.path.dirname(sys.executable)  
        WKHTMLTOPDF_CMD = subprocess.Popen(
            ['which', os.environ.get('WKHTMLTOPDF_BINARY', 'wkhtmltopdf')], # Note we default to 'wkhtmltopdf' as the binary name
            stdout=subprocess.PIPE).communicate()[0].strip()
        print request.form
        rendered = ''
        posts = organizeItems(request.form)
        print "\n\n\n"
        name  = request.form['name']
        email = request.form['email']
        renders = dict()
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
                filepdf = renderPDF(render, pdfname, WKHTMLTOPDF_CMD)
                # UPLOAD TO S3
                url = uploadS3(filepdf, pdfname)
                media_url = "https://badlands-invoice.s3.us-east-2.amazonaws.com/%s" % pdfname
                renders[social] = media_url
        # FAX SHIT HERE
        #if renders.get('Facebook'): fax(renders['Facebook'], '+16505434801')
        #if renders.get('Instagram'): fax(renders['Instagram'], '+16505434801')
        # WAIT FOR RESPONSE & THEN DELETE PDF (THIS IS A SAFE SPACE BITCH!!!!!)'''
        return render_template('thanks.html', renders=renders)
    return render_template('form.html')

@app.route("/yerp/", methods=['POST', 'GET'])
def woof():
    return "yerp"

def fax(media_url, phone):
    fax = client.fax.v1.faxes.create(
                    from_="+15017250604", #our number
                    to=phone, # whatever number
                    media_url=media_url)
    return

def uploadS3(pdf, filename):
    bucket = conn.get_bucket('badlands-invoice', validate=False)
    k = Key(bucket)
    k.key = filename
    k.set_contents_from_string(pdf,replace=True,
                                   headers={'Content-Type': 'application/pdf'},
                                   policy='authenticated-read',
                                   reduced_redundancy=True)
    return k.generate_url(expires_in=600, force_http=True)

def renderPDF(render, filename, WKHTMLTOPDF_CMD):
    pdfkit_config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_CMD)
    options = {
            'print-media-type': '',
            'page-size': 'A4',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'margin-right': '0.75in',
            'margin-top': '0.75in',
            'dpi': 300#1920
        }
    pdf = pdfkit.from_string(render, False, options=options, configuration=pdfkit_config)
    pdfkit.from_string(render, filename, options=options)
    return pdf

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

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)