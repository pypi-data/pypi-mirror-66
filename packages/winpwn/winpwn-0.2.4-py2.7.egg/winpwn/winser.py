import sock
import threading
from .winpwn import remote
from .asm import asm as ASM
from .asm import disasm as DISASM
from .misc import u32,p32,Latin1_encode,Latin1_decode
class wincs():
    def __init__(self,ip=None,port=512):
        winser_socket=None
        wincli_socket=None
        if ip is None: # server
            winser_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            winser_socket.bind((socket.gethostname(), port))
            winser_socket.listen()
            (conn, client_ip) = serversocket.accept()
            threading.Thread(target=self.__winser_thread,args=(conn,client_ip)).start()
        else: # client
            wincli_socket=remote(ip,port)
    def __winser_thread(self,conn,client_ip): # [0:1]-> opcode; [1:5] -> len; [5:5+len]->asmcode/machinecode
        while(1):
            opcode=LLatin1_decode(conn.recv(1))
            length=u32(Latin1_decode(conn.recv(4)))
            code=Latin1_decode(conn.recv(length))
            if opcode=='\x03':
                self.winser_socket.close()
            elif opcode=='\x01':
                asmcode=ASM(code)
                conn.send(p32(len(asmcode))+asmcode)
            elif opcode=='\x02':
                disasmcode=DISASM(code)
                conn.send(p32(len(disasmcode))+disasmcode)
            else:
                raise Exception("Error in winser.wincs().__winser_thread when parse opcode")
    def asm(self,asmcode):
        self.wincli_socket.send(Latin1_encode('\x01'+p32(len(asmcode))+asmcode))
        return self.wincli_socket.recvn(u32(self.wincli_socket.recvn(4)))

    def disasm(self,machinecode):
        self.wincli_socket.send(Latin1_encode('\x02'+p32(len(asmcode))+machinecode))
        return self.wincli_socket.recvn(u32(self.wincli_socket.recvn(4)))
    def close():
        self.wincli_socket.send('\x03')
        self.wincli_socket.close()