'''
Description:
Python Selenium program to login to every student's Websis account and retrieve
the marks / grades secured for each subject for each semester. The program then
ranks all the sudents by CGPA
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException,NoSuchElementException
import time
import csv
import os

def computeCGPA():
	login_data = dict()
	gpa1_list = dict()
	gpa2_list = dict()
	cgpa_list = dict()
	name_data = dict()


	with open('csis_inputStudentDetails.csv', 'rb') as f:
	    reader = csv.reader(f)
	    # read file row by row
	    for row in reader:
	    	login_data[row[0]] = row[2]
	    	name_data[row[0]] = row[1]

	if(os.stat("csis_retrievedResults.csv").st_size > 0):
		with open('csis_retrievedResults.csv', 'rb') as f:
		    reader = csv.reader(f)
		    # read file row by row
		    for row in reader:
		    	gpa1_list[row[0]] = row[1]
		    	gpa2_list[row[0]] = row[2]
		    	cgpa_list[row[0]] = row[3]


	if(len(cgpa_list.keys())<len(login_data.keys())):
		#For using Firefox
		#driver = webdriver.Firefox(executable_path='/Users/tebbythomas/Downloads/geckodriver')
		#For using Chrome
		driver = webdriver.Chrome('/Users/tebbythomas/Downloads/chromedriver')
		try:
			driver.set_page_load_timeout(180)
			for regNum, bDate in login_data.iteritems():
				if regNum in gpa1_list:
					continue;
				else:
					driver.get("http://websismit.manipal.edu/websis/control/createAnonSession")
					login = driver.find_element_by_xpath("//button[@type='submit']")
					password = driver.find_element_by_xpath("//input[@name='birthDate_i18n']")
					reg_no =  driver.find_element_by_xpath("//input[@name='idValue']")
					reg_no.send_keys(regNum)
					password.send_keys(bDate)
					password.send_keys(Keys.RETURN)
					driver.get("http://websismit.manipal.edu/websis/control/StudentAcademicProfile")
					gpa1_list[regNum] = float(driver.find_element_by_xpath("//span[@id='cc_ProgramAdmissionItemSummary_ptermResultScore_2']").text)
					gpa2_list[regNum] = float(driver.find_element_by_xpath("//span[@id='cc_ProgramAdmissionItemSummary_ptermResultScore_1']").text)
					cgpa_list[regNum] = float(((gpa1_list[regNum] * 24.0) + (gpa2_list[regNum] * 26.0))/50.0)
					print "Name = %s Registration Number = %s CGPA = %f GPA of 2nd Sem = %f " % (name_data[regNum],regNum, cgpa_list[regNum], gpa2_list[regNum])
					with open('csis_retrievedResults.csv', 'ab') as csvfile:
					    filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
					    filewriter.writerow([str(regNum), str(gpa1_list[regNum]),str(gpa2_list[regNum]),str(cgpa_list[regNum])])
					driver.get("http://websismit.manipal.edu/websis/control/clearSession")
		except TimeoutException as ex:
		    print("Timeout Exception has been thrown. " + str(ex))
		    driver.close()
		except NoSuchElementException as ex:
		    print("No Such Element Exception has been thrown. " + str(ex))
		    driver.close()
	else:
		f = open('csis_Ranks_CGPA.txt', 'w')
		rank = 1
		f.write("Ranks based on CGPA:\n")
		for key, value in sorted(cgpa_list.iteritems(), key=lambda (k,v): (v,k), reverse=True):
			f.write("Rank = %s\t Name = %s\t CGPA = %s\t GPA of Sem 1 = %s\t GPA of Sem 2 = %s\n" % (str(rank), str(name_data[key]),str(cgpa_list[key]),str(gpa1_list[key]),str(gpa2_list[key])))
			rank = rank + 1

	'''for i in range(3) :
		for j in range(6) :
			tag = "cc_ListAssessmentScores_obtainedMarks_"+str(j+1)
			marks =  marks + float(driver.find_element_by_xpath("(//span[@id='"+tag+"'])["+str(i+1)+"]").text)
	classMarks[regNum] = marks
	gpa
	driver.get("http://websismit.manipal.edu/websis/control/clearSession")

print classMarks
print "Ranks based on 2nd sem internal marks (out of 300):"
rank = 1
for key, value in sorted(classMarks.iteritems(), key=lambda (k,v): (v,k), reverse=True):
    print "Rank = %d Registration Number = %s Internal Marks = %f GPA of first sem = %f" % (rank, key, value, gpa_list[key])
    rank = rank + 1'''

#login_data = {'160913002':'1991-06-10','160913003':'1991-09-30','160913004':'1989-10-11','160913006':'1990-04-20','160913007':'1994-01-02','160913008':'1993-05-31','160913009':'1990-06-10','160913010':'1993-11-19','160913011':'1992-07-21','160913012':'1993-11-14','160913013':'1991-09-17','160913014':'1994-04-28','160913015':'1994-05-02','160913016':'1993-02-12','160913017':'1990-08-31','160913018':'1989-11-03','160913019':'1991-04-27','160913020':'1993-01-01','160913021':'1994-11-23','160913022':'1992-05-29','160913023':'1993-09-10','160913024':'1994-08-21','160913025':'1994-02-21','160913026':'1994-01-03','160913027':'1993-09-03'}
	#gpa1_list = {'160913002':0.0,'160913003':0.0,'160913004':0.0,'160913006':0.0,'160913007':0.0,'160913008':0.0,'160913009':0.0,'160913010':0.0,'160913011':0.0,'160913012':0.0,'160913013':0.0,'160913014':0.0,'160913015':0.0,'160913016':0.0,'160913017':0.0,'160913018':0.0,'160913019':0.0,'160913020':0.0,'160913021':0.0,'160913022':0.0,'160913023':0.0,'160913024':0.0,'160913025':0.0,'160913026':0.0,'160913027':0.0}
	#gpa2_list = {'160913002':0.0,'160913003':0.0,'160913004':0.0,'160913006':0.0,'160913007':0.0,'160913008':0.0,'160913009':0.0,'160913010':0.0,'160913011':0.0,'160913012':0.0,'160913013':0.0,'160913014':0.0,'160913015':0.0,'160913016':0.0,'160913017':0.0,'160913018':0.0,'160913019':0.0,'160913020':0.0,'160913021':0.0,'160913022':0.0,'160913023':0.0,'160913024':0.0,'160913025':0.0,'160913026':0.0,'160913027':0.0}
	#cgpa_list = {'160913002':0.0,'160913003':0.0,'160913004':0.0,'160913006':0.0,'160913007':0.0,'160913008':0.0,'160913009':0.0,'160913010':0.0,'160913011':0.0,'160913012':0.0,'160913013':0.0,'160913014':0.0,'160913015':0.0,'160913016':0.0,'160913017':0.0,'160913018':0.0,'160913019':0.0,'160913020':0.0,'160913021':0.0,'160913022':0.0,'160913023':0.0,'160913024':0.0,'160913025':0.0,'160913026':0.0,'160913027':0.0}
	#name_list = {'160913002':'Nadiya','160913003':'Sital','160913004':'Tebby','160913006':'Umesh','160913007':'Shruti','160913008':'Sapna','160913009':'Anurag','160913010':'Sonali','160913011':'Pratik','160913012':'Byresh','160913013':'Yogesh','160913014':'Yashika','160913015':'Shobha','160913016':'Anjali','160913017':'Arfin','160913018':'Bhaskar','160913019':'Venkata','160913020':'Ganesh','160913021':'Shrikant','160913022':'Suresh','160913023':'Keerthi','160913024':'Sony','160913025':'Kripa','160913026':'Prasad','160913027':'Gopi'}
