import base64       
from robobrowser import RoboBrowser
import time

def getAttendance(usn,dob):
    br = RoboBrowser(parser="html.parser",history=True)
    br.open("http://parents.msrit.edu/index.php")
    form = br.get_form()
    form['username'] = usn
    passw = dob
    s =''
    for i in range(0,len(passw)):
        s+=passw[i]+'aa'
    encoded = base64.b64encode(bytes(s,"utf-8"))
    form['password'] = encoded
    form['passwd'] = encoded
    br.submit_form(form)
    final ={}
    
    if("[]"!=str(br.find_all("input",id="username"))):
        final['ResultCode']="Fail"
    else:
        attend = []
        per =[]
        res={}
        for y in br.find_all("div",attrs={"class": "coursename"}):
            attend.append(str(y.string))
        for x in br.find_all("div",attrs={"class": "att"}):
            details = {}
            details['Attendance'] = str(x.contents[0].string).replace('%','')
            br.follow_link(x.contents[0])
            pre = br.find("div",attrs={"class":"progress-bar progress-bar-success"})
            clas = str(pre.string).strip()
            if(len(clas)==0):
                details['NoOfClassesAttended']=0
            else:
                details['NoOfClassesAttended']=int(clas)
            
            present=[]
            absent=[]
            xd = br.find_all("tr",attrs={"class":"odd"})
            for x in xd:
                b = x.find_all("td")
                flag = len(x.find_all("td",attrs={"style":"color: red;"}))
                if(flag==1):
                    absent.append(time.strptime(str(b[1].string).strip(), "%d-%m-%Y"))
                else:
                    present.append(time.strptime(str(b[1].string).strip(), "%d-%m-%Y"))
            
            xd = br.find_all("tr",attrs={"class":"even"})
            for x in xd:
                b = x.find_all("td")
                flag = len(x.find_all("td",attrs={"style":"color: red;"}))
                if(flag==1):
                    absent.append(time.strptime(str(b[1].string).strip(), "%d-%m-%Y"))
                else:
                    present.append(time.strptime(str(b[1].string).strip(), "%d-%m-%Y"))
            if(len(present)==0 and len(absent)==0):
                details['AsOn']='nil'
                details['Present']='nil'
                details['Absent']='nil'
            else:
                pTemp = []
                aTemp = []
                asOn = 0
                if(len(present)==0):
                    details['Present']='nil'
                    asOn=max(absent)
                    for m in absent:
                        aTemp.append(str(m.tm_mday)+"-"+str(m.tm_mon)+"-"+str(m.tm_year))
                    details['Absent']=aTemp
                else:
                    details['Absent']='nil'
                    for m in present:
                        pTemp.append(str(m.tm_mday)+"-"+str(m.tm_mon)+"-"+str(m.tm_year))
                    details['Present']=pTemp
                    asOn = max(present)
                if(len(present)!=0 and len(absent)!=0):
                    asOn = max(max(present),max(absent))
                    
                
                details['AsOn']=str(asOn.tm_mday)+"-"+str(asOn.tm_mon)+"-"+str(asOn.tm_year)
                
                
            per.append(details)
        for i in range(0,len(attend)):
            res[attend[i]]=per[i]
        final["Result"]=res
        final["ResultCode"]="Success"
    return final

def isStudent(usn,dob):
    br = RoboBrowser(parser="html.parser")
    br.open("http://parents.msrit.edu/index.php")
    form = br.get_form()
    form['username'] = usn
    passw = dob
    s =''
    for i in range(0,len(passw)):
        s+=passw[i]+'aa'
    encoded = base64.b64encode(bytes(s,"utf-8"))
    form['password'] = encoded
    form['passwd'] = encoded
    br.submit_form(form)
    if("[]"!=str(br.find_all("input",id="username"))):
        return False
    else:
        return True
def getDetails(usn,dob):
    br = RoboBrowser(parser="html.parser")
    br.open("http://parents.msrit.edu/index.php")
    form = br.get_form()
    form['username'] = usn
    passw = dob
    s =''
    for i in range(0,len(passw)):
        s+=passw[i]+'aa'
    encoded = base64.b64encode(bytes(s,"utf-8"))
    form['password'] = encoded
    form['passwd'] = encoded
    br.submit_form(form)
    final = {}
    if("[]"!=str(br.find_all("input",id="username"))):
        final['ResultCode']='Fail'
    else:
        details={}
        n = br.find_all("div",class_="tname2")
        details["Name"]=str(n[0].string).strip()
        sem = str(n[2].string).split()
        details["Semester"]=int(sem[1])
        j = br.find("img",class_="imagize")
        details["Image"]="http://parents.msrit.edu/"+j['src']
        ce=str(n[3].string).split(":")
        details["CreditsEarned"]=int(ce[1].strip())
        ce=str(n[4].string).split(":")
        details["CreditsToEarn"]=int(ce[1].strip())
        final['ResultCode']="Success"
        final['Result']=details
    return final