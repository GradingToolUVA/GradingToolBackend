from bs4 import BeautifulSoup
import requests
import argparse
import os, sys

class Parser:
    def parse(self, url):
        req = requests.get(url)
        soup = BeautifulSoup(req.content, "html.parser")

        tags = {tag.name for tag in soup.find_all()}
  
        main = None
        # iterate all tags
        for tag in tags:
          
            # find all element of tag
            for i in soup.find_all( tag ):
          
                # if tag has attribute of role
                if i.has_attr( "role" ):
                    if i['role'] == "main":
                        main = i

        head = soup.find_all("head")[0]
        header = soup.find_all("header")[0]
        # main = soup.find_all("div")[0]

        return head, header, main
          
                    # if len( i['class'] ) != 0:
                    #     class_list.add(" ".join( i['class']))
      

        # data = [ele.text for ele in soup.find_all(text = True) if ele.text.strip() != '']
        # return soup


    def find_links(self, url):
        req = requests.get(url)
        soup = BeautifulSoup(req.content, "html.parser")

        front_cutoff = url.find("/vt.edu/")
        end_cutoff = url.find("?authuser=0")
        pattern = url[front_cutoff : end_cutoff] #for matching purposes when filtering the links we don't need

        website_urls = []
        for a in soup.find_all('a', href=True):
            if a.has_attr('title'):
                if pattern in a['href'] and pattern != a['href']:
                    link = {"url": a['href'], "name": a['title']}
                    if link not in website_urls:
                        website_urls.append({"url": a['href'], "name": a['title']})

        return website_urls

    def parse_all(self, url):
        website_urls = self.find_links(url)
        data = []

        for page in website_urls:
            head, header, main = self.parse(f"https://sites.google.com{page['url']}")
            output = str(head) + str(main)
            data.append({"url": page['url'], "name": page['name'], "html": output})

        return data


    def write_to_file(self, soup, path="some path that makes sense"):
        with open(path, 'w') as outfile:
            outfile.write(soup)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="URL to parse")
    parser.add_argument("-p", "--path", help="location to write to")
    args = parser.parse_args()

    assert args.url is not None

    url = args.url
    path = args.path if args.path else "./output.html"

    p = Parser()

    # p.parse_all(url)

    # sys.exit()

    # head, header, main = p.parse(url)

    # output = str(head) + str(header) + str(main)
    output = str(p.parse(url))
    # print(output)

    p.write_to_file(output, path)

    with open(path, 'r') as infile:
        check_output = infile.read()

    assert output == check_output