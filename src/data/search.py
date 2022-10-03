import requests as req, re
from bs4 import BeautifulSoup as par

img, typeK, judulEN, judulIND, info, chapter = [],[],[],[],[],[]
data,all = {},{}

class Main:

    def request(url):
        if("/cari/" in url):
            img.clear();typeK.clear();judulEN.clear();judulIND.clear();info.clear();chapter.clear();data.clear();all.clear()
        r = par(req.get(url).text, "html.parser")
        for x in r.find("main").find("section").find("div",{"class":"daftar"}).find_all("div",{"class":"bge"}):
            #bgei
            for b in x.find_all("div",{"class":"bgei"}):
                for a in b.find_all("a"):
                    for i in a.find_all("img"):
                        img.append(i.get("data-src"))
                    for t in a.find_all("div"):
                        text = re.findall('\<\/b\>\s(\w+)', str(t))[0]
                        typeK.append(t.find("b").string+" "+str(text))

            #content
            for k in x.find_all("div",{"class":"kan"}):
                #judulEN
                for j in k.find_all("h3"):
                    judulEN.append(" ".join(re.findall('(\w+)', str(j.string))))
                
                #judulIND
                for j in k.find_all("span",{"class":"judul2"}):
                    judulIND.append(j.string)

                #info
                for s in k.find_all("p"):
                    info.append(" ".join(re.findall('(\w+)', str(s.string))))

                #chapter
                for c in k.find_all("div",{"class":"new1"}):
                    for a in c.find_all("a"):
                        try:
                            chp = re.findall('\<span\>Terbaru: <\/span\><span\>Chapter (.*?)<\/span\>', str(a))[0]
                            chapter.append(chp)
                        except:pass

        for im,t,jE,jI,i,c in zip(img,typeK,judulEN,judulIND,info,chapter):
            data.update(
                
                {
                    jE:
                    {
                        "img":im,
                        "type":t,
                        "judul-EN":jE,
                        "judul-IND":jI,
                        "info":i,
                        "chapter":c
                    }
                }
            )

        try:
            next = r.find("a",{"class":"next"}).get("href")
            Main.request("https://data.komiku.id"+next)
        except:pass

        all.update(
            {
                "data":data,
                "hasil-pencarian":len(judulEN)
            }
        )

        return all

#print(Main.request("https://data.komiku.id/cari/?post_type=manga&s=god"))
