#!/bin/env python
# coding:utf-8
import socket
import select
listen_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
listen_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_fd.bind(("0.0.0.0", 8828))
listen_fd.listen(10)
epoll_sock = select.epoll()
epoll_sock.register(listen_fd.fileno(), select.EPOLLIN)
fdsock = {
    listen_fd.fileno(): listen_fd,
}
buf = ""
sent = 0
while True:
    epoll_list = epoll_sock.poll()
    for fd, events in epoll_list:
        if select.EPOLLIN & events:
        #print fd, events
            if fd == listen_fd.fileno():
                conn, addr = listen_fd.accept()
                conn.setblocking(0)
                print conn, addr, conn.fileno()
                epoll_sock.register(conn.fileno(), select.EPOLLIN)
                fdsock[conn.fileno()] = conn
            else:
                buf += fdsock[fd].recv(100)
                if len(buf) > 2 and buf[-2:] == '\r\n':
                    buf = buf[:-2][::-1] + '\r\n'
                    epoll_sock.unregister(conn)
                    epoll_sock.register(conn.fileno(), select.EPOLLOUT)
        elif select.EPOLLOUT & events:
            print sent, buf
            s = fdsock[fd].send(buf[sent:])
            print 's', s
            if s > 0:
                sent += s
            if sent == len(buf):
                epoll_sock.unregister(conn)
                epoll_sock.register(conn.fileno(), select.EPOLLIN)
                buf = ""
                sent = 0
                
