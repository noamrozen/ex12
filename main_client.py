from four_in_a_row import main
import socket

if __name__ == '__main__':
    ip = socket.gethostbyname(socket.gethostname())

    main([None, "ai", 8000, ip])