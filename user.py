import socket

ERROR = 'FAILED'
SUCCESS = 'SUCCESS'
LOGOUT = 1

class Response(object):
    def __init__(self, buf):
        print "Response received ==> " + buf
        values = buf.split(',')
        self.resType = values[0]
        self.resParams = {}
        for elem in values[1:]:
            k, v = elem.split(':')
            self.resParams[k] = v

class Request:
    def __init__(self):
        self.reqType = ''
        self.reqParams = {}

    
    def toString(self):
        s = "{}".format(self.reqType)
        for k,v in self.reqParams.items():
            s = "{},{}:{}".format(s, k, v)
        print "Request Sent ==> " + s
        return s


class Customer(object):
    def __init__(self, cli_obj, cli_id):
        self.cli_obj = cli_obj
        self_cli_id = cli_id
        

    def display_customer_options(self):
        while True:
            print "1. Display Checking acct balance"
            print "2. Display Saving acct balance"
            print "3. Display User profile"
            print "4. Withdraw from Checking account"
            print "5. Winthdraw from Saving account"
            print "6. Deposit to Checking account"
            print "7. Deposit to Saving account"
            print "8. Transfer funds"
            print "9. Update User information"
            print "10. Log out"

            user_choice = raw_input("your choice ->")
            if (user_choice >= 1 and user_choice <= 10):
                break
            else:
                print ">>> Invalid input"

        print "returning user choice => " + str(user_choice)
        return user_choice


class Teller(object):
    def __init__(self, cli_obj, cli_id):
        self.cli_obj = cli_obj
        self.cli_type = 'Teller'
        self.cli_id = cli_id
    
        self.temp_cust_id = ''
        self.temp_cust_name = ''
        self.temp_cust_chk_acct = ''
        self.temp_cust_chk_bal = ''
        self.temp_cust_sav_acct = ''
        self.temp_cust_sav_bal = ''

    def display_teller_options(self):
        while True:
            print "1. Access Customer Account"
            print "2. Create Customer Account"
            print "3. Delete Customer Account"
            print "4. Logout"

            choice = raw_input("your choice ->")

            if(choice == '1'):
                # Access Customer account
                print "calling opt 1 => access_cust_acct()"
                self.access_customer_account()
            elif(choice =='2'):
                # Create Customer account
                print "calling opt 2 => access_cust_acct()"
                self.create_customer_account()
            elif(choice == '3'):
                # Delete Customer account
                print "calling opt 3 => access_cust_acct()"
                self.delete_customer_account()
            elif(choice == '4'):
                # Logout
                print "calling opt 4 => access_cust_acct()"
                return LOGOUT
            else:
                # Update Customer profile
                print "Invalid choice"

    def access_customer_account(self):
        while True:
            print "1. View User accounts"
            print "2. Update Checking account"
            print "3. Update Saving account"
            print "4. View User profile"
            print "5. Update User profile"
            print "6. Exit Menu"

            choice = raw_input("choice -> ")
            if (choice == '1'):
                self.view_customer_accounts()
            elif( choice == '2'):
                self.update_chk_acct()
            elif(choice == '3'):
                self.update_sav_acct()
            elif(choice == '4'):
                self.update_customer_profile()
            elif(choice == '5'):
                return

    def get_customer_id(self, customer_name):    
        # create request object
        req_obj = Request()
        req_obj.reqType = 'GET'
        req_obj.reqParams['client_type'] = self.cli_type
        req_obj.reqParams['subreq_type'] = 'CUSTOMER_ID'
        req_obj.reqParams['customer_name'] =  customer_name
    
        err = self.cli_obj.sock.sendall(req_obj.toString())
        if err != None:
            print" Send ERROR"
            
        print "Waiting for response.."
        data = self.cli_obj.sock.recv(1024)

        print "creating Response object"
        res_obj = Response(data)

        if(res_obj.resParams['status'] == 'SUCCESS'):
            return res_obj.resParams['client_id']
        else:
            print "GET :operation failed"


    def view_customer_accounts(self):
        customer_name = raw_input("Login Name: -> ")
        customer_id = 0
        customer_id = self.get_customer_id(customer_name)
        if customer_id:
            self.temp_cust_name = customer_name
            self.temp_cust_id = customer_id

            # create request object
            req_obj = Request()
            req_obj.reqType = 'GET'
            req_obj.reqParams['client_type'] = self.cli_type
            req_obj.reqParams['subreq_type'] = 'CUSTOMER_ACCT'
            req_obj.reqParams['customer_id'] = customer_id

            print"sending GET Acct request.."
            err = self.cli_obj.sock.sendall(req_obj.toString())
            if err != None:
                print" Send ERROR"
            
            print "Waiting for response.."
            data = self.cli_obj.sock.recv(1024)

            print "creating Response object"
            res_obj = Response(data)

            if(res_obj.resParams['status'] == 'SUCCESS'):
                self.temp_cust_chk_acct = res_obj.resParams['chk_acct']
                self.temp_cust_chk_bal = res_obj.resParams['chk_bal']
                self.temp_cust_sav_acct = res_obj.resParams['sav_acct']
                self.temp_cust_sav_bal = res_obj.resParams['sav_bal']

                print"------------------------------------------------"
                print "| Name: "+customer_name+"     "+"Customer ID: "+customer_id+"\n"
                print "|Checking Account               Balance     "
                print "|"+res_obj.resParams['chk_acct']+ "                      $" + res_obj.resParams['chk_bal']+"\n"
                print "|Saving Account                 Balance "
                print "|"+res_obj.resParams['sav_acct']+"                      $"+ res_obj.resParams['sav_bal']
                print"------------------------------------------------"
                
            else:
                print "GET :operation failed"
                
        else:
            print "Invalid Customer ID"


    def update_chk_acct(self):
        while True:
            print"1. Withdrawal"
            print"2. Deposit"
            print"3. Exit"
            choice = raw_input("Select your option: -> ")
            if choice >= '1' or choice <= '3':
                break
            else:
                print"Invalid Input. Enter again"
        
        if choice == '3':
            return
        if(choice =='1' or choice == '2'):
            while True:
                balance = raw_input("Amount -> ")
                if balance != '':
                    break
                else:
                    print "Amount Invalid"
    
        # create request object
        req_obj = Request()
        req_obj.reqType = 'UPDATE'
        req_obj.reqParams['client_type'] = self.cli_type
        req_obj.reqParams['subreq_type'] = 'UPDATE_CHK_ACCT'
        req_obj.reqParams['customer_id'] = self.temp_cust_id
        req_obj.reqParams['chk_acct_num'] = self.temp_cust_chk_acct
        if (choice == '1'):
            req_obj.reqParams['op_type'] = 'SUBTRACT'
            req_obj.reqParams['amt'] = balance
        elif (choice == '2'):
            req_obj.reqParams['op_type'] = 'ADD'
            req_obj.reqParams['amt'] = balance

        print"sending UPDATE Acct request.."
        err = self.cli_obj.sock.sendall(req_obj.toString())
        if err != None:
            print" Send ERROR"
            
        print "Waiting for response.."
        data = self.cli_obj.sock.recv(1024)

        print "creating Response object"
        res_obj = Response(data)

        if(res_obj.resParams['status'] == 'SUCCESS'):
            print "Customer account updated successfully. New balance =>"
            self.view_customer_accounts()
        else:
            print "Update failure: Customer account could not be updated at this time"


    def create_customer_account(self):
        pass

    def delete_customer_account(self):
        pass

    def logout(self):
        pass

class Admin(object):
    def __init__(self, cli_obj, cli_id):
        self.cli_obj = cli_obj
        self.cli_id = cli_id

class ClientConnection(object):
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 5500
        self.sock = 0
        self.usr = ''
        self.pwd = ''

        #start a TCP connection
        err = self.connect_server()
        if err != None:
            raise Exception("Failed to connect to server")

    # start a secure TCP connection with the server
    def connect_server(self):
        self.sock = socket.socket()
        err = self.sock.connect((self.host, self.port))
        return err

    # login into the system
    def login(self):
        
        req_obj = Request()

        self.usr = raw_input("Login Name: -> ")
        self.pwd = raw_input("Password: -> ")

        # create request object
        req_obj.reqType = 'LOGIN'
        req_obj.reqParams['username'] = self.usr
        req_obj.reqParams['password'] = self.pwd

        print"sending Login request.."
        err = self.sock.sendall(req_obj.toString())
        if err != None:
            return [ERROR,'','']
            
        print "Waiting for response.."
        data = self.sock.recv(1024)

        print "creating Response object"
        res_obj = Response(data)

        if(res_obj.resParams['status'] == 'SUCCESS'):
            print "login():client type : "+ res_obj.resParams['client_type']
            res_list = [res_obj.resParams['status'],res_obj.resParams['client_type'],res_obj.resParams['client_id']]
            return res_list
        else:
            print "login(): returning ERROR"
            return [ERROR,'','']
        
    def closeconnection(self):
        self.sock.close()

    
# Main Function
def main():
    try:
        # create TCP connection with the server
        cc1 = ClientConnection()
    except Exception, e:
        print e
        return

    print "Client connection successful"
    # send login credentials
    res_list = cc1.login()
    if (res_list[0] == ERROR):
        print "Authentication Failure"
    else:
        if (res_list[1] == 'Customer'):
            #create customer object
            cst_user = Customer(cc1, res_list[2])
            cst_user.display_customer_options()

        elif (res_list[1] == 'Teller'):
            #create teller object
            tel_user = Teller(cc1, res_list[2])
            while True:
                choice = tel_user.display_teller_options()
                if(choice == LOGOUT):
                    break

        elif (client_type == 'Admin'):
            #create admin user
            admin_user = admin(cc1, res_list[2])
            
        else:
            #user authentication failed
            print "Unknown Client_type.Closing the connection"
    
    cc1.closeconnection()


if __name__ == "__main__":
    main()