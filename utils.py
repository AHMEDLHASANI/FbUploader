def LinksFilter(Links) -> tuple :
     _Links = []
     pattern = "^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"
     for link in c, v, p:
         for _ in link:
             if match(pattern,_) :
                 _Links.append(_)
     return _Links
def DescriptionMaker(string,Dict):
    String = string
    for Key,Value in Dict.items():
        String = String.replace(Key,str(Value))
    return String