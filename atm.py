import config
import socket
import select
import sys

class atm:
  def __init__(self):
    self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.s.bind((config.local_ip, config.port_atm))

  def __del__(self):
    self.s.close()

  def sendBytes(self, m):
    self.s.sendto(m, (config.local_ip, config.port_router))

  def recvBytes(self):
      data, addr = self.s.recvfrom(config.buf_size)
      if addr[0] == config.local_ip and addr[1] == config.port_router:
        return True, data
      else:
        return False, bytes(0)

  #====================================================================
  # TO DO: Modify the following function to output prompt properly
  #====================================================================
  def prompt(self):
    sys.stdout.write("ATM: ")
    sys.stdout.flush()

  def prompt2(self):
      sys.stdout.write("ATM (" + details[1].strip() + "): ")
      sys.stdout.flush()


  #====================================================================
  # TO DO: Modify the following function to handle the console input
  #====================================================================
  def handleLocal(self,m):
    self.sendBytes(bytes(m, "utf-8"))


    flag = 0
    if m== "begin-session":
        #the user inserts their card (before starting program, copy user's card info into Inserted.card)
        #user enters pin
        #verify PIN
        f1 = open("Inserted.card","r+")
        card = f1.read()
        details = card.split(" ")
        pin = input("PIN? ")
        #if the pin is not 4 characters long, or if the pin has anything besides digits in it, or if it is the wrong pin, cancel transaction
        if len(pin) != 4 or pin.isdigit() != True or pin != details[0]:
            sys.stdout.write("Unauthorized\n")
            self.prompt()
        else: #they entered the correct pin
            sys.stdout.write("Authorized\n")
            currentuser = details[1].strip()
            currentuser = str(currentuser)
            self.sendBytes(bytes(currentuser, "utf-8"))
            flag = 1
    while flag == 1:

        #self.prompt2()
        sys.stdout.write("ATM (" + details[1].strip() + "): ")
        sys.stdout.flush()
        m = sys.stdin.readline().rstrip("\n")
        #print(m)
        if "withdraw" in m:
            value = m.split()
            #print(value[0])
            #print(value[1])
            if value[1] != int:
              sys.stdout.write("Unauthorized\n")
              self.prompt()
            if int(value[1]) <= int(details[2]):
                print("$" + value[1] + " dispensed\n")
                details[2] = int(details[2]) - int(value[1])
                detailstr = ""
                for item in details:
                    detailstr = detailstr + " " + str(item)
                    name = details[1].strip() + ".card"
                    f1 = open(name, "r+")
                    f1.write(detailstr)
            #check that the user has sufficient funds
            #if they do, subtract from their balance
            #do something
            else:
                sys.stdout.write("Insufficent Funds\n")
        elif m == "balance":
            sys.stdout.write("$" + str(details[2]) + "\n")
        elif m == "end-session":
            sys.stdout.write("User logged out\n")
            flag = 0

        else:
            sys.stdout.write("Invalid command: Visit your local branch for more details\n")
    else:
        sys.stdout.write("No user logged in\n")
        self.prompt()

  #====================================================================
  # TO DO: Modify the following function to handle the bank's reply
  #====================================================================
  def handleRemote(self, inBytes):
    print("From Bank: ", inBytes.decode("utf-8") )
    self.prompt()


  def mainLoop(self):
    self.prompt()

    while True:
      l_socks = [sys.stdin, self.s]

      # Get the list sockets which are readable
      r_socks, w_socks, e_socks = select.select(l_socks, [], [])

      for s in r_socks:
        # Incoming data from the router
        if s == self.s:
          ret, data = self.recvBytes()
          if ret == True:
            self.handleRemote(data) # call handleRemote


        # User entered a message
        elif s == sys.stdin:
          m = sys.stdin.readline().rstrip("\n")
          if m == "quit":
            return
          self.handleLocal(m) # call handleLocal






if __name__ == "__main__":
  card = open("Inserted.card","r").read()
  details = card.split(",")
  a = atm()
  a.mainLoop()
