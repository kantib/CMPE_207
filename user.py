import socket
from random import randint

ERROR = 'FAILED'
SUCCESS = 'SUCCESS'
LOGOUT = 1

class Response(object):
    def __init__(self, buf):
        print "Response received ==> " + buf
        values = buf.split('::')
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
            s = "{}::{}:{}".format(s, k, v)
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
                print "calling opt 1 => Access_cust_acct"
                self.access_customer_account()
            elif(choice == '2'):
                # Create Customer account
                print "calling opt 2 => Create_cust_acct"
                self.create_customer_account()
            elif(choice == '3'):
                # Delete Customer account
                print "calling opt 3 => Delete_cust_acct"
                self.delete_customer_account()
            elif(choice == '4'):
                # Logout
                return LOGOUT
            else:
                # Update Customer profile
                print "Invalid choice"


    def delete_customer_account(self):
        customer_id = raw_input("Enter customer id: ")

        req_obj = Request()
        req_obj.reqType = 'DELETE'
        req_obj.reqParams['client_type'] = self.cli_type
        req_obj.reqParams['subreq_type'] = 'DELETE_LOGIN_RECORD'
        req_obj.reqParams['customer_id'] = customer_id

        err = self.cli_obj.sock.sendall(req_obj.toString())
        if err != None:
            print" Send ERROR"
            
        print "Waiting for response.."
        data = self.cli_obj.sock.recv(1024)

        print "creating Response object"
        res_obj = Response(data)

        if(res_obj.resParams['status'] == 'SUCCESS'):
            print "Customer login Deleted"

            req_obj.reqType = 'DELETE'
            req_obj.reqParams['client_type'] = self.cli_type
            req_obj.reqParams['subreq_type'] = 'DELETE_ACCT_RECORD'
            req_obj.reqParams['customer_id'] = customer_id

            err = self.cli_obj.sock.sendall(req_obj.toString())
            if err != None:
                print" Send ERROR"

            print "Waiting for response.."
            data = self.cli_obj.sock.recv(1024)

            print "creating Response object"
            res_obj = Response(data)

            if(res_obj.resParams['status'] == 'SUCCESS'):
                print "Customer Account Deleted"

                req_obj.reqType = 'DELETE'
                req_obj.reqParams['client_type'] = self.cli_type
                req_obj.reqParams['subreq_type'] = 'DELETE_PROFILE_RECORD'
                req_obj.reqParams['customer_id'] = customer_id

                err = self.cli_obj.sock.sendall(req_obj.toString())
                if err != None:
                    print" Send ERROR"

                print "Waiting for response.."
                data = self.cli_obj.sock.recv(1024)

                print "creating Response object"
                res_obj = Response(data)

                if(res_obj.resParams['status'] == 'SUCCESS'):
                    print "Customer Profile Deleted"

                else:
                    print "Create Failed - Error: "+ res_obj+resParams['err']
                    # Send Delete request to delete the corresponding entries
                    # in customer_login and ACCOUNT_TABLE table
            else:
                print"Create Failed - Error: "+res_obj.resParams['err']
                # Delete Corresponding entry in the Customer login here
        else:
            print "Create Failed - Error: " + res_obj.resParams['err']


    def create_customer_account(self):
        print "Inside create_customer_account"
        user_name = raw_input("User Name: ")
        password = raw_input("Password: ")
        customer_id = randint(1000000000, 2147483648)
        print "Generated Customer id = " + str(customer_id)
        client_type = 'Customer'

        req_obj = Request()
        req_obj.reqType = 'INSERT'
        req_obj.reqParams['client_type'] = self.cli_type
        req_obj.reqParams['subreq_type'] = 'INSERT_LOGIN_RECORD'
        req_obj.reqParams['user_name'] =  user_name
        req_obj.reqParams['password'] = password
        req_obj.reqParams['customer_id'] = customer_id
        req_obj.reqParams['record_client_type'] = client_type

        err = self.cli_obj.sock.sendall(req_obj.toString())
        if err != None:
            print" Send ERROR"
            
        print "Waiting for response.."
        data = self.cli_obj.sock.recv(1024)

        print "creating Response object"
        res_obj = Response(data)

        if(res_obj.resParams['status'] == 'SUCCESS'):
            print "Customer login Created"
            chk_acct_num = randint(100000000, 2147483648)
            sav_acct_num = randint(100000000, 2147483648)

            req_obj.reqType = 'INSERT'
            req_obj.reqParams['client_type'] = self.cli_type
            req_obj.reqParams['subreq_type'] = 'INSERT_ACCT_RECORD'
            req_obj.reqParams['customer_chk_acct'] = chk_acct_num
            req_obj.reqParams['customer_sav_acct'] = sav_acct_num
            req_obj.reqParams['customer_id'] = customer_id
            req_obj.reqParams['customer_chk_bal'] = 0
            req_obj.reqParams['customer_sav_bal'] = 0

            err = self.cli_obj.sock.sendall(req_obj.toString())
            if err != None:
                print" Send ERROR"

            print "Waiting for response.."
            data = self.cli_obj.sock.recv(1024)

            print "creating Response object"
            res_obj = Response(data)

            if(res_obj.resParams['status'] == 'SUCCESS'):
                print "Customer Accounts Created"

                first_name = raw_input("First Name: ")
                last_name = raw_input("Last_name: ")
                dob = raw_input("Date Of Birth: ")
                email = raw_input("Email: ")
                phone_num = raw_input("Phone number: ")
                address = raw_input("Address: ")

                req_obj.reqType = 'INSERT'
                req_obj.reqParams['client_type'] = self.cli_type
                req_obj.reqParams['subreq_type'] = 'INSERT_PROFILE_RECORD'
                req_obj.reqParams['first_name'] =  first_name
                req_obj.reqParams['last_name'] = last_name
                req_obj.reqParams['DOB'] = dob
                req_obj.reqParams['email'] = email
                req_obj.reqParams['phone'] = phone_num
                req_obj.reqParams['address'] = address

                err = self.cli_obj.sock.sendall(req_obj.toString())
                if err != None:
                    print" Send ERROR"

                print "Waiting for response.."
                data = self.cli_obj.sock.recv(1024)

                print "creating Response object"
                res_obj = Response(data)

                if(res_obj.resParams['status'] == 'SUCCESS'):
                    print "Customer Profile Created"

                else:
                    print "Create Failed - Error: "+ res_obj+resParams['err']
                    # Send Delete request to delete the corresponding entries
                    # in customer_login and ACCOUNT_TABLE table
            else:
                print"Create Failed - Error: "+res_obj.resParams['err']
                # Delete Corresponding entry in the Customer login here
        else:
            print "Create Failed - Error: " + res_obj.resParams['err']

    def access_customer_account(self):
        while True:
            print "1. View / Manage User accounts"
            print "2. View / Manage User profile"
            print "3. Exit Menu"

            choice = raw_input("choice -> ")
            if (choice == '1'):
                self.view_customer_accounts(True)
            elif(choice == '2'):
                self.view_customer_profile(True)
            elif(choice == '3'):
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

    def view_customer_profile(self,_flag):
        if _flag:

            customer_name = raw_input("Login Name: -> ")
            customer_id = 0
            customer_id = self.get_customer_id(customer_name)
            self.temp_cust_id = customer_id
            self.temp_cust_name = customer_name
        else:
            customer_id = self.temp_cust_id

        # create request object
        req_obj = Request()
        req_obj.reqType = 'GET'
        req_obj.reqParams['client_type'] = self.cli_type
        req_obj.reqParams['subreq_type'] = 'CUSTOMER_PROFILE'
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
            print"Customer ID: "+res_obj.resParams['customer_id']
            print"First Name: "+res_obj.resParams['first_name']
            print"Last Name: "+res_obj.resParams['last_name']     
            print"Date of Birth: "+res_obj.resParams['DOB']
            print"Email: "+res_obj.resParams['email']
            print"Phone: "+res_obj.resParams['phone']
            print"Address: "+res_obj.resParams['address']
            print"\n"

            while True:
                print"1. Update User profile"
                print"2. Exit"
                choice = raw_input('Enter Choice: ->')
                if choice >= '1' and choice <= '2':
                    break
            if choice == 2:
                return
            else:
                self.update_customer_profile()

    def update_customer_profile(self):

        first_name = last_name = dob = email_id = phone_num = address = ''
        print"Press Y if you wish to change ==>"
        choice = raw_input("First name? ")
        if choice == 'Y'or choice =='y':
            first_name = raw_input("Enter New First name: ")
        choice = raw_input("Last name? ")
        if choice == 'Y' or choice == 'y':
            last_name = raw_input("Enter New Last name: ")
        choice = raw_input("Date of Birth? ")
        if choice == 'Y' or choice == 'y':
            dob = raw_input("Enter New DOB: ")
        choice = raw_input("Email ID? ")
        if choice == 'Y' or choice == 'y':
            email_id = raw_input("Enter New Email ID: ")
        choice = raw_input("Phone number? ")
        if choice == 'Y' or choice == 'y':
            phone_num = raw_input("Enter New Phone number: ")
        choice = raw_input("Address? ")
        if choice == 'Y' or choice == 'y':
            address = raw_input("Enter New Address: ")
                        
        # create request object
        req_obj = Request()
        req_obj.reqType = 'SET'
        req_obj.reqParams['client_type'] = self.cli_type
        req_obj.reqParams['customer_id'] = self.temp_cust_id
        req_obj.reqParams['subreq_type'] = 'UPDATE_CUSTOMER_PROFILE'
        if first_name != '':
            req_obj.reqParams['first_name']=first_name
        if last_name != '':
            req_obj.reqParams['last_name']=last_name
        if dob != '':
            req_obj.reqParams['DOB']=dob
        if email_id != '':
            req_obj.reqParams['email_id']=email_id
        if phone_num != '':
            req_obj.reqParams['phone']=phone_num
        if address != '':
            req_obj.reqParams['address']=Address

        print"sending UPDATE profile request.."
        print"==> "+req_obj.toString()
        err = self.cli_obj.sock.sendall(req_obj.toString())
        if err != None:
            print" Send ERROR"
            
        print "Waiting for response.."
        data = self.cli_obj.sock.recv(1024)

        print "creating Response object"
        res_obj = Response(data)

        if(res_obj.resParams['status'] == 'SUCCESS'):
            print "Customer account updated successfully."
            self.view_customer_profile(False)
        else:
            print "Update failure: Customer account could not be updated at this time"


    def view_customer_accounts(self,_flag):
        if _flag:
            customer_name = raw_input("Login Name: -> ")
            customer_id = 0
            customer_id = self.get_customer_id(customer_name)
        else:
            customer_id = self.temp_cust_id
            customer_name = self.temp_cust_name
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
                print "Name: "+customer_name+"     "+"Customer ID: "+customer_id+"\n"
                print "Checking Account               Balance     "
                print res_obj.resParams['chk_acct']+ "                      $" + res_obj.resParams['chk_bal']+"\n"
                print "Saving Account                 Balance "
                print res_obj.resParams['sav_acct']+"                      $"+ res_obj.resParams['sav_bal']
                print"------------------------------------------------\n"
                print" 1. Update User Checking Account"
                print" 2. Update User Saving Account"
                print" 3. Exit"

                while True:
                    choice = raw_input("Enter Choice: ->")
                    if choice >= '1' and choice <= '3':
                        break

                if choice == '1':
                    self.update_acct('checking')
                elif choice == '2':
                    self.update_acct('saving')
                else:
                    return
            else:
                print "GET :operation failed"
                
        else:
            print "Invalid Customer ID"


    def update_acct(self,acct_type):
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
        req_obj.reqType = 'SET'
        req_obj.reqParams['client_type'] = self.cli_type
        req_obj.reqParams['customer_id'] = self.temp_cust_id
        if acct_type == 'checking':
            req_obj.reqParams['subreq_type'] = 'UPDATE_CHK_ACCT'
            req_obj.reqParams['chk_acct_num'] = self.temp_cust_chk_acct
        else:
            req_obj.reqParams['subreq_type'] = 'UPDATE_SAV_ACCT'
            req_obj.reqParams['chk_acct_num'] = self.temp_cust_sav_acct

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
            self.view_customer_accounts(False)
        else:
            print "Update failure: Customer account could not be updated at this time"


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
