import socket
import ssl
from random import randint

ERROR = 'FAILED'
SUCCESS = 'SUCCESS'
LOGOUT = 1

class Response(object):
    def __init__(self, buf):
        #print"Response object created"
        print "Response received ==> " + buf
        print "\n"
        values = buf.split('::')
        #print values
        self.resType = values[0]
        self.resParams = {}
        for elem in values[1:]:
            k, v = elem.split(':')
            #print"k = "+k+":"+"v = "+v
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
        #print "\n"
        return s

######################### CUSTOMER CLASS  #########################

class Customer(object):
    def __init__(self, cli_obj,_name,_pwd,cli_id):
        self.cli_obj = cli_obj
        self.cli_type = 'Customer'
        self.cli_id = cli_id
        self.cli_name = _name
        self.cli_pwd = _pwd

        tmp_user_chk_act = ''
        tmp_user_sav_act = ''
        tmp_user_chk_bal = ''
        tmp_user_sav_bal = ''
    
    def display_customer_options(self):
        while True:
            print "1. Display checking AND saving acct balance"
            print "2. Display profile"
            print "3. Change Profile"
            print "4. Transfer funds"
            print "5. Monthly Transactions"
            print "6. Withdraw"
            print "7. Deposit"
            print "8. Log out"

            choice = raw_input("your choice ->")

            if(choice == '1'):
                # view account balance
                self.view_user_accounts(1)
            elif(choice == '2'):
                # view personal information
                self.view_user_profile()
            elif(choice == '3'):
                # Update personal information
                self.update_user_profile()
            elif(choice == '4'):
                # transfer money
                self.transfer_money()
            elif(choice == '5'):
                self.view_monthly_statements()
            elif(choice == '6'):
                print "\n==> Please approach the Teller for withdrawal\n"
            elif(choice == '7'):
                print "\n==> Please approach the Teller for Deposital\n"
            elif(choice == '8'):
                # Logout
                return LOGOUT
            else:
                # Update Customer profile
                print "Invalid choice"

    def view_monthly_statements(self):
        print"\nFunction: view_monthly_statements() ==>"
        print"YET TO BE IMPLEMENTED..."

    def view_user_accounts(self, display_flag):
        #print "view_customer_accounts - display_flag = "+ str(display_flag)
        print"\nFunction: view_user_accounts() ==>"
        # create request object
        req_obj = Request()
        req_obj.reqType = 'GET'
        req_obj.reqParams['client_type'] = self.cli_type
        req_obj.reqParams['subreq_type'] = 'CUSTOMER_ACCT'
        req_obj.reqParams['customer_id'] = self.cli_id

        #print"sending GET Acct request.."
        err = self.cli_obj.sock.sendall(req_obj.toString())
        #if err != None:
        #    print" Send ERROR"
        
        #print "Waiting for response.."
        data = self.cli_obj.sock.recv(1024)

        #print "creating Response object"
        res_obj = Response(data)

        if(res_obj.resParams['status'] == 'SUCCESS'):
            self.tmp_user_chk_act = res_obj.resParams['chk_acct']
            self.tmp_user_chk_bal = res_obj.resParams['chk_bal']
            self.tmp_user_sav_act = res_obj.resParams['sav_acct']
            self.tmp_user_sav_bal = res_obj.resParams['sav_bal']
            if(display_flag == 1):
                #print "display flag 1 block"
                print"------------------------------------------------"
                print "Name: "+self.cli_name+"     "+"Customer ID: "+self.cli_id+"\n"
                print "Checking Account               Balance     "
                print res_obj.resParams['chk_acct']+ "                      $" + res_obj.resParams['chk_bal']+"\n"
                print "Saving Account                 Balance "
                print res_obj.resParams['sav_acct']+"                      $"+ res_obj.resParams['sav_bal']
                print"------------------------------------------------\n"
            elif(display_flag == 2):
                #print "display flag 2 block"
                print"------------------------------------------------"
                print "Name: "+self.cli_name+"     "+"Customer ID: "+self.cli_id+"\n"
                print "Checking Account               Balance     "
                print res_obj.resParams['chk_acct']+ "                      $" + res_obj.resParams['chk_bal']+"\n"
                print"------------------------------------------------\n"
            else:
                #print "Last else block"
                print"------------------------------------------------"
                print "Name: "+self.cli_name+"     "+"Customer ID: "+self.cli_id+"\n"
                print "Saving Account               Balance     "
                print res_obj.resParams['sav_acct']+ "                      $" + res_obj.resParams['sav_bal']+"\n"
                print"------------------------------------------------\n"
        else:
            print "GET :operation failed"


    def view_user_profile(self):
        print"\nFunction view_user_profile() ==>"
        # create request object
        req_obj = Request()
        req_obj.reqType = 'GET'
        req_obj.reqParams['client_type'] = self.cli_type
        req_obj.reqParams['subreq_type'] = 'CUSTOMER_PROFILE'
        req_obj.reqParams['customer_id'] = self.cli_id

        #print"sending GET Acct request.."
        err = self.cli_obj.sock.sendall(req_obj.toString())
        #if err != None:
        #    print" Send ERROR"
            
        data = self.cli_obj.sock.recv(1024)
        res_obj = Response(data)
        if(res_obj.resParams['status'] == 'SUCCESS'):
            print"\n---------------------------------------------"
            print"Customer ID  : "+res_obj.resParams['customer_id']
            print"First Name   : "+res_obj.resParams['first_name']
            print"Last Name    : "+res_obj.resParams['last_name']     
            print"Date of Birth: "+res_obj.resParams['DOB']
            print"Email Address: "+res_obj.resParams['email']
            print"Phone Number : "+res_obj.resParams['phone']
            print"Address      : "+res_obj.resParams['address']
            print"---------------------------------------------\n"

    def update_user_profile(self):
        first_name = last_name = dob = email_id = phone_num = address = ''
        state = apt_num = street_name = city = country = zipcode = gender = ''
        print"\n Function: update_user_profile ==>"
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
        choice = raw_input("APT number? ")
        if choice == 'Y' or choice == 'y':
            apt_num = raw_input("Enter New APT number: ")
        choice = raw_input("Street Name? ")
        if choice == 'Y' or choice == 'y':
            street_name = raw_input("Enter New Street name: ")
        choice = raw_input("City? ")
        if choice == 'Y' or choice == 'y':
            city = raw_input("Enter New City: ")
        choice = raw_input("State? ")
        if choice == 'Y' or choice == 'y':
            state = raw_input("Enter New State: ")
        choice = raw_input("Country? ")
        if choice == 'Y' or choice == 'y':
            country = raw_input("Enter New Country: ")
        choice = raw_input("Zipcode? ")
        if choice == 'Y' or choice == 'y':
            zipcode = raw_input("Enter New Zipcode: ")
        choice = raw_input("Gender? ")
        if choice == 'Y' or choice == 'y':
            gender = raw_input("Enter New Gender: ")

        if (first_name == '' and last_name == '' and dob == '' \
                and email_id == '' and phone_num == '' and address == '' \
                and apt_num == '' and street_name == '' and city == '' \
                and state == '' and country == '' and zipcode == '' and gender == ''):
            print"\n-----------------------"
            print" => No changes opted."
            print"-------------------------\n"

        # create request object
        req_obj = Request()
        req_obj.reqType = 'SET'
        req_obj.reqParams['client_type'] = self.cli_type
        req_obj.reqParams['customer_id'] = self.cli_id
        req_obj.reqParams['subreq_type'] = 'UPDATE_CUSTOMER_PROFILE'
        if first_name != '':
            req_obj.reqParams['first_name']=first_name
        if last_name != '':
            req_obj.reqParams['last_name']=last_name
        if dob != '':
            req_obj.reqParams['DOB']=dob
        if email_id != '':
            req_obj.reqParams['email']=email_id
        if phone_num != '':
            req_obj.reqParams['phone']=phone_num
        if apt_num != '':
            req_obj.reqParams['apt_num']=apt_num
        if street_name != '':
            req_obj.reqParams['street_name']=street_name
        if city != '':
            req_obj.reqParams['city'] = city
        if state != '':
            req_obj.reqParams['state'] = state
        if country != '':
            req_obj.reqParams['country'] = country
        if zipcode != '':
            req_obj.reqParams['zipcode'] = zipcode
        if gender != '':
            req_obj.reqParams['gender'] = gender
        
        #print"sending UPDATE profile request.."
        #print"==> "+req_obj.toString()
        err = self.cli_obj.sock.sendall(req_obj.toString())
        #if err != None:
        #    print" Send ERROR"
            
        #print "Waiting for response.."
        data = self.cli_obj.sock.recv(1024)

        #print "creating Response object"
        res_obj = Response(data)

        if(res_obj.resParams['status'] == 'SUCCESS'):
            print "Customer account updated successfully."
            self.view_user_profile()
        else:
            print "Update failure: Customer account could not be updated at this time"


    def transfer_money(self):
        print"\nFunction: transfer_money() ==>"
        print"select account type for transfer:"
        while True:
            print "1. Checking"
            print "2. Saving"
            choice = raw_input("choice -> ")
            if (choice == '1'):
                #print "tmp_user_chk_act = " + self.tmp_user_chk_act
                from_acct = self.tmp_user_chk_act
                #print"Dispaly flag set to 2"
                display_flag = 2
                break
            elif (choice == '2'):
                from_acct = self.tmp_user_sav_act
                #print"Display flag set to 3"
                display_flag = 3
                break
            else:
                print"Invalid choice"

        to_bank = raw_input("Bank Name: ")
        to_acct = raw_input("Bank Account number: ")
        amount = raw_input("Amount: ")

        req_obj = Request()
        req_obj.reqType = 'SET'
        req_obj.reqParams['client_type'] = self.cli_type
        req_obj.reqParams['customer_id'] = self.cli_id
        req_obj.reqParams['subreq_type'] = 'TRANSFER_MONEY'
        if (display_flag == 2):
            req_obj.reqParams['acct_type'] = 'checking'
        elif(display_flag ==3):
            req_obj.reqParams['acct_type'] = 'saving'

        req_obj.reqParams['chk_acct_num'] = from_acct
        req_obj.reqParams['op_type'] = 'SUBTRACT'
        req_obj.reqParams['to_bank'] = to_bank
        req_obj.reqParams['to_acct'] = to_acct
        req_obj.reqParams['amt'] = amount

        err = self.cli_obj.sock.sendall(req_obj.toString())
        #if err != None:
        #    print" Send ERROR"
            
        #print "Waiting for response.."
        data = self.cli_obj.sock.recv(1024)

        #print "creating Response object"
        res_obj = Response(data)

        if(res_obj.resParams['status'] == 'SUCCESS'):
            print "TRANSFER SUCCESSFUL."
            self.view_user_accounts(display_flag)
        else:
            print "\nTRANSFER FAILED: Error:"+res_obj.resParams['error']


    #def view_monthly_statements(self):
        # create request object
     #   req_obj = Request()
     #   req_obj.reqType = 'GET'
     #   req_obj.reqParams['client_type'] = self.cli_type
     #   req_obj.reqParams['subreq_type'] = 'MONTHLY_STATEMENT'
     #   req_obj.reqParams['customer_id'] = self.cli_id

        #print"sending GET Acct request.."
     #   err = self.cli_obj.sock.sendall(req_obj.toString())
        #if err != None:
        #    print" Send ERROR"
            
     #   data = self.cli_obj.sock.recv(1024)
     #   res_obj = Response(data)
        #if(res_obj.resParams['status'] == 'SUCCESS'):

######################### TELLER CLASS  #########################

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
                self.access_customer_account()
            elif(choice == '2'):
                # Create Customer account
                self.create_customer_login_record()
                #self.create_customer_account_record()
                #self.create_customer_profile_record()
            elif(choice == '3'):
                # Delete Customer account
                self.delete_customer_account()
            elif(choice == '4'):
                # Logout
                return LOGOUT
            else:
                # Update Customer profile
                print "Invalid choice"


    def access_customer_account(self):
        print"Function: access_customer_account() ==>"
        customer_name = raw_input("Login Name: -> ")
        customer_id = 0
        customer_id = self.get_customer_id(customer_name)
        if customer_id:
            self.temp_cust_name = customer_name
            self.temp_cust_id = customer_id
        else:
            print"\nCUSTOMER RECORD NOT FOUND\n"
            return
        while True:
            print "1. Manage customer accounts"
            print "2. Manage customer profile"
            print "3. Exit Menu"

            choice = raw_input("choice -> ")
            if (choice == '1'):
                self.manage_customer_accounts()
            elif(choice == '2'):
                self.manage_customer_profile()
            elif(choice == '3'):
                return

    def manage_customer_accounts(self):
        print"Function:manage_customer_accounts() ==>"
        while True:
            print "1. View customer account"
            print "2. View customer Transactions"
            print "3. Update customer Checking account"
            print "4. Update customer Saving account"
            print "5. Exit"

            choice = raw_input("choice -> ")
            if (choice == '1'):
                self.view_customer_accounts('1')
            elif(choice == '2'):
                self.view_customer_transactions()
            elif(choice == '3'):
                self.update_acct('checking')
            elif(choice == '4'):
                self.update_acct('saving')
            elif(choice == '5'):
                return
            else:
                print "Invalid choice. Enter again"


    def manage_customer_profile(self):
        print"Function:manage_customer_profile() ==>"
        while True:
            print "1. View customer profile"
            print "2. Update customer profile"
            print "3. Exit"

            choice = raw_input("choice -> ")
            if (choice == '1'):
                self.view_customer_profile()
            elif(choice == '2'):
                self.update_customer_profile()
            elif(choice == '3'):
                return
            else:
                print "Invalid choice. Enter again"


    def get_customer_id(self, customer_name):    
        print"Function:get_customer_id() ==>"
        # create request object
        req_obj = Request()
        req_obj.reqType = 'GET'
        req_obj.reqParams['client_type'] = self.cli_type
        req_obj.reqParams['subreq_type'] = 'CUSTOMER_ID'
        req_obj.reqParams['customer_name'] =  customer_name
    
        err = self.cli_obj.sock.sendall(req_obj.toString())
        #if err != None:
        #    print" Send ERROR"
            
        #print "Waiting for response.."
        data = self.cli_obj.sock.recv(1024)

        #print "creating Response object"
        res_obj = Response(data)

        if(res_obj.resParams['status'] == 'SUCCESS'):
            return res_obj.resParams['client_id']
        else:
            print "GET :operation failed"


    def view_customer_accounts(self, display_flag):
        print"Function:view_customer_accounts() ==>"
        # create request object
        req_obj = Request()
        req_obj.reqType = 'GET'
        req_obj.reqParams['client_type'] = self.cli_type
        req_obj.reqParams['subreq_type'] = 'CUSTOMER_ACCT'
        req_obj.reqParams['customer_id'] = self.temp_cust_id

        #print"sending GET Acct request.."
        err = self.cli_obj.sock.sendall(req_obj.toString())
        #if err != None:
        #    print" Send ERROR"
        
        #print "Waiting for response.."
        data = self.cli_obj.sock.recv(1024)

        #print "creating Response object"
        res_obj = Response(data)

        if(res_obj.resParams['status'] == 'SUCCESS'):
            self.temp_cust_chk_acct = res_obj.resParams['chk_acct']
            self.temp_cust_chk_bal = res_obj.resParams['chk_bal']
            self.temp_cust_sav_acct = res_obj.resParams['sav_acct']
            self.temp_cust_sav_bal = res_obj.resParams['sav_bal']
            if(display_flag == '1'):
                print"------------------------------------------------"
                print "Name: "+self.temp_cust_name+"     "+"Customer ID: "+self.temp_cust_id+"\n"
                print "Checking Account               Balance     "
                print res_obj.resParams['chk_acct']+ "                      $" + res_obj.resParams['chk_bal']+"\n"
                print "Saving Account                 Balance "
                print res_obj.resParams['sav_acct']+"                      $"+ res_obj.resParams['sav_bal']
                print"------------------------------------------------\n"
            elif(display_flag == '2'):
                print"------------------------------------------------"
                print "Name: "+self.temp_cust_name+"     "+"Customer ID: "+self.temp_cust_id+"\n"
                print "Checking Account               Balance     "
                print res_obj.resParams['chk_acct']+ "                      $" + res_obj.resParams['chk_bal']+"\n"
                print"------------------------------------------------\n"
            else:
                print"------------------------------------------------"
                print "Name: "+self.temp_cust_name+"     "+"Customer ID: "+self.temp_cust_id+"\n"
                print "Saving Account               Balance     "
                print res_obj.resParams['sav_acct']+ "                      $" + res_obj.resParams['sav_bal']+"\n"
                print"------------------------------------------------\n"
        else:
            print "GET :operation failed"


    def view_customer_profile(self):
        print"Function:view_customer_profile()==>"
        # create request object
        req_obj = Request()
        req_obj.reqType = 'GET'
        req_obj.reqParams['client_type'] = self.cli_type
        req_obj.reqParams['subreq_type'] = 'CUSTOMER_PROFILE'
        req_obj.reqParams['customer_id'] = self.temp_cust_id

        #print"sending GET Acct request.."
        err = self.cli_obj.sock.sendall(req_obj.toString())
        #if err != None:
        #    print" Send ERROR"
            
        data = self.cli_obj.sock.recv(1024)
        res_obj = Response(data)
        if(res_obj.resParams['status'] == 'SUCCESS'):
            print"\n---------------------------------------------"
            print"Customer ID  : "+res_obj.resParams['customer_id']
            print"First Name   : "+res_obj.resParams['first_name']
            print"Last Name    : "+res_obj.resParams['last_name']     
            print"Date of Birth: "+res_obj.resParams['DOB']
            print"Email Address: "+res_obj.resParams['email']
            print"Phone Number : "+res_obj.resParams['phone']
            print"Address      : "+res_obj.resParams['address']
            print"---------------------------------------------\n"



    def view_customer_transactions(self):#, customer_id):
        print"Function:view_customer_transactions() ==>"
        # create request object
        req_obj = Request()
        req_obj.reqType = 'GET'
        req_obj.reqParams['client_type'] = self.cli_type
        req_obj.reqParams['subreq_type'] = 'CUSTOMER_TRANSACTION'
        req_obj.reqParams['customer_id'] = self.temp_cust_id

        #print"sending GET Acct request.."
        err = self.cli_obj.sock.sendall(req_obj.toString())
        #if err != None:
        #    print" Send ERROR"
            
        data = self.cli_obj.sock.recv(1024)
        res_obj = Response(data)
        if(res_obj.resParams['status'] == 'SUCCESS'):
            if(res_obj.resParams['trns_list'] == ''):
                print"==> NO TRANSACTIONS FOUND FOR GIVEN MONTH\n"
            else:
                self.print_transactions(res_obj.resParams['trns_list'])
        else:
            print"Server error. Failed to get transactions at this time"



    def print_transactions(self, trns_str):
        print "\nFunction: print_transactions() ==> "
        trns_list = trns_str.split()
        #print trns_list
        #print"\n"
        print"%-3s %-14s %-12s %-10s %-8s %-18s %-12s %-13s %-15s" % ('NUM','CUSTOMER ID', \
                'DATE','TIME','ACCOUNT','TRANSACTION TYPE','AMOUNT','FROM ACCOUNT', 'TO_ACCOUNT')
        print"---------------------------------------------------------------------------------------------------------------"
        for i in range(0,len(trns_list),8):
            for j in range(0,8):
                #print trns_list[i+j]
                key, t_id = trns_list[i+0].split('-')
                key, t_date = trns_list[i+1].split('-')
                key, t_time = trns_list[i+2].split('-')
                key, t_acct = trns_list[i+3].split('-')
                key, t_trtype = trns_list[i+4].split('-')
                key, t_amt = trns_list[i+5].split('-')
                key, t_facct = trns_list[i+6].split('-')
                if t_facct is None:
                    t_facct = ' '
                key, t_tacct = trns_list[i+7].split('-')
                if t_facct is None:
                    t_facct = ' '
            print "%-3s %-14s %-12s %-10s %-11s %-16s %-12s %-13s %-15s" % (str(j+1),t_id,t_date, \
                    str(t_time),str(t_acct),str(t_trtype),str(t_amt),str(t_facct),str(t_tacct))
            #print "\n"
        print"---------------------------------------------------------------------------------------------------------------"



    def update_acct(self,acct_type):
        print"Function:update_acct() ==>"
        if (self.temp_cust_chk_acct == '' and self.temp_cust_sav_acct == ''):
            if acct_type == 'checking':
                self.view_customer_accounts('2')
            elif acct_type == 'saving':
                self.view_customer_accounts('3')

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
                balance = float(balance)
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

        #print"sending UPDATE Acct request.."
        err = self.cli_obj.sock.sendall(req_obj.toString())
        #if err != None:
        #    print" Send ERROR"
            
        #print "Waiting for response.."
        data = self.cli_obj.sock.recv(1024)

        #print "creating Response object"
        res_obj = Response(data)

        if(res_obj.resParams['status'] == 'SUCCESS'):
            print "Customer account updated successfully. New balance =>"
            if acct_type == 'checking':
                self.view_customer_accounts('2')
            elif acct_type == 'saving':
                self.view_customer_accounts('3')
        else:
            print "Update failure: Customer account could not be updated at this time"



    def update_customer_profile(self):
        print"Function:update_customer_profile() ==>"
        first_name = last_name = dob = email_id = phone_num = address = ''
        state = apt_num = street_name = city = country = zipcode = gender = ''

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
        choice = raw_input("APT number? ")
        if choice == 'Y' or choice == 'y':
            apt_num = raw_input("Enter New APT number: ")
        choice = raw_input("Street Name? ")
        if choice == 'Y' or choice == 'y':
            street_name = raw_input("Enter New Street name: ")
        choice = raw_input("City? ")
        if choice == 'Y' or choice == 'y':
            city = raw_input("Enter New City: ")
        choice = raw_input("State? ")
        if choice == 'Y' or choice == 'y':
            state = raw_input("Enter New State: ")
        choice = raw_input("Country? ")
        if choice == 'Y' or choice == 'y':
            country = raw_input("Enter New Country: ")
        choice = raw_input("Zipcode? ")
        if choice == 'Y' or choice == 'y':
            zipcode = raw_input("Enter New Zipcode: ")
        choice = raw_input("Gender? ")
        if choice == 'Y' or choice == 'y':
            gender = raw_input("Enter New Gender: ")

        if (first_name == '' and last_name == '' and dob == '' \
                and email_id == '' and phone_num == '' and address == '' \
                and apt_num == '' and street_name == '' and city == '' \
                and state == '' and country == '' and zipcode == '' and gender == ''):
            print"\n-----------------------"
            print" => No changes opted."
            print"-------------------------\n"

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
            req_obj.reqParams['email']=email_id
        if phone_num != '':
            req_obj.reqParams['phone']=phone_num
        if apt_num != '':
            req_obj.reqParams['apt_num']=apt_num
        if street_name != '':
            req_obj.reqParams['street_name']=street_name
        if city != '':
            req_obj.reqParams['city'] = city
        if state != '':
            req_obj.reqParams['state'] = state
        if country != '':
            req_obj.reqParams['country'] = country
        if zipcode != '':
            req_obj.reqParams['zipcode'] = zipcode
        if gender != '':
            req_obj.reqParams['gender'] = gender
        
        #print"sending UPDATE profile request.."
        #print"==> "+req_obj.toString()
        err = self.cli_obj.sock.sendall(req_obj.toString())
        #if err != None:
        #    print" Send ERROR"
            
        #print "Waiting for response.."
        data = self.cli_obj.sock.recv(1024)

        #print "creating Response object"
        res_obj = Response(data)

        if(res_obj.resParams['status'] == 'SUCCESS'):
            print "Customer account updated successfully."
            self.view_customer_profile()
        else:
            print "Update failure: Customer account could not be updated at this time"



    def create_customer_login_record(self):
        print "Function:create_customer_login_record() ==>"

        user_name = raw_input("User Name: ")
        password = raw_input("Password: ")
        customer_id = randint(1000000000, 2147483648)
        #print "Generated Customer id = " + str(customer_id)
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
        #if err != None:
        #    print" Send ERROR"
            
        #print "Waiting for response.."
        data = self.cli_obj.sock.recv(1024)

        #print "creating Response object"
        res_obj = Response(data)

        if(res_obj.resParams['status'] == 'SUCCESS'):
            print "New Customer login Created successfully"
            self.create_customer_account_record(customer_id)
        else:
            print "Create Failed - Error: " + res_obj.resParams['error']



    def create_customer_account_record(self, customer_id):
        print"Function:create_customer_account_record() ==>"

        chk_acct_num = randint(100000000, 2147483648)
        sav_acct_num = randint(100000000, 2147483648)

        req_obj = Request()
        req_obj.reqType = 'INSERT'
        req_obj.reqParams['client_type'] = self.cli_type
        req_obj.reqParams['subreq_type'] = 'INSERT_ACCT_RECORD'
        req_obj.reqParams['customer_chk_acct'] = chk_acct_num
        req_obj.reqParams['customer_sav_acct'] = sav_acct_num
        req_obj.reqParams['customer_id'] = customer_id
        req_obj.reqParams['customer_chk_bal'] = 0
        req_obj.reqParams['customer_sav_bal'] = 0

        err = self.cli_obj.sock.sendall(req_obj.toString())
        #if err != None:
        #    print" Send ERROR"

        #print "Waiting for response.."
        data = self.cli_obj.sock.recv(1024)

        #print "creating Response object"
        res_obj = Response(data)

        if(res_obj.resParams['status'] == 'SUCCESS'):
            print "Customer Account record created successfully"
            self.create_customer_profile_record(customer_id)

        else:
            print"Create Failed - Error: "+res_obj.resParams['error']
            # Delete Corresponding entry in the Customer login here



    def create_customer_profile_record(self, customer_id):
        print"Function:create_customer_profile_record() ==>"
        while True:
            first_name = raw_input("First Name: ")
            last_name = raw_input("Last_name: ")
            dob = raw_input("Date Of Birth: ")
            email = raw_input("Email: ")
            phone_num = raw_input("Phone number: ")
            apt_num = raw_input("Apt number: ")
            street_name = raw_input("Street num: ")
            city = raw_input("City: ")
            state = raw_input("State: ")
            country = raw_input("Country: ")
            zipcode = raw_input("Zipcode: ")
            gender = raw_input("Gender: ")
            if first_name != '' and last_name != '' and dob != '' \
                    and email != '' and phone_num != '' and apt_num != ''  \
                    and street_name != '' and city != '' and state != '' \
                    and country != '' and zipcode != '' and gender != '':
                break
            else: print "Some fields are empty. Enter all the details:"

        req_obj = Request()
        req_obj.reqType = 'INSERT'
        req_obj.reqParams['client_type'] = self.cli_type
        req_obj.reqParams['subreq_type'] = 'INSERT_PROFILE_RECORD'
        req_obj.reqParams['customer_id'] = customer_id
        req_obj.reqParams['first_name'] =  first_name
        req_obj.reqParams['last_name'] = last_name
        req_obj.reqParams['DOB'] = dob
        req_obj.reqParams['email'] = email
        req_obj.reqParams['phone'] = phone_num
        req_obj.reqParams['apt_num'] = apt_num
        req_obj.reqParams['street_name'] = street_name
        req_obj.reqParams['city'] = city
        req_obj.reqParams['state'] = state
        req_obj.reqParams['country'] = country
        req_obj.reqParams['zipcode'] = zipcode
        req_obj.reqParams['gender'] = gender
        err = self.cli_obj.sock.sendall(req_obj.toString())
        #if err != None:
        #    print" Send ERROR"

        #print "Waiting for response.."
        data = self.cli_obj.sock.recv(1024)

        #print "creating Response object"
        res_obj = Response(data)

        if(res_obj.resParams['status'] == 'SUCCESS'):
            print "Customer Profile Created sucessfully"

        else:
            print "Create Failed - Error: "+ res_obj+resParams['error']
            # Send Delete request to delete the corresponding entries
            # in customer_login and ACCOUNT_TABLE table


    
    def delete_customer_account(self):
        print"Function:delete_customer_account() ==>"
        customer_id = raw_input("Enter customer id: ")

        req_obj = Request()
        req_obj.reqType = 'DELETE'
        req_obj.reqParams['client_type'] = self.cli_type
        req_obj.reqParams['subreq_type'] = 'DELETE_LOGIN_RECORD'
        req_obj.reqParams['customer_id'] = customer_id

        err = self.cli_obj.sock.sendall(req_obj.toString())
        #if err != None:
        #    print" Send ERROR"
            
        #print "Waiting for response.."
        data = self.cli_obj.sock.recv(1024)

        #print "creating Response object"
        res_obj = Response(data)

        if(res_obj.resParams['status'] == 'SUCCESS'):
            print "Customer login Deleted"

            req_obj.reqType = 'DELETE'
            req_obj.reqParams['client_type'] = self.cli_type
            req_obj.reqParams['subreq_type'] = 'DELETE_ACCT_RECORD'
            req_obj.reqParams['customer_id'] = customer_id

            err = self.cli_obj.sock.sendall(req_obj.toString())
            #if err != None:
            #    print" Send ERROR"

            #print "Waiting for response.."
            data = self.cli_obj.sock.recv(1024)

            #print "creating Response object"
            res_obj = Response(data)

            if(res_obj.resParams['status'] == 'SUCCESS'):
                print "Customer Account Deleted"

                req_obj.reqType = 'DELETE'
                req_obj.reqParams['client_type'] = self.cli_type
                req_obj.reqParams['subreq_type'] = 'DELETE_PROFILE_RECORD'
                req_obj.reqParams['customer_id'] = customer_id

                err = self.cli_obj.sock.sendall(req_obj.toString())
                #if err != None:
                #    print" Send ERROR"

                #print "Waiting for response.."
                data = self.cli_obj.sock.recv(1024)

                #print "creating Response object"
                res_obj = Response(data)

                if(res_obj.resParams['status'] == 'SUCCESS'):
                    print "Customer Profile Deleted"

                else:
                    print "Create Failed - Error: "+ res_obj+resParams['error']
                    # Send Delete request to delete the corresponding entries
                    # in customer_login and ACCOUNT_TABLE table
            else:
                print"Create Failed - Error: "+res_obj.resParams['error']
                # Delete Corresponding entry in the Customer login here
        else:
            print "Create Failed - Error: " + res_obj.resParams['error']



######################### ADMIN CLASS  #########################

class Admin(object):
    def __init__(self, cli_obj, cli_id):
        self.cli_obj = cli_obj
        self.cli_type = 'Admin'
        self.cli_id = cli_id
    
        self.temp_teller_id = ''
        self.temp_teller_name = ''

    def display_admin_options(self):
        while True:
            print "1. View Tellers"
            print "2. View Teller information"
            print "3. View Transactions"
            print "4. Update Teller information"
            print "5. Create Teller record"
            print "6. Delete Teller record"
            print "7. Logout"

            choice = raw_input("your choice ->")

            if(choice == '1'):
                self.view_all_tellers()
            elif(choice == '2'):
                self.view_teller_info()
            elif(choice == '3'):
                self.view_transactions()
            elif(choice == '4'):
                self.update_teller_info()
            elif(choice == '5'):
                self.create_teller_login_record()
            elif(choice == '6'):
                self.delete_teller_record()
            elif(choice == '7'):
                # Logout
                return LOGOUT
            else:
                # Update Customer profile
                print "Invalid choice"

    
    def view_all_tellers(self):
        print "\nFunction: view_all_tellers() ==>"
        # create request object
        req_obj = Request()
        req_obj.reqType = 'GET'
        req_obj.reqParams['client_type'] = self.cli_type
        req_obj.reqParams['subreq_type'] = 'ALL_TELLER_ID'

        #print"sending GET Acct request.."
        err = self.cli_obj.sock.sendall(req_obj.toString())
        #if err != None:
        #    print" Send ERROR"
            
        data = self.cli_obj.sock.recv(1024)
        res_obj = Response(data)
        num_of_tellers = 0
        if(res_obj.resParams['status'] == 'SUCCESS'):
            #print tellers info    
            num_of_tellers = int(res_obj.resParams['total_teller_num'])
            if num_of_tellers == 0:
                print"TELLER RECORDS NOT FOUND"
            else:
                print"----------------------------------"
                print "%-17s %-17s" % ('TELLER NAME', 'TELLER ID')
                print"----------------------------------"
                for x in range(0, num_of_tellers):
                    teler = 'teller'+str(x+1)
                    teller_name, teller_id = res_obj.resParams[teler].split("/")
                    #print "'{:>20}'.format(teller_name)" +"'{:>20}'.format(teller_id)"
                    print"%-17s %-17s" % (teller_name, teller_id)
                print"----------------------------------"
        else:
            print"Server Error. Unable to get Tellers information"


    def view_teller_info(self):
        print"\nFunction:view_teller_info() ==>"
        self.view_all_tellers()
        teller_id = raw_input("Teller ID ->")
        # create request object
        req_obj = Request()
        req_obj.reqType = 'GET'
        req_obj.reqParams['client_type'] = self.cli_type
        req_obj.reqParams['subreq_type'] = 'TELLER_PROFILE'
        req_obj.reqParams['teller_id'] = teller_id

        #print"sending GET Acct request.."
        err = self.cli_obj.sock.sendall(req_obj.toString())
        #if err != None:
        #    print" Send ERROR"
            
        data = self.cli_obj.sock.recv(1024)
        res_obj = Response(data)
        if(res_obj.resParams['status'] == 'SUCCESS'):
            self.temp_teller_id = res_obj.resParams['teller_id']
            print"\n---------------------------------------------"
            print"Teller ID    : "+res_obj.resParams['teller_id']
            print"First Name   : "+res_obj.resParams['first_name']
            print"Last Name    : "+res_obj.resParams['last_name']     
            print"Date of Birth: "+res_obj.resParams['DOB']
            print"Email Address: "+res_obj.resParams['email']
            print"Phone Number : "+res_obj.resParams['phone']
            print"Address      : "+res_obj.resParams['address']
            print"---------------------------------------------\n"

        else:
            print"==> RECORD NOT FOUND\n"

    def view_transactions(self):
        print"Function: view_transactions() ==> "
        while True:
            month = raw_input("Enter Month -> ")
            #print"month="+month
            if((int(month)) >= 1 and (int(month)) <= 12):
                break
            else:
                print"Enter a valid month of the year(1 >= range <= 12) "

        # create request object
        req_obj = Request()
        req_obj.reqType = 'GET'
        req_obj.reqParams['client_type'] = self.cli_type
        req_obj.reqParams['subreq_type'] = 'MONTH_TRANSACTIONS'
        req_obj.reqParams['month'] = month

        #print"sending GET Acct request.."
        err = self.cli_obj.sock.sendall(req_obj.toString())
        #if err != None:
        #    print" Send ERROR"

        data = self.cli_obj.sock.recv(1024)
        res_obj = Response(data)
        if(res_obj.resParams['status'] == 'SUCCESS'):
            if(res_obj.resParams['trns_list'] == ''):
                print"==> NO TRANSACTIONS FOUND FOR GIVEN MONTH\n"
            else:
                self.print_transactions(res_obj.resParams['trns_list'])
        else:
            print"Server error. Failed to get transactions at this time"


    def print_transactions(self, trns_str):
        print "\nFunction: print_transactions() ==> "
        trns_list = trns_str.split()
        #print trns_list
        #print"\n"
        print"%-3s %-14s %-12s %-10s %-8s %-18s %-12s %-13s %-15s" % ('NUM','CUSTOMER ID', \
                'DATE','TIME','ACCOUNT','TRANSACTION TYPE','AMOUNT','FROM ACCOUNT', 'TO_ACCOUNT')
        print"---------------------------------------------------------------------------------------------------------------"
        for i in range(0,len(trns_list),8):
            for j in range(0,8):
                #print trns_list[i+j]
                key, t_id = trns_list[i+0].split('-')
                key, t_date = trns_list[i+1].split('-')
                key, t_time = trns_list[i+2].split('-')
                key, t_acct = trns_list[i+3].split('-')
                key, t_trtype = trns_list[i+4].split('-')
                key, t_amt = trns_list[i+5].split('-')
                key, t_facct = trns_list[i+6].split('-')
                if t_facct is '':
                    t_facct = ' '
                key, t_tacct = trns_list[i+7].split('-')
                if t_facct is '':
                    t_facct = ' '
            print "%-3s %-14s %-12s %-10s %-11s %-16s %-12s %-13s %-15s" % (str(j+1),t_id,t_date, \
                    str(t_time),str(t_acct),str(t_trtype),str(t_amt),str(t_facct),str(t_tacct))
            #print "\n"
        print"---------------------------------------------------------------------------------------------------------------"


    
    def update_teller_info(self):
        print"\nFunction: update_teller_info() ==> "

        self.view_all_tellers()
        first_name = last_name = dob = email_id = phone_num = address = ''
        apt_num = street_name = city = country = zipcode = gender = ''

        teller_id = raw_input("Teller_ID ->")

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
        choice = raw_input("APT number? ")
        if choice == 'Y' or choice == 'y':
            apt_num = raw_input("Enter New APT number: ")
        choice = raw_input("Street Name? ")
        if choice == 'Y' or choice == 'y':
            street_name = raw_input("Enter New Street name: ")
        choice = raw_input("City? ")
        if choice == 'Y' or choice == 'y':
            city = raw_input("Enter New City: ")
        choice = raw_input("State? ")
        if choice == 'Y' or choice == 'y':
            state = raw_input("Enter New State: ")
        choice = raw_input("Country? ")
        if choice == 'Y' or choice == 'y':
            country = raw_input("Enter New Country: ")
        choice = raw_input("Zipcode? ")
        if choice == 'Y' or choice == 'y':
            zipcode = raw_input("Enter New Zipcode: ")
        choice = raw_input("Gender? ")
        if choice == 'Y' or choice == 'y':
            gender = raw_input("Enter New Gender: ")

        if (first_name == '' and last_name == '' and dob == '' \
                and email_id == '' and phone_num == '' and address == '' \
                and apt_num == '' and street_name == '' and city == '' \
                and state == '' and country == '' and zipcode == '' and gender == ''):
            print"\n-----------------------"
            print" => No changes opted."
            print"-------------------------\n"

            return

        # create request object
        req_obj = Request()
        req_obj.reqType = 'SET'
        req_obj.reqParams['client_type'] = self.cli_type
        req_obj.reqParams['customer_id'] = teller_id
        req_obj.reqParams['subreq_type'] = 'UPDATE_TELLER_PROFILE'
        if first_name != '':
            req_obj.reqParams['first_name']=first_name
        if last_name != '':
            req_obj.reqParams['last_name']=last_name
        if dob != '':
            req_obj.reqParams['DOB']=dob
        if email_id != '':
            req_obj.reqParams['email']=email_id
        if phone_num != '':
            req_obj.reqParams['phone']=phone_num
        if apt_num != '':
            req_obj.reqParams['apt_num']=apt_num
        if street_name != '':
            req_obj.reqParams['street_name']=street_name
        if city != '':
            req_obj.reqParams['city'] = city
        if city != '':
            req_obj.reqParams['state'] = state
        if country != '':
            req_obj.reqParams['country'] = country
        if zipcode != '':
            req_obj.reqParams['zipcode'] = zipcode
        if gender != '':
            req_obj.reqParams['gender'] = gender

        #print"sending UPDATE profile request.."
        #print"==> "+req_obj.toString()
        err = self.cli_obj.sock.sendall(req_obj.toString())
        #if err != None:
        #    print" Send ERROR"
            
        #print "Waiting for response.."
        data = self.cli_obj.sock.recv(1024)

        #print "creating Response object"
        res_obj = Response(data)

        if(res_obj.resParams['status'] == 'SUCCESS'):
            print "Teller account updated successfully."
            self.view_customer_profile()
        else:
            print "Update failure: Teller account could not be updated at this time"
            

    def create_teller_login_record(self):
        print "\nFunction:create_teller_login_record() ==>"

        user_name = raw_input("Teller Name: ")
        password = raw_input("Password: ")
        customer_id = randint(1000, 9999)
        #customer_id = randint(1000000000, 2147483648)
        #print "Generated Customer id = " + str(customer_id)
        client_type = 'Teller'

        req_obj = Request()
        req_obj.reqType = 'INSERT'
        req_obj.reqParams['client_type'] = self.cli_type
        req_obj.reqParams['subreq_type'] = 'INSERT_LOGIN_RECORD'
        req_obj.reqParams['user_name'] =  user_name
        req_obj.reqParams['password'] = password
        req_obj.reqParams['customer_id'] = customer_id
        req_obj.reqParams['record_client_type'] = client_type

        err = self.cli_obj.sock.sendall(req_obj.toString())
        #if err != None:
        #    print" Send ERROR"
            
        #print "Waiting for response.."
        data = self.cli_obj.sock.recv(1024)

        #print "creating Response object"
        res_obj = Response(data)

        if(res_obj.resParams['status'] == 'SUCCESS'):
            print "New Teller login Created successfully"
            self.create_teller_info_record(customer_id)
        else:
            print "Create Failed - Error: " + res_obj.resParams['error']


    def create_teller_info_record(self, teller_id):
        print"Function:create_teller_info_record() ==>"
        while True:
            first_name = raw_input("First Name: ")
            last_name = raw_input("Last_name: ")
            dob = raw_input("Date Of Birth: ")
            email = raw_input("Email: ")
            phone_num = raw_input("Phone number: ")
            apt_num = raw_input("Apt number: ")
            street_name = raw_input("Street num: ")
            city = raw_input("City: ")
            state = raw_input("State: ")
            country = raw_input("Country: ")
            zipcode = raw_input("Zipcode: ")
            gender = raw_input("Gender: ")
            if first_name != '' and last_name != '' and dob != '' \
                    and email != '' and phone_num != '' and apt_num != ''  \
                    and street_name != '' and city != '' and state != '' \
                    and country != '' and zipcode != '' and gender != '':
                break
            else: print "Some fields are empty. Enter all the details:"

        req_obj = Request()
        req_obj.reqType = 'INSERT'
        req_obj.reqParams['client_type'] = self.cli_type
        req_obj.reqParams['subreq_type'] = 'INSERT_PROFILE_RECORD'
        req_obj.reqParams['teller_id'] = teller_id
        req_obj.reqParams['first_name'] =  first_name
        req_obj.reqParams['last_name'] = last_name
        req_obj.reqParams['DOB'] = dob
        req_obj.reqParams['email'] = email
        req_obj.reqParams['phone'] = phone_num
        req_obj.reqParams['apt_num'] = apt_num
        req_obj.reqParams['street_name'] = street_name
        req_obj.reqParams['city'] = city
        req_obj.reqParams['state'] = state
        req_obj.reqParams['country'] = country
        req_obj.reqParams['zipcode'] = zipcode
        req_obj.reqParams['gender'] = gender
        err = self.cli_obj.sock.sendall(req_obj.toString())
        #if err != None:
        #    print" Send ERROR"

        #print "Waiting for response.."
        data = self.cli_obj.sock.recv(1024)

        #print "creating Response object"
        res_obj = Response(data)

        if(res_obj.resParams['status'] == 'SUCCESS'):
            print "Teller Profile Created sucessfully"

        else:
            print "Create Failed - Error: "+ res_obj+resParams['error']
            # Send Delete request to delete the corresponding entries
            # in customer_login and ACCOUNT_TABLE table


    def delete_teller_record(self):
        print"\nFunction: delete_teller_record() ==>"
        self.view_all_tellers()
        teller_id = raw_input("Enter Teller id: ")

        req_obj = Request()
        req_obj.reqType = 'DELETE'
        req_obj.reqParams['client_type'] = self.cli_type
        req_obj.reqParams['subreq_type'] = 'DELETE_LOGIN_RECORD'
        req_obj.reqParams['customer_id'] = teller_id

        err = self.cli_obj.sock.sendall(req_obj.toString())
        if err != None:
            print" Send ERROR"
            
        #print "Waiting for response.."
        data = self.cli_obj.sock.recv(1024)

        #print "creating Response object"
        res_obj = Response(data)

        if(res_obj.resParams['status'] == 'SUCCESS'):
            print "Teller Login record Deleted successfully"
            self.delete_teller_info_record(teller_id)


    def delete_teller_info_record(self, teller_id):
        print"\nFunction:delete_teller_info_record() ==>"
        req_obj = Request()
        req_obj.reqType = 'DELETE'
        req_obj.reqParams['client_type'] = self.cli_type
        req_obj.reqParams['subreq_type'] = 'DELETE_PROFILE_RECORD'
        req_obj.reqParams['teller_id'] = teller_id

        err = self.cli_obj.sock.sendall(req_obj.toString())
        #if err != None:
        #    print" Send ERROR"

        #print "Waiting for response.."
        data = self.cli_obj.sock.recv(1024)

        #print "creating Response object"
        res_obj = Response(data)

        if(res_obj.resParams['status'] == 'SUCCESS'):
            print "Teller Profile Deleted"

        else:
            print "Delete Failed - Error: "+ res_obj+resParams['error']
            # Send Delete request to delete the corresponding entries
            # in customer_login and ACCOUNT_TABLE table



    def create_admin_record(self):
        pass
    def delete_admin_record(self):
        pass

#################### SOCKET CONNECTION CLASS  ####################
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
#--------------------------------------------------------
# Below two lines enables normal connection without ssl
        #self.sock = socket.socket()
        #err = self.sock.connect((self.host,self.port))
#--------------------------------------------------------       

#----------------------------------------------------------------------------------
# Below two lines enables ssl
        self.orig_sock = socket.socket()
        # use SSL wrapped socket to connect to the server
        self.sock = ssl.wrap_socket(self.orig_sock, ssl_version=ssl.PROTOCOL_TLSv1)
        err = self.sock.connect((self.host, self.port))
#----------------------------------------------------------------------------------
        return err

    # login into the system
    def login(self, usr, pwd):
        print"\nFunction login() ==>"
        self.usr = usr
        self.pwd = pwd

        # create request object
        req_obj = Request()

        req_obj.reqType = 'LOGIN'
        req_obj.reqParams['username'] = self.usr
        req_obj.reqParams['password'] = self.pwd

        #print"sending Login request.."
        err = self.sock.sendall(req_obj.toString())
        #print "err = " + str(err)
        #if err != None:
        #    print"login(): returning error here"
        #    return [ERROR,'','']
            
        #print "login(): Waiting for response.."
        data = self.sock.recv(1024)

        #print "creating Response object"
        res_obj = Response(data)

        if(res_obj.resParams['status'] == 'SUCCESS'):
            #print "login():client type : "+ res_obj.resParams['client_type']
            res_list = [res_obj.resParams['status'],res_obj.resParams['client_type'],res_obj.resParams['client_id']]
            return res_list
        else:
            #print "login(): returning ERROR"
            return [ERROR,'','']
        
    def closeconnection(self):
        self.sock.close()


######################### MAIN  #########################
def main():
    try:
        # create TCP connection with the server
        cc1 = ClientConnection()
    except Exception, e:
        print e
        return

    print "Client connection successful"
    while True:
        usr = raw_input("Login Name: -> ")
        pwd = raw_input("Password: -> ")

        if usr != '' and pwd != '':
            break
        else:
            print"Error: Login / password empty"

    # send login credentials
    res_list = cc1.login(usr, pwd)
    #print"res_list ="
    #print res_list

    if (res_list[0] == ERROR):
        print "Authentication Failure"
    else:
        if (res_list[1] == 'Customer'):
            #create customer object
            cst_user = Customer(cc1,usr,pwd, res_list[2])
            cst_user.display_customer_options()

        elif (res_list[1] == 'Teller'):
            #create teller object
            tel_user = Teller(cc1, res_list[2])
            while True:
                choice = tel_user.display_teller_options()
                if(choice == LOGOUT):
                    break

        elif (res_list[1] == 'Admin'):
            #create admin user
            admin_user = Admin(cc1, res_list[2])
            while True:
                choice = admin_user.display_admin_options()
                if(choice == LOGOUT):
                    break
            
        else:
            #user authentication failed
            print "Unknown Client_type.Closing the connection"
    
    cc1.closeconnection()


if __name__ == "__main__":
    main()
