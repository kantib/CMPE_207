import socket
import threading
import MySQLdb

REQUEST_TYPE_LOGIN = "login"
REQUEST_TYPE_INQUIRY = "enquiry"
AUTHENTICATION_FAILURE = "authentication_failed"
AUTHENTICATION_SUCCESSFUL = "authentication_successfull"

SUCCESS = 0
ERROR = 1
LOGOUT = 2
class Response(object):
    def __init__(self):
        self.resType = ''
        self.resParams = {}

    def toString(self):
        s = "{}".format(self.resType)
        for k,v in self.resParams.items():
            s = "{}::{}:{}".format(s, k, v)
        print"Response sent ==> " + s
        return s

class Request(object):
    def __init__(self, buf):
        print "Request Received ==> "+buf
        values = buf.split('::')
        self.reqType = values[0]
        #print "Request Received ==> "+self.reqType
        self.reqParams = {}
        for elem in values[1:]:
            k, v = elem.split(':')
            self.reqParams[k] = v
            #print "\""+k+":"+v+"\" "


        
class Client(threading.Thread):
    def __init__(self, sock, addr):
        threading.Thread.__init__(self)
        self.sock = sock
        self.addr = addr
        self.db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="vaibhav", db="Bank")
        self.cursor = self.db.cursor()

    def send_error(self,msgtype,errmsg):
        #create response to send an error
        resp = Response()
        resp.resType = msgtype
        resp.resParams['status']='FAILED'
        resp.resParams['error']=errmsg
        self.sock.send(resp.toString())

    def process_request(self,buf):
        req = Request(buf)
        if req.reqType == 'LOGIN':
            return self.check_login(req)
        elif req.reqType == 'GET':
            self.service_get_request(req)    
        elif req.reqType == 'SET':
            self.service_set_request(req)
        else:
            #create response to send an error
            resp = Response()
            resp.resType = 'UNKNOWN_REQUEST'
            resp.resParams['status']='FAILED'
            resp.resParams['error']="invalid request type."
            self.sock.send(resp.toString())
            return ERROR

    def check_login(self, req):
        resp = Response()

        if "username" not in req.reqParams or \
            "password" not in req.reqParams or \
            req.reqParams["username"] == "" or \
            req.reqParams["password"] == "":
                self.send_error('LOGIN_RESPONSE','Invalid Username or password')
                #self.sock.close()
                return ERROR
        else: 
            sql = "SELECT * from customer_login WHERE USERNAME='{x}' AND PASSWORD='{y}'".format(x=req.reqParams["username"],y=req.reqParams["password"]) 
            print "sql query ==> " + sql
            try:
                self.cursor.execute(sql)
            except Exception as e:
                print e
                print "calling auth failure server side error"
                self.send_error('LOGIN_RESPONSE', 'Server side error')
                #self.sock.close()
                return ERROR
            
            # fetch results (its a list)
            results = self.cursor.fetchone()
            if not results:
                print "calling auth failure user does not exist"
                self.send_error('LOGIN_RESPONSE','User does not exist')
                #self.sock.close()
                return  ERROR
            else:
                print "INSIDE ELSE BLOCK"
                print results[0]+","+results[1]+","+str(results[2])+","+results[7]
                resp.resType = 'LOGIN_RESPONSE'
                resp.resParams['status']='SUCCESS'
                resp.resParams['client_type']=results[7]
                resp.resParams['client_id']=str(results[2])
                self.sock.send(resp.toString())
                return SUCCESS

    def service_get_request(self, req):
        resp = Response()

        if req.reqParams['subreq_type'] == 'CUSTOMER_ID':
            self.get_customer_id(req)
        elif req.reqParams['subreq_type'] == 'CUSTOMER_ACCT':
            self.get_customer_acct(req)
        elif req.reqParams['subreq_type'] == 'CUSTOMER_PROFILE':
            self.get_customer_profile(req)
        else:
            self.send_error('GET_RESPONSE','Invalid Sub request sent.')
            return ERROR

    def get_customer_profile(self, req):
        if "customer_id" not in req.reqParams or \
                req.reqParams["customer_id"] == "" :
            self.send_error('GET_RESPONSE','Invalid Customer ID')
            return ERROR
        else: 
            resp = Response()
            sql = "SELECT * from CUSTOMER_INFO_TABLE WHERE CUSTOMER_ID='{x}'".format(x=req.reqParams["customer_id"]) 
            print "sql query ==> " + sql
            try:
                self.cursor.execute(sql)
            except Exception as e:
                print e
                self.send_error('GET_RESPONSE', 'Server error: DB operation failed.')
                return ERROR

            # fetch results (its a list)
            results = self.cursor.fetchone()
            if not results:
                print "get request failure:Record does not exist"
                self.send_error('GET_RESPONSE','Record does not exist')
                return ERROR
            else:
                print str(results[0])+","+results[1]+","+results[2]+","+results[3]+","+results[4]+","+results[5]+","+results[6]
                
                resp.resType = 'GET_RESPONSE'
                resp.resParams['status']='SUCCESS'
                resp.resParams['customer_id']=results[0]
                resp.resParams['first_name']=results[1]
                resp.resParams['last_name']=results[2]
                resp.resParams['DOB']=results[3]
                resp.resParams['email']=results[4]
                resp.resParams['phone']=results[5]
                resp.resParams['address']=results[6]
                self.sock.send(resp.toString())
                return SUCCESS


    def get_customer_id(self, req):
        if "customer_name" not in req.reqParams or \
                req.reqParams["customer_name"] == "" :
            self.send_error('GET_RESPONSE','Invalid Username or password')
            return ERROR
        else: 
            resp = Response()
            sql = "SELECT * from customer_login WHERE USERNAME='{x}'".format(x=req.reqParams["customer_name"]) 
            print "sql query ==> " + sql
            try:
                self.cursor.execute(sql)
            except Exception as e:
                print e
                print " DB execute error"
                self.send_error('GET_RESPONSE', 'Server side error')
                return ERROR

            # fetch results (its a list)
            results = self.cursor.fetchone()
            if not results:
                print "get request failure:Record does not exist"
                self.send_error('GET_RESPONSE','Record does not exist')
                return ERROR
            else:
                print "User_name: "+ req.reqParams['customer_name'] +","+"Id: "+ str(results[2])
                resp.resType = 'GET_RESPONSE'
                resp.resParams['status']='SUCCESS'
                resp.resParams['client_id']=results[2]
                self.sock.send(resp.toString())
                return SUCCESS

    def get_customer_chk_acct(self,customer_id):
        sql = "SELECT * from ACCOUNT_TABLE WHERE CUSTOMER_ID='{x}'".format(x=customer_id) 
        print "sql query ==> " + sql
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print e
            return ERROR
            
        # fetch results (its a list)
        results = self.cursor.fetchone()
        if not results:
            return  ERROR
        else:
            return results[1], results[3]

    def get_customer_sav_acct(self,customer_id):
        sql = "SELECT * from ACCOUNT_TABLE WHERE CUSTOMER_ID='{x}'".format(x=customer_id) 
        print "sql query ==> " + sql
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print e
            return ERROR
            
        # fetch results (its a list)
        results = self.cursor.fetchone()
        if not results:
            return  ERROR
        else:
            return results[2], results[4]


    def get_customer_acct(self, req):
        if "customer_id" not in req.reqParams or \
                req.reqParams["customer_id"] == "":
            self.send_error('GET_RESPONSE','Invalid key-value entries for customer_id')
            return ERROR
        else: 

            chk_acct_num, chk_acct_bal = self.get_customer_chk_acct(req.reqParams['customer_id'])
            sav_acct_num, sav_acct_bal = self.get_customer_sav_acct(req.reqParams['customer_id'])

            if chk_acct_num == '' or chk_acct_bal == '' or \
                    sav_acct_num == '' or sav_acct_num == '':
                print "Failed to GET Records"
                self.send_error('GET_RESPONSE','Get operation failed')
                return  ERROR
            else:
                resp = Response()
                print "INSIDE ELSE BLOCK"
                resp.resType = 'GET_RESPONSE'
                resp.resParams['status']='SUCCESS'
                resp.resParams['customer_id'] = req.reqParams['customer_id']
                resp.resParams['chk_acct'] = chk_acct_num
                resp.resParams['chk_bal'] = chk_acct_bal
                resp.resParams['sav_acct'] = sav_acct_num
                resp.resParams['sav_bal'] = sav_acct_bal
                self.sock.send(resp.toString())
                return SUCCESS


    def service_set_request(self, req):
        if req.reqParams['subreq_type'] == 'UPDATE_CHK_ACCT':
            self.update_customer_acct(req)

        elif req.reqParams['subreq_type'] == 'UPDATE_SAV_ACCT':
            self.update_customer_acct(req)

        elif req.reqParams['subreq_type'] == 'UPDATE_CUSTOMER_PROFILE':
            self.update_customer_profile(req)

        else:
            self.send_error('GET_RESPONSE','Invalid Sub request sent.')
            return ERROR


    def update_customer_acct(self, req):
        if 'customer_id' not in req.reqParams or \
                req.reqParams['customer_id'] == "" or \
                'chk_acct_num' not in req.reqParams or \
                req.reqParams['chk_acct_num'] == "" or \
                'op_type' not in req.reqParams or \
                req.reqParams['op_type'] == "" or \
                'amt' not in req.reqParams or \
                req.reqParams['amt'] == "":
            self.send_error('UPDATE_RESPONSE','Multiple Invalid key-value entries')
            return ERROR
        
        amt = req.reqParams['amt']
        amt = int(amt)
        if req.reqParams['subreq_type'] == 'UPDATE_CHK_ACCT':
            acct, bal = self.get_customer_chk_acct(req.reqParams['customer_id'])
        else:
            acct, bal = self.get_customer_sav_acct(req.reqParams['customer_id'])
        bal = int(bal)
        if(req.reqParams['op_type'] == 'SUBTRACT'):
            bal = bal - amt
            if bal < 10:
                # send update failure
                self.send_error('UPDATE_RESPONSE', 'Minimum balance should be $10')
                return ERROR
        elif(req.reqParams['op_type'] == 'ADD'):
            bal = bal + amt
        else:
            self.send_error('UPDATE_RESPONSE', 'Unknown operation type sent')
            return ERROR
    
        if req.reqParams['subreq_type'] == 'UPDATE_CHK_ACCT':
            sql = "UPDATE ACCOUNT_TABLE SET CHECKING_ACCOUNT_BAL = '{x}' WHERE CHECKING_ACCOUNT_NUM ='{y}'".format(x=bal, y=acct)
        else:
            sql = "UPDATE ACCOUNT_TABLE SET SAVING_ACCOUNT_BAL = '{x}' WHERE SAVING_ACCOUNT_NUM ='{y}'".format(x=bal, y=acct)
        print "sql query ==> " + sql
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print e
            print "UPDATE request failure: server side error"
            self.db.rollback()
            self.send_error('UPDATE_RESPONSE', 'Server error: DB operation could not be completed')
            return ERROR
            
        resp = Response()
        resp.resType = 'UPDATE_RESPONSE'
        resp.resParams['status']='SUCCESS'
        self.sock.send(resp.toString())
        return SUCCESS

    def update_customer_profile(self,req):
        if 'customer_id' not in req.reqParams or \
                req.reqParams['customer_id'] == "":
                #'first_name' not in req.reqParams or \
                #'last_name' not in req.reqParams or \
                #'DOB' not in req.reqParams or \
                #'email' not in req.reqParams or \
                #'phone' not in req.reqParams or \
                #'address' not in req.reqParams:
            self.send_error('UPDATE_RESPONSE','Multiple Invalid key-value entries')
            return ERROR
        if 'first_name' in req.reqParams and req.reqParams['first_name'] != '':
            fname = 'FIRST_NAME'
            fname_val = req.reqParams['first_name']
        if 'last_name' in req.reqParams and req.reqParams['last_name'] != '':
            lname = 'LAST_NAME'
            lname_val = req.reqParams['last_name']
        if 'DOB' in req.reqParams and req.reqParams['DOB'] != '':
            dob = 'DATE_OF_BIRTH'
            dob_val = req.reqParams['DOB']
        if 'email' in req.reqParams and req.reqParams['email'] != '':
            emial = 'EMAIL_ID'
            emial_val = req.reqParams['email']
        if 'phone' in req.reqParams and req.reqParams['phone'] != '':
            phone = 'PHONE_NUMBER'
            phone_val = req.reqParams['phone']
        if 'address' in req.reqParams and req.reqParams[''] != '':
            address = 'ADDRESS'
            address_val = req.reqParams['address']
        sql = "UPDATE CUSTOMER_INFO_TABLE SET '{a}' = '{b}' WHERE SAVING_ACCOUNT_NUM ='{y}'".format(x=bal, y=acct)
        print "sql -> "+sql

        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print e
            print "UPDATE request failure: server side error"
            self.db.rollback()
            self.send_error('UPDATE_RESPONSE', 'Server error: DB operation could not be completed')
            return ERROR
            
        resp = Response()
        resp.resType = 'UPDATE_RESPONSE'
        resp.resParams['status']='SUCCESS'
        self.sock.send(resp.toString())
        return SUCCESS

    def run(self):
        print"waiting for login info from the client.."
        while True:
            #receive login request from the client
            data = self.sock.recv(1024)

            result = self.process_request(data)
            if(result == ERROR):
                print "Error. Client connection closed."
                break
            elif(result == LOGOUT):
                print "Client done. Connection closed."
                break
        print "Closing the client connection"
        self.sock.close()
        self.db.close()
        return

    
class Server(object):
    def __init__(self, host, port):
        # store input values for future reference
        self.host = host
        self.port = port
        self.clientThreads = []

        # create new server socket and bind to host:port
        self.ssock = socket.socket()
        self.ssock.bind((host, port))
        self.ssock.listen(5)

    def serve(self):
        while True:
            print "Server Listening for Clients.."

            # c,addr is a <connected_socket , client_address> tuple
            cliSock, cliAddr = self.ssock.accept()
            print "=======>>>>>> New Client request accepted from: [" + str(cliAddr) + "]"

            cli = Client(cliSock, cliAddr)
            cli.start()


def main():
    host = '127.0.0.1'
    port = 5500

    # Create DataBase object
    server = Server(host, port)
    server.serve()

if __name__=='__main__':
    main()

