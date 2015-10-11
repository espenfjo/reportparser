import hashlib
import urllib2
import urllib
import re
import io
from datetime import datetime
import pycountry
from tempfile import TemporaryFile
from bs4 import BeautifulSoup, Comment

from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

def datetime_serialiser(obj):
    """
    Datetime JSON serializer
    """
    if isinstance(obj, datetime):
        obj = str(obj)
    return obj

class Parser(object):
    """
    Common parser class
    """
    tldlist = "ABOGADO|AC|ACADEMY|ACCOUNTANTS|ACTIVE|ACTOR|AD|ADULT|AE|AERO|AF|AG|AGENCY|AI|AIRFORCE|AL|ALLFINANZ|ALSACE|AM|AN|ANDROID|AO|AQ|AQUARELLE|AR|ARCHI|ARMY|ARPA|AS|ASIA|ASSOCIATES|AT|ATTORNEY|AU|AUCTION|AUDIO|AUTOS|AW|AX|AXA|AZ|BA|BAND|BAR|BARGAINS|BAYERN|BB|BD|BE|BEER|BERLIN|BEST|BF|BG|BH|BI|BID|BIKE|BIO|BIZ|BJ|BLACK|BLACKFRIDAY|BLOOMBERG|BLUE|BM|BMW|BN|BNPPARIBAS|BO|BOO|BOUTIQUE|BR|BRUSSELS|BS|BT|BUDAPEST|BUILD|BUILDERS|BUSINESS|BUZZ|BV|BW|BY|BZ|BZH|CA|CAB|CAL|CAMERA|CAMP|CANCERRESEARCH|CAPETOWN|CAPITAL|CARAVAN|CARDS|CARE|CAREER|CAREERS|CARTIER|CASA|CASH|CAT|CATERING|CC|CD|CENTER|CEO|CERN|CF|CG|CH|CHANNEL|CHEAP|CHRISTMAS|CHROME|CHURCH|CI|CITIC|CITY|CK|CL|CLAIMS|CLEANING|CLICK|CLINIC|CLOTHING|CLUB|CM|CN|CO|COACH|CODES|COFFEE|COLLEGE|COLOGNE|COM|COMMUNITY|COMPANY|COMPUTER|CONDOS|CONSTRUCTION|CONSULTING|CONTRACTORS|COOKING|COOL|COOP|COUNTRY|CR|CREDIT|CREDITCARD|CRICKET|CRS|CRUISES|CU|CUISINELLA|CV|CW|CX|CY|CYMRU|CZ|DAD|DANCE|DATING|DAY|DE|DEALS|DEGREE|DELIVERY|DEMOCRAT|DENTAL|DENTIST|DESI|DEV|DIAMONDS|DIET|DIGITAL|DIRECT|DIRECTORY|DISCOUNT|DJ|DK|DM|DNP|DO|DOCS|DOMAINS|DOOSAN|DURBAN|DVAG|DZ|EAT|EC|EDU|EDUCATION|EE|EG|EMAIL|EMERCK|ENERGY|ENGINEER|ENGINEERING|ENTERPRISES|EQUIPMENT|ER|ES|ESQ|ESTATE|ET|EU|EUROVISION|EUS|EVENTS|EVERBANK|EXCHANGE|EXPERT|EXPOSED|FAIL|FARM|FASHION|FEEDBACK|FI|FINANCE|FINANCIAL|FIRMDALE|FISH|FISHING|FITNESS|FJ|FK|FLIGHTS|FLORIST|FLSMIDTH|FLY|FM|FO|FOO|FORSALE|FOUNDATION|FR|FRL|FROGANS|FUND|FURNITURE|FUTBOL|GA|GAL|GALLERY|GARDEN|GB|GBIZ|GD|GE|GENT|GF|GG|GH|GI|GIFT|GIFTS|GIVES|GL|GLASS|GLE|GLOBAL|GLOBO|GM|GMAIL|GMO|GMX|GN|GOOGLE|GOP|GOV|GP|GQ|GR|GRAPHICS|GRATIS|GREEN|GRIPE|GS|GT|GU|GUIDE|GUITARS|GURU|GW|GY|HAMBURG|HAUS|HEALTHCARE|HELP|HERE|HIPHOP|HIV|HK|HM|HN|HOLDINGS|HOLIDAY|HOMES|HORSE|HOST|HOSTING|HOUSE|HOW|HR|HT|HU|IBM|ID|IE|IL|IM|IMMO|IMMOBILIEN|IN|INDUSTRIES|INFO|ING|INK|INSTITUTE|INSURE|INT|INTERNATIONAL|INVESTMENTS|IO|IQ|IR|IRISH|IS|IT|IWC|JE|JETZT|JM|JO|JOBS|JOBURG|JP|JUEGOS|KAUFEN|KE|KG|KH|KI|KIM|KITCHEN|KIWI|KM|KN|KOELN|KP|KR|KRD|KRED|KW|KY|KZ|LA|LACAIXA|LAND|LATROBE|LAWYER|LB|LC|LDS|LEASE|LEGAL|LGBT|LI|LIDL|LIFE|LIGHTING|LIMITED|LIMO|LINK|LK|LOANS|LONDON|LOTTO|LR|LS|LT|LTDA|LU|LUXE|LUXURY|LV|LY|MA|MADRID|MAISON|MANAGEMENT|MANGO|MARKET|MARKETING|MC|MD|ME|MEDIA|MEET|MELBOURNE|MEME|MEMORIAL|MENU|MG|MH|MIAMI|MIL|MINI|MK|ML|MM|MN|MO|MOBI|MODA|MOE|MONASH|MONEY|MORMON|MORTGAGE|MOSCOW|MOTORCYCLES|MOV|MP|MQ|MR|MS|MT|MU|MUSEUM|MV|MW|MX|MY|MZ|NA|NAGOYA|NAME|NAVY|NC|NE|NET|NETWORK|NEUSTAR|NEW|NEXUS|NF|NG|NGO|NHK|NI|NINJA|NL|NO|NP|NR|NRA|NRW|NU|NYC|NZ|OKINAWA|OM|ONG|ONL|OOO|ORG|ORGANIC|OSAKA|OTSUKA|OVH|PA|PARIS|PARTNERS|PARTS|PARTY|PE|PF|PG|PH|PHARMACY|PHOTO|PHOTOGRAPHY|PHOTOS|PHYSIO|PICS|PICTURES|PINK|PIZZA|PK|PL|PLACE|PLUMBING|PM|PN|POHL|POKER|PORN|POST|PR|PRAXI|PRESS|PRO|PROD|PRODUCTIONS|PROF|PROPERTIES|PROPERTY|PS|PT|PUB|PW|PY|QA|QPON|QUEBEC|RE|REALTOR|RECIPES|RED|REHAB|REISE|REISEN|REIT|REN|RENTALS|REPAIR|REPORT|REPUBLICAN|REST|RESTAURANT|REVIEWS|RICH|RIO|RIP|RO|ROCKS|RODEO|RS|RSVP|RU|RUHR|RW|RYUKYU|SA|SAARLAND|SAMSUNG|SARL|SB|SC|SCA|SCB|SCHMIDT|SCHULE|SCHWARZ|SCIENCE|SCOT|SD|SE|SERVICES|SEW|SEXY|SG|SH|SHIKSHA|SHOES|SI|SINGLES|SJ|SK|SKY|SL|SM|SN|SO|SOCIAL|SOFTWARE|SOHU|SOLAR|SOLUTIONS|SOY|SPACE|SPIEGEL|SR|ST|SU|SUPPLIES|SUPPLY|SUPPORT|SURF|SURGERY|SUZUKI|SV|SX|SY|SYDNEY|SYSTEMS|SZ|TAIPEI|TATAR|TATTOO|TAX|TC|TD|TECHNOLOGY|TEL|TF|TG|TH|TIENDA|TIPS|TIRES|TIROL|TJ|TK|TL|TM|TN|TO|TODAY|TOKYO|TOOLS|TOP|TOWN|TOYS|TP|TR|TRADE|TRAINING|TRAVEL|TRUST|TT|TUI|TV|TW|TZ|UA|UG|UK|UNIVERSITY|UNO|UOL|US|UY|UZ|VA|VACATIONS|VC|VE|VEGAS|VENTURES|VERSICHERUNG|VET|VG|VI|VIAJES|VILLAS|VISION|VLAANDEREN|VN|VODKA|VOTE|VOTING|VOTO|VOYAGE|VU|WALES|WANG|WATCH|WEBCAM|WEBSITE|WED|WEDDING|WF|WHOSWHO|WIEN|WIKI|WILLIAMHILL|WME|WORK|WORKS|WORLD|WS|WTC|WTF|XN--1QQW23A|XN--3BST00M|XN--3DS443G|XN--3E0B707E|XN--45BRJ9C|XN--45Q11C|XN--4GBRIM|XN--55QW42G|XN--55QX5D|XN--6FRZ82G|XN--6QQ986B3XL|XN--80ADXHKS|XN--80AO21A|XN--80ASEHDB|XN--80ASWG|XN--90A3AC|XN--C1AVG|XN--CG4BKI|XN--CLCHC0EA0B2G2A9GCD|XN--CZR694B|XN--CZRS0T|XN--CZRU2D|XN--D1ACJ3B|XN--D1ALF|XN--FIQ228C5HS|XN--FIQ64B|XN--FIQS8S|XN--FIQZ9S|XN--FLW351E|XN--FPCRJ9C3D|XN--FZC2C9E2C|XN--GECRJ9C|XN--H2BRJ9C|XN--HXT814E|XN--I1B6B1A6A2E|XN--IO0A7I|XN--J1AMH|XN--J6W193G|XN--KPRW13D|XN--KPRY57D|XN--KPUT3I|XN--L1ACC|XN--LGBBAT1AD8J|XN--MGB9AWBF|XN--MGBA3A4F16A|XN--MGBAAM7A8H|XN--MGBAB2BD|XN--MGBAYH7GPA|XN--MGBBH1A71E|XN--MGBC0A9AZCG|XN--MGBERP4A5D4AR|XN--MGBX4CD0AB|XN--NGBC5AZD|XN--NODE|XN--NQV7F|XN--NQV7FS00EMA|XN--O3CW4H|XN--OGBPF8FL|XN--P1ACF|XN--P1AI|XN--PGBS0DH|XN--Q9JYB4C|XN--QCKA1PMC|XN--RHQV96G|XN--S9BRJ9C|XN--SES554G|XN--UNUP4Y|XN--VERMGENSBERATER-CTB|XN--VERMGENSBERATUNG-PWB|XN--VHQUV|XN--WGBH1C|XN--WGBL6A|XN--XHQ521B|XN--XKC2AL3HYE2A|XN--XKC2DL3A5EE0H|XN--YFRO4I67O|XN--YGBI2AMMX|XN--ZFR164B|XXX|XYZ|YACHTS|YANDEX|YE|YOGA|YOKOHAMA|YOUTUBE|YT|ZA|ZIP|ZM|ZONE|ZW"

    country_list = r'%s' % '|'.join(x.name.encode('utf-8') for x in pycountry.countries)
    official_country_list = r'%s' % '|'.join(x.official_name.encode('utf-8') for x in pycountry.countries if hasattr(x, 'official_name'))
    country_list += '|' + official_country_list
    ipv4match = re.compile(r"\b((?:\d{1,3}\[?\.\]?){3}\d{1,3}(?:/[0-9][0-9])?)")
    hashmatch = re.compile(r"\b([a-fA-F0-9]{128}|[a-fA-F0-9]{32}|[a-fA-F0-9]{40}|[a-fA-F0-9]{64}|(?:\d+):(?:[a-z0-9+\/]{10,}):(?:[a-z0-9+\/]{5,})(?:\s\d+)?)\b", re.I)
    countrymatch = re.compile(r"\b(%s)\b" % country_list, re.I)
    cvematch = re.compile(r"CVE-\d{4}-\d+\b", re.I)
    domainmatch = re.compile(r"\b((?:[a-zA-Z0-9.\-\[\]]{3,})\[?\.\]?(?:%s))\b" % tldlist, re.I)
    tldmatch = re.compile(r"\b(%s)\b" % tldlist)
    urlmatch = re.compile(r"""((?:https?|ftp)://[^\s/$.?#].[^\s]*)""", re.I)
    filematch = re.compile(r"\b((?:[a-zA-Z]{2,255})\.([a-z]{1,4}))\b", re.I)
    filewhite = re.compile(r"\b(com|py)\b", re.I)
    registrymatch = re.compile(r"(HK(?:(?:LM|CR|CU|CC)|EY_.*?)\\.*)", re.I)
    emailmatch = re.compile(r"[a-z0-9!#$%&*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?", re.I)

    def __init__(self, report, config):
        self.report = report
        self.config = config

    def download_thing(self, report):
        response = urllib2.urlopen(report)
        return response.read()

    def save_to_storage(self, sha1, data):
        """
        Save raw report to HDFS
        """
        from hdfs import Client
        if self.config.no_save:
            return False

        host = 'http://{}:50070'.format(self.config.hdfs_host)
        path = self.config.storage
        client = Client(host, root=path)
        client.write(sha1, data=data, overwrite=True)
        return True

    def store_database(self, result):
        """
        Store a parsed report to ES
        """
        if self.config.disable_database:
            return False
        from elasticsearch import Elasticsearch
        es = Elasticsearch(self.config.es_host)
        es.index(index="sis", id=result.pop('id'), doc_type="pdf", body=result)
        return True

    def extract_iocs(self, output):
        result = {
            "content": {
                "text": output
            }
        }
        content_types = ['cve', 'domain', 'hash', 'filename', 'ipv4', 'registry', 'url', 'email', 'country']
        for name in content_types:
            if not name in result['content']:
                result['content'][name] = []

        for x in self.countrymatch.findall(output):
            if x[0].lower() in result['content']['country']:
                continue
            result['content']['country'].append(x[0].lower())

        for x in self.domainmatch.findall(output):
            if x.lower() in result['content']['domain']:
                continue
            result['content']['domain'].append(x.lower())

        for x in self.hashmatch.findall(output):
            if x.lower() in result['content']['hash']:
                continue
            result['content']['hash'].append(x.lower())

        for x in self.ipv4match.findall(output):
            if x in result['content']['ipv4']:
                continue
            result['content']['ipv4'].append(x)

        for x in self.cvematch.findall(output):
            if x.lower() in result['content']['cve']:
                continue
            result['content']['cve'].append(x.lower())

        for x in self.filematch.findall(output):
            if self.tldmatch.findall(x[1]) and not self.filewhite.findall(x[1]):
                continue
            if x[0].lower() in result['content']['filename']:
                continue
            result['content']['filename'].append(x[0].lower())

        for x in self.urlmatch.findall(output):
            if x in result['content']['url']:
                continue
            result['content']['url'].append(x)

        for x in self.registrymatch.findall(output):
            if x in result['content']['registry']:
                continue
            result['content']['registry'].append(x)

        for x in self.emailmatch.findall(output):
            if x.lower() in result['content']['email']:
                continue
            result['content']['email'].append(x.lower())

        [result['content'][name].sort() for name in content_types]
        return result

    def produce_md5(self, data):
        q = hashlib.md5(data)
        return q.hexdigest()

    def produce_sha1(self, data):
        q = hashlib.sha1(data)
        return q.hexdigest()



class HTMLReportparser(Parser):
    """
    Parser web page
    """
    def __init__(self, report, config):
        super(HTMLReportparser, self).__init__(report, config)
        self.name = urllib.unquote(report.split("/")[-1]).decode('utf8')
        self.result = {}
        self.data = self.download_thing(self.report)

    def process(self):
        soup = BeautifulSoup(self.data, "lxml")
        texts = soup.findAll(text=True)
        visible_texts = filter(self.visible, texts)        
        result = self.extract_iocs(" ".join(visible_texts))

        result['file'] = {}
        result['file']['parsed'] = datetime.now()
        result['file']['name'] = self.name
        result['file']['hash'] = {}
        result['file']['hash']['md5'] = self.produce_md5(self.data)
        result['file']['hash']['sha1'] = self.produce_sha1(self.data)
        result['file']['saved'] = self.save_to_storage(result['file']['hash']['sha1'], self.data)
        result['id'] = result['file']['hash']['sha1']
        self.result = result

    def visible(self, element):
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
            return False
        elif isinstance(element, Comment):
            return False
        return True


class PDFReportparser(Parser):
    """
    Parse PDFs
    """
    def __init__(self, report, config):
        super(PDFReportparser, self).__init__(report, config)
        self.name = urllib.unquote(report.split("/")[-1]).decode('utf8')
        self.result = {}
        if report.startswith("http"):
            self.fp = TemporaryFile()
            self.data = self.download_thing(self.report)
            self.fp.write(self.data)
        else:
            self.fp = open(report, 'rb')
            self.data = self.fp.read()

    def process(self):
        output = io.BytesIO()
        caching = True

        pagenos = set()
        rsrcmgr = PDFResourceManager(caching=caching)

        outfp = output
        maxpages = 0
        codec = "utf-8"

        device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.get_pages(self.fp, pagenos, maxpages=maxpages):
            interpreter.process_page(page)

        result = self.extract_iocs(output.getvalue())
        result['file'] = {}
        result['file']['parsed'] = datetime.now()
        result['file']['name'] = self.name
        result['file']['hash'] = {}
        result['file']['hash']['md5'] = self.produce_md5(self.data)
        result['file']['hash']['sha1'] = self.produce_sha1(self.data)
        result['file']['saved'] = self.save_to_storage(result['file']['hash']['sha1'], self.data)
        result['id'] = result['file']['hash']['sha1']

        self.result = result
        output.close()

