#!/usr/bin/env python

import socket
from webob import Response


def get_path(http_request):
    # noinspection PyBroadException
    try:
        return http_request.split()[1]
    except:
        return False


def get_file_contents(path):
    """Returns the contents of the specified file as a string. Path should include the name of the file."""
    path = path[1:]  # remove the leading slash
    file_obj = open(path)
    contents = file_obj.read()
    file_obj.close()
    return contents


def compute_content_type(path):
    """Returns the content type associated with file with the given path"""
    suffix = path[path.find('.')+1:]
    if suffix == 'txt':
        return 'text/plain'
    elif suffix == 'jpg':
        return 'image/jpeg'
    elif suffix == 'png':
        return 'image/png'
    elif suffix == 'js':
        return 'text/javascript'
    elif suffix == 'css':
        return 'text/css'
    elif suffix == 'gif':
        return 'image/gif'
    else:
        return 'text/html'


def main():

    doc_root = ''
    doc_index = '/index.html'
    site_index = '/site_index.html'
    file_not_found_page = '/no_such_file.html'

    valid_paths = ['/', doc_index, site_index, file_not_found_page, '/books/tomsawyer.txt',
                   '/books/theimportanceofbeingearnest.txt', '/pictures/puppy.jpg', '/pictures/catfight.jpg',
                   '/favicon.ico', '/pictures/clouds.jpg']

    directories = ['pictures', 'books']

    redirects = {
        '/home': doc_index,
        '/index': doc_index,
        '/': doc_index,
        '/puppy': '/pictures/puppy.jpg',
        '/cat': '/pictures/catfight.jpg',
        '/catfight': '/pictures/catfight.jpg',
        '/tomsawyer': '/books/tomsawyer.txt',
        '/earnest': '/books/theimportanceofbeingearnest.txt'
    }

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 8080))
    sock.listen(5)

    while True:
        try:
            conn, client_address = sock.accept()
            request = conn.recv(1024)
        except KeyboardInterrupt, socket.error:
            sock.shutdown(2)
            print("Shutting down..")
            break

        print('received "%s"' % request)
        res = Response()
        path = get_path(request)

        if path in redirects:
            res.status_code = 302
            res.location = doc_root + redirects[path]
        # requested a valid document
        elif path in valid_paths:
            res.status_code = 200
            res.location = doc_root + path
        # requested a directory
        elif path[1:] in directories:
            res.location = doc_root + site_index
        # don't have the requested file
        else:
            res.status_code = 404
            res.location = doc_root + file_not_found_page

        body = get_file_contents(res.location)
        res.content_type = compute_content_type(res.location)

        res.body = body
        res.headers['Connection'] = 'close'
        conn.send(str(body))
        conn.close()


if __name__ == '__main__':
    main()
