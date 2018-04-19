import config
import socket
import select
import sys

class bank:
  def __init__(self):
    self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.s.bind((config.local_ip, config.port_bank))

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
    sys.stdout.write("BANK: ")
    sys.stdout.flush()


  #====================================================================
  # TO DO: Modify the following function to handle the console input
  #====================================================================
  def handleLocal(self,m):
    self.sendBytes(bytes(m, "utf-8"))
    self.prompt()


    while 1:
        info = m.split(" ")
        try:
            name = info[1].strip() + ".card"
        except IndexError:
            break
        except ValueError:
            break
        try:
            f1 = open(name, "r+")
            card = f1.read()
            details = card.split()
        except NameError:
            sys.stdout.write("User not in system.  Please contact your local branch to create an account!\n")
            break
        except IOError:
            sys.stdout.write("User not in system.  Please contact your local branch to create an account!\n")
        except IndexError:
            sys.stdout.write("User not in system.  Please contact your local branch to create an account!\n")
            break
        flag = 1

        #if command is balance, print balance (info[2])
        if info[0] == "balance":
            try:
                sys.stdout.write("$" + details[2] + "\n")
            except IndexError:
                break
        elif info[0] == "deposit":
            #print("$" + value[1])
            if len(info) > 2:
              if "$" in info[2]:
                  sys.stdout.write("Dollar sign is not a valid input. Please try your command without the symbol\n")
                  break
              try:
                  details[2] = int(details[2]) + int(info[2])

              except IndexError:
                  break
              sys.stdout.write("$" + str(info[2]) + " added to " + str(details[1]) + "'s account" + "\n")
              detailstr = ""
              for item in details:
                  detailstr = detailstr + " " + str(item)
              f1 = open(name, "r+")
              f1.write(detailstr)
            else:
                #whatever
                pass
        sys.stdout.write("BANK: ")
        sys.stdout.flush()
        m = sys.stdin.readline().rstrip("\n")

  #====================================================================
  # TO DO: Modify the following function to handle the atm request
  #====================================================================
  def handleRemote(self, inBytes):
    #print("\nFrom ATM: ", inBytes.decode("utf-8") )
    #self.sendBytes(inBytes)

    print("\n")
    queries = inBytes.decode("utf-8").split(" ")
    #print(queries[0])
    if queries[0] == "Alice":
      #print("received")
      #start working on the logic for accepting commands from ATM to change the global variables below



    self.prompt()
  def mainLoop(self):
    self.prompt()

    #Permitted Users
    global Alice, Bob, Carol

    #Account Values
    Alice = 100
    Bob = 100
    Carol = 0





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
  b = bank()
  b.mainLoop()
