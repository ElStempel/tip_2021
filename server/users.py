class User:
    def __init__(self, tcpConn, name, addr, udpPort):
        self.tcpConn = tcpConn
        self.name = name
        self.tcpAddr = addr
        self.udpAddr = (addr[0],udpPort)
    