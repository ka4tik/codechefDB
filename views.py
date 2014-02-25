from django.shortcuts import render
from django.template import RequestContext,loader
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
from django.template import RequestContext,loader
from django.core.context_processors import csrf
import hellodjango.settings as settings
from django.utils.encoding import smart_str, smart_unicode
from django.utils import simplejson
import sqlite3
# def custom_500(request):
#     t = loader.get_template('500.html')

#     print sys.exc_info()
#     type, value, tb = sys.exc_info()
#     return HttpResponseServerError(t.render(Context({
#     'exception_value': value,
#     'value':type,
#     'tb':traceback.format_exception(type, value,
#                                           tb)
#     },RequestContext(request))))
def send_email(TEXT):
            import smtplib
            gmail_user = "ka4tik@gmail.com"
            gmail_pwd = "..."
            FROM = 'ka4tik@gmail.com'
            TO = ['ka4tik@gmail.com'] #must be a list
            SUBJECT = "new query executed"
            # TEXT = "Testing sending mail using gmail servers"

            # Prepare actual message
            message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
            try:
                #server = smtplib.SMTP(SERVER) 
                server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
                server.ehlo()
                server.starttls()
                server.login(gmail_user, gmail_pwd)
                server.sendmail(FROM, TO, message)
                #server.quit()
                server.close()
                print 'successfully sent the mail'
            except:
                print "failed to send mail"
def index(request):
    args={}
    args.update(csrf(request));
    return render_to_response('codechefindex.html',args);
def results(request):
	alpha="";
	if 'alpha' in request.POST:
		alpha=request.POST['alpha']
	context_dict={}
	print settings.DATABASES['codechef']['NAME']
	db=sqlite3.connect(settings.DATABASES['codechef']['NAME'])
	temp_db = sqlite3.connect(':memory:') # create a memory database
	# query2 = smart_str("").join(smart_str(line) for line in db.iterdump())
	c=temp_db.cursor()
	c.execute('''CREATE TABLE users
             (username text primary key,
             name text,
             url text,
             long_rating real,
             short_rating real,
             long_global_rank integer,
             long_country_rank integer,
             short_global_rank integer,
             short_country_rank integer,
             country text,
             state text,
             city text,
             motto text,
             link text,
             about_me text,
             student_professional text,
             institution text
             )''')
	for row in db.cursor().execute('select * from users '):
		c.execute('''insert into users values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',row)
	success="yes"
	try:
		db.cursor().execute('select * from users ')
	except:
		success="no"
	db.close();
	TEXT=alpha+ " query succeded ? = "+ success;
	send_email(TEXT)

	result=""
	# for link in c.execute('select * from users where username="ka4tik"'):
	rows=[]
	c.row_factory = sqlite3.Row
	for row in c.execute(alpha):
		# print type(row);
		rows.append(row)
		context_dict['keys']=row.keys();
	print context_dict['keys'];
	temp_db.close()
	context_dict['alpha']=alpha
	context_dict['rows']=rows
	context_dict['t']=range(len(rows[0]))
	# js_data = simplejson.dumps(rows)
	# context_dict['js_data']=js_data;
	return render_to_response('codechefresult.html',context_dict);
