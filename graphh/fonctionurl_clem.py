def url_def(self, listedargument):
    url = GraphHopper.url + listedargument[0] + "?"
    for argument in listedargument[1:]:
        url += argument + "&"
    url += "key=" + self.APIKey
    fp = urllib.request.urlopen(url)
    d_res = json.load(fp)
    return d_res

