import pdfkit
from flask import Flask, request, render_template
from datetime import date
app = Flask(__name__)

# INSTAGRAM FAX:
#  SNAPCHAT FAX:
#  FACEBOOK FAX:
#   TWITTER FAX:

@app.route("/", methods=['POST', 'GET'])
def hello():
    if request.method == 'POST':
        posts = organizeItems(request.form)
        name  = request.form['name']
        email = request.form['email']
        td    = date.today()
        today = "%d/%d/%d" % (td.month, td.day, td.year)

        render  = render_template('pdf.html', posts=posts[0], postcount=len(posts), name=request.form['name'])
        filepdf = renderPDF(render)
        return render_template('pdf.html', posts=posts[0], postcount=len(posts[0]), name=request.form['name'], today=today, email=email)
    return render_template('form.html')

@app.route("/yerp/", methods=['POST', 'GET'])
def woof():
    return "yerp"

if __name__ == "__main__":
    app.run()

def renderPDF(render):
    options = {
            'print-media-type': '',
            'page-size': 'A4',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'margin-right': '0.75in',
            'margin-top': '0.75in',
            'dpi': 2000
        }
    filename = 'out.pdf'
    pdfkit.from_string(render, filename, options=options)
    return filename

def organizeItems(form):
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
        print key
        network = sites[key]['site']
        if   network == 'facebook' :
            facebook.append(sites[key])
        elif network == 'twitter'  :
            twitter.append(sites[key])
        elif network == 'snapchat' :
            snapchat.append(sites[key])
        elif network == 'instagram':
            instagram.append(sites[key])
    posts = [{'name':'Facebook', 'fax':'+10123456789', 'posts': facebook}, 
             {'name':'Twitter',  'fax':'+10123456789', 'posts': twitter}, 
             {'name':'Snapchat', 'fax':'+10123456789', 'posts': snapchat}, 
             {'name':'Instagram','fax':'+10123456789', 'posts': instagram}]
    return posts