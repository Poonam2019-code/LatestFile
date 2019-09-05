from rasa_core.actions import Action
from rasa_core.events import Restarted
from rasa_core.actions.forms import (
    BooleanFormField,
    EntityFormField,
    FormAction,
    FreeTextFormField
)
from rasa_core_sdk.events import SlotSet
import httplib2
import requests
from requests.auth import HTTPBasicAuth
import json
import urllib.request as urllib
from bs4 import BeautifulSoup

 



username='parimalPatel123@yahoo.com'
password='Accenture@123'
headers={'Content-Type':'application/json'}
resp=[]
temp= list()
summary=""
description=""
base=""
_links=""
results=""
webui=""
data=[]

class ActionCheckWord(FormAction):

	RANDOMIZE = False
	
	@staticmethod
	def required_fields():
		return [
			EntityFormField("word", "word")
			]
			
	def name(self):
		return "action_checkword"
		
	def submit(self, dispatcher, tracker, domain):
		a=str(tracker.get_slot("word"))
		URL = "https://nnsha.atlassian.net/wiki/rest/api/content/search?cql=text~"+a
		#dispatcher.utter_message("URL :" + URL)
		auth = HTTPBasicAuth("nishans1625@gmail.com", "aA5ewNugsl30hT2dfVL91942")
		query = {'cql': '{cql}'}
		response="Document Found!! You can go to the following URL:-"
		dispatcher.utter_message(response)
		resp=requests.get(URL,headers=headers,params=query,auth=auth,verify=False)
			#data=json.loads(resp.text)
			#webui=data['results'][0]['_links']['webui']
			#base=data['_links']['base']
		data=json.loads(resp.text)
		data1=data['results'][0]['_links']
		data2=data['_links']['base']
		for i in data.items():
			for j in i[1]:
				data3=data2+j['_links']['webui']
				dispatcher.utter_message(data3)
		return []
		
		
class ActionCodeCoverage(FormAction):

	RANDOMIZE = False

	@staticmethod
	def required_fields():
		return [
			EntityFormField("codecoverageapp", "codecoverageapp")
			]

	def name(self):
		# you can then use action_example in your stories
		return "action_checkcodecoverage"

	def submit(self, dispatcher, tracker, domain):
		# what your action should do
		s=str(tracker.get_slot("codecoverageapp"))
		if s=='javaapp':
			response="Cool! the Coverage is 83% within baseline. Sonarqube URL: https://mysonarqube.com/javaapp"
			dispatcher.utter_message(response)
		elif s=='testapp':
			response="Opps !!! the Coverage is 47% which is very low. Sonarqube URL: https://mysonarqube.com/testapp"
			dispatcher.utter_message(response)
		else:
			dispatcher.utter_message("Opps, looks like your application doesn't have code coverage")
		return []


class ActionCheckService(FormAction):

	RANDOMIZE = False

	@staticmethod
	def required_fields():
		return [
			EntityFormField("servicename", "servicename")
			]

	def name(self):
		# you can then use action_example in your stories
		return "action_checkservice"

	def submit(self, dispatcher, tracker, domain):
		# what your action should do
		s=str(tracker.get_slot("servicename"))
		URL="https://www."+s+".com"
		try:
			resp, content = httplib2.Http().request(URL)
			if resp.status==200:
				response="""{} is up and running  """.format(URL)
				dispatcher.utter_message(response)
			elif resp.status==302:
				response="""{} is up and running  """.format(URL)
				dispatcher.utter_message(response)
			else:
				dispatcher.utter_message("Errorcode :"+str(resp.status)+" For website:"+URL)
		except:
			dispatcher.utter_message("Sorry! an exception occured in accessing "+s+" website")
		return []


class ActionStartJenkinsBuild(FormAction):

	RANDOMIZE = False

	@staticmethod
	def required_fields():
		return [
			EntityFormField("jenkinsjob", "jenkinsjob")
			]

	def name(self):
		# you can then use action_example in your stories
		  return "action_jenkins"

	def submit(self, dispatcher, tracker, domain):
		# what your action should do
		jobname=[]
		job=str(tracker.get_slot('jenkinsjob'))
		URL="http://localhost:8080/api/json?tree=jobs[name]"
		#dispatcher.utter_message('URL :' + URL)
		response = urllib.Request(URL)
		result = urllib.urlopen(response)
		data = json.load(result)
		for job in data['jobs']:
			jobname.append(job['name'])
		#dispatcher.utter_message(str(jobname))
		html="""
		<html>
		<head>
		<body>
		<p>
        <input type="button" style="margin:10px 0;" onclick="populateSelect()"  value="Click to select from list of jobs" />
		</p>
		<select id="ddlCustomers" onchange="show(this)">
		</select>
		<p id="msg"></p>
		<script type="text/javascript">
        function populateSelect() {
			var customers= """+str(jobname)+""";	
			var ddlCustomers = document.getElementById("ddlCustomers");
			for (var i = 0; i < customers.length; i++) {
                var option = document.createElement("OPTION");
                option.innerHTML = customers[i];
                option.value = customers[i];
                ddlCustomers.options.add(option);
            }
        }				
		function show(ele) {
        var msg = document.getElementById('msg');
        msg.innerHTML = 'Selected Job: <b>' + ele.options[ele.selectedIndex].text + '</b> </br>' +
        'ID: <b>' + ele.value + '</b>';
		document.getElementById('msgIp').value=ele.options[ele.selectedIndex].text;
		}
		</script>
		</body>
		</head>
		</html>
		"""
		dispatcher.utter_message(html)
		return[]
class ActionStartJenkinsBuildWithParams(FormAction):
	RANDOMIZE = False
	@staticmethod
	def required_fields():
		return [
			EntityFormField("appname", "appname"),
			EntityFormField("environment", "environment")
			]
	def name(self):
		return "action_jenkins_param"

	def submit(self, dispatcher, tracker, domain):
		job = str(tracker.get_slot("appname"))
#               if(tracker.get_slot("param")=="environment"):
#               param = "Environment"
		pvalue = str(tracker.get_slot("environment")).upper()
		URL = "http://localhost:8080/job/"+job+"/buildWithParameters?token=remote_enable_token&Environment="+pvalue
		dispatcher.utter_message("URL :" + URL)
		try:
			resp, content = httplib2.Http().request(URL)
			if resp.status==201:
				response=job+" Job successfully triggered in "+pvalue
				dispatcher.utter_message(response)
			else:
				dispatcher.utter_message("status code :"+str(resp.status))
				dispatcher.utter_message(content.decode())
		except:
			dispatcher.utter_message("Sorry! an exception occured in triggering the job")
		return []        

class ActionGetJIRAStatus(FormAction):
	RANDOMIZE = False
	@staticmethod
	def required_fields():
		return [
			EntityFormField("JIRAID", "JIRAID")
			]
	def name(self):
		return "action_GetJIRAStatus_param"

	def submit(self, dispatcher, tracker, domain):
		ID = str(tracker.get_slot("JIRAID"))
		URL = "https://parimalpatel123.atlassian.net/rest/api/2/issue/"+ID+"?fields=status"
		#dispatcher.utter_message("URL :" + URL)
		try:
			resp=requests.get(URL,headers,auth=(username,password),verify=False) 

			if resp.status_code==201:
				response="Status Returned Successfully"
				dispatcher.utter_message(response)
				dispatcher.utter_message(resp.text)
			else:
				   # dispatcher.utter_message("status code :"+str(resp.status_code))
				a = resp.json()
				dispatcher.utter_message(a['fields']['status']['description'])
				
		except:
			dispatcher.utter_message(resp.text)
			dispatcher.utter_message(resp.status_code)
		return []

class ActionGetJIRACreate(FormAction):
	RANDOMIZE = False
	@staticmethod
	def required_fields():
		return [
			EntityFormField("summary", "summary"),
			EntityFormField("description", "description"),
			EntityFormField("priority", "priority")
			]
	def name(self):
		return "action_createJIRArequest_param"

	def submit(self, dispatcher, tracker, domain):
		summary = str(tracker.get_slot("summary"))
		description = str(tracker.get_slot("description"))
		priority = str(tracker.get_slot("priority"))		
		samplejson={
				"fields":
					{
			"project":
							{
								"key": "TS"
							},
						"summary": summary,
						"description": description,
						"issuetype":
							{
								"name": "Task"
							},
						"priority":
							{
								"name":"High"
							}
					}
		}
		URL = "https://parimalpatel123.atlassian.net/rest/api/2/issue/"
		#dispatcher.utter_message("URL :" + URL)
		disp = "https://parimalpatel123.atlassian.net/projects/TS/queues/custom/8/"
		try:
			resp=requests.post(URL,json=samplejson,auth=(username,password))
			a=resp.json()
			dispatcher.utter_message("New Issue is created with ID : "+a['key'])
			dispatcher.utter_message("You can find the details at : "+disp+a['key'])
		except:
			dispatcher.utter_message(resp.text)
			#dispatcher.utter_message(resp.status_code)
		return []
	


class ActionSearchRestaurants(FormAction):

    RANDOMIZE = False

    @staticmethod
    def required_fields():
	    return [
		    EntityFormField("cuisine", "cuisine"),
		    EntityFormField("number", "people")
		    ]

    def name(self):
	    return "action_search_restaurants"

    def submit(self, dispatcher, tracker, domain):
	    results = RestaurantAPI().search(
		    tracker.get_slot("cuisine"),
		    tracker.get_slot("people"))
	    return [SlotSet("search_results", results)]
		


class ActionRestarted(Restarted):
        def name(self):
                return "action_chat_restart"

        def run(self, dispatcher, tracker, domain):
                return [Restarted()]
