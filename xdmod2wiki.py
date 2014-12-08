from xdmodgg.graph import Graph
from getpass import getpass
import xmlrpclib


def format_image(name):
    return '<p><ac:image><ri:attachment ri:filename="{0}" /></ac:image></p>'.format(name)


def main():
    g = Graph("cpu-stats", "http://xdmod.rc.rit.edu", statistic="total_cpu_hours")
    server = xmlrpclib.Server("https://wiki.rit.edu/rpc/xmlrpc")
    client = server.confluence2
    auth_token = client.login(getpass("Username: "), getpass("Password: "))
    print(auth_token)
    test_page = client.getPage(auth_token, "rc", "Test XDMOD Graph Exports")
    print(test_page)
    attach_name = "{0}.{1}".format(g.name, g.options['format'])
    attach_mime = "image/{0}".format(g.options['format'])
    image = xmlrpclib.Binary(g.download().read())
    new_a = client.addAttachment(
        auth_token,
        test_page['id'],
        {
            'fileName': attach_name,
            'contentType': attach_mime,
        },
        image)
    print(new_a)
    test_page.update({
        "content": "{0}\n{1}".format(test_page["content"], format_image(new_a['fileName']))
    })
    np = client.updatePage(auth_token, test_page, {})
    print(np)


if __name__ == "__main__":
    main()
