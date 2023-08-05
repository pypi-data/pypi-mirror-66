import re

class CountryList():
    """ CountryList class for searching through a list of mappings 
    between DJII region codes and ISO Alpha 2 country codes to 
    convert the passed inputs into the appropriate format requested.
    
    Attributes:
        country_list (list of lists) a list of country code lists
    
    """
    def __init__(self):
        self.country_list = []
    

    def get_country_name(self, query):
        """Function to search through self.country_list to return the 
        country name that matches the search query.
        
        Args:
            query (str): search parameter (DJII RC or ISO Alpha 2)
        
        Returns:
            country_name (str): country returned from running search

        """

        try:
            if (re.match('^[A-Z]{2}$', query) and query != 'UK'):
                #Query is ISO Alpha 2 - 'UK' is a two character DJII RC
                return self.search_list(self.country_list, 2, query)[0]

            else:
                #Query is DJII RC
                return self.search_list(self.country_list, 1, query)[0]

        except Exception as e:
            print(f'File parsing unsuccessful: {str(e)}')
    

    def get_djii_rc(self, query):
        """Function to search through self.country_list to return the 
        DJII region code that matches the search query.
        
        Args:
            query (str): search parameter (ISO Alpha 2 or country name)
        
        Returns:
            djii_rc (str): DJII region code returned from running search

        """

        try:
            if (re.match('^[A-Z]{2}$', query) and query != 'UK'):
                #Query is ISO Alpha 2 - 'UK' is a two character DJII RC
                return self.search_list(self.country_list, 2, query)[1]

            else:
                #Query is country name
                return self.search_list(self.country_list, 0, query)[1]

        except Exception as e:
            print(f'File parsing unsuccessful: {str(e)}')


    def get_iso_alpha_2(self, query):
        """Function to search through self.country_list to return the 
        ISO Alpha 2 country code that matches the search query.
        
        Args:
            query (str): search parameter (DJII RC or country name)
        
        Returns:
            iso_alpha_2 (str): ISO Alpha 2 code returned from running search

        """

        try:
            if (re.match('^[A-Z]{2,6}$', query)):
                #Query is DJII RC
                return self.search_list(self.country_list, 1, query)[2]

            else:
                #Query is country name
                return self.search_list(self.country_list, 0, query)[2]

        except Exception as e:
            print(f'File parsing unsuccessful: {str(e)}')
    

    def search_list(self, item_list, idx, query):
        """Function to search through a list of lists to return the 
        matching list containing the search query.
        
        Args:
            item_list (list of lists): list to be searched against
            idx (int): index corresponding to input type as per below
                        0 = country name
                        1 = DJII region code
                        2 = ISO Alpha 2 code
            query (str): search parameter
        
        Returns:
            item (list of str): list returned from running search

        """

        for item in item_list:
            if item[idx] == query:
                return item


    def create_country_list(self):
        """Function to create a a list of lists to map country names to 
        DJII region codes and ISO Alpha 2 country codes.
        
        Args:
            None
        
        Returns:
            country_list (list of lists): a list of country code lists

        """

        self.country_list.append(["Afghanistan","AFGH","AF"])
        self.country_list.append(["Albania","ALB","AL"])
        self.country_list.append(["Algeria","ALG","DZ"])
        self.country_list.append(["American Samoa","AMSAM","AS"])
        self.country_list.append(["Andorra","ANDO","AD"])
        self.country_list.append(["Angola","ANGOL","AO"])
        self.country_list.append(["Anguilla","ANGUIL","AI"])
        self.country_list.append(["Antarctica","AARCT","AQ"])
        self.country_list.append(["Antigua and Barbuda","ANTA","AG"])
        self.country_list.append(["Argentina","ARG","AR"])
        self.country_list.append(["Armenia","ARMEN","AM"])
        self.country_list.append(["Aruba","ARUBA","AW"])
        self.country_list.append(["Australia","AUSTR","AU"])
        self.country_list.append(["Austria","AUST","AT"])
        self.country_list.append(["Azerbaijan","AZERB","AZ"])
        self.country_list.append(["Bahamas","BAH","BS"])
        self.country_list.append(["Bahrain","BAHRN","BH"])
        self.country_list.append(["Bangladesh","BANDH","BD"])
        self.country_list.append(["Barbados","BARB","BB"])
        self.country_list.append(["Belarus","BYELRS","BY"])
        self.country_list.append(["Belgium","BELG","BE"])
        self.country_list.append(["Belize","BELZ","BZ"])
        self.country_list.append(["Benin","BENIN","BJ"])
        self.country_list.append(["Bermuda","BERM","BM"])
        self.country_list.append(["Bhutan","BHUTAN","BT"])
        self.country_list.append(["Bolivia","BOL","BO"])
        self.country_list.append(["Bosnia and Herzegovina","BSHZG","BA"])
        self.country_list.append(["Botswana","BOTS","BW"])
        self.country_list.append(["Bouvet Island","BOUV","BV"])
        self.country_list.append(["Brazil","BRAZ","BR"])
        self.country_list.append(["British Indian Ocean Territory","BIOT","IO"])
        self.country_list.append(["British Virgin Islands","BVI","VG"])
        self.country_list.append(["Brunei","BRUNEI","BN"])
        self.country_list.append(["Bulgaria","BUL","BG"])
        self.country_list.append(["Burkina Faso","UPVOLA","BF"])
        self.country_list.append(["Burundi","BURUN","BI"])
        self.country_list.append(["Cambodia","KAMPA","KH"])
        self.country_list.append(["Cameroon","CAMER","CM"])
        self.country_list.append(["Canada","CANA","CA"])
        self.country_list.append(["Cape Verde","CVI","CV"])
        self.country_list.append(["Cayman Islands","CAYI","KY"])
        self.country_list.append(["Central African Republic","CAFR","CF"])
        self.country_list.append(["Chad","CHAD","TD"])
        self.country_list.append(["Chile","CHIL","CL"])
        self.country_list.append(["China","CHINA","CN"])
        self.country_list.append(["Christmas Island","CHR","CX"])
        self.country_list.append(["Cocos (Keeling) Islands","COCOS","CC"])
        self.country_list.append(["Colombia","COL","CO"])
        self.country_list.append(["Comoros","COMOR","KM"])
        self.country_list.append(["Congo Republic","CONGO","CG"])
        self.country_list.append(["Cook Islands","COOKIS","CK"])
        self.country_list.append(["Costa Rica","COSR","CR"])
        self.country_list.append(["Cote d'Ivoire","ICST","CI"])
        self.country_list.append(["Croatia","CRTIA","HR"])
        self.country_list.append(["Cuba","CUBA","CU"])
        self.country_list.append(["Cyprus","CYPR","CY"])
        self.country_list.append(["Czech Republic","CZREP","CZ"])
        self.country_list.append(["Democratic Republic of the Congo","ZAIRE","CD"])
        self.country_list.append(["Denmark","DEN","DK"])
        self.country_list.append(["Djibouti","TAI","DJ"])
        self.country_list.append(["Dominica","DOMA","DM"])
        self.country_list.append(["Dominican Republic","DOMR","DO"])
        self.country_list.append(["Timor Leste","TIMOR","TL"])
        self.country_list.append(["Ecuador","ECU","EC"])
        self.country_list.append(["Egypt","EGYPT","EG"])
        self.country_list.append(["El Salvador","ELSAL","SV"])
        self.country_list.append(["Equatorial Guinea","EQGNA","GQ"])
        self.country_list.append(["Eritrea","ERTRA","ER"])
        self.country_list.append(["Estonia","ESTNIA","EE"])
        self.country_list.append(["Ethiopia","ETHPA","ET"])
        self.country_list.append(["Faroe Islands","FAEROE","FO"])
        self.country_list.append(["Falkland Islands","FALK","FK"])
        self.country_list.append(["Fiji","FIJI","FJ"])
        self.country_list.append(["Finland","FIN","FI"])
        self.country_list.append(["France","FRA","FR"])
        self.country_list.append(["French Guiana","FGNA","GF"])
        self.country_list.append(["French Polynesia","FPOLY","PF"])
        self.country_list.append(["Gabon","GABON","GA"])
        self.country_list.append(["Gambia","GAMB","GM"])
        self.country_list.append(["Georgia","GRGIA","GE"])
        self.country_list.append(["Germany","GFR","DE"])
        self.country_list.append(["Ghana","GHANA","GH"])
        self.country_list.append(["Gibraltar","GIB","GI"])
        self.country_list.append(["Greece","GREECE","GR"])
        self.country_list.append(["Greenland","GREENL","GL"])
        self.country_list.append(["Grenada","GREN","GD"])
        self.country_list.append(["Guadeloupe","GUAD","GP"])
        self.country_list.append(["Guam","GUAM","GU"])
        self.country_list.append(["Guatemala","GUAT","GT"])
        self.country_list.append(["Guinea","GUREP","GN"])
        self.country_list.append(["Guinea-Bissau","GUBI","GW"])
        self.country_list.append(["Guyana","GUY","GY"])
        self.country_list.append(["Haiti","HAIT","HT"])
        self.country_list.append(["Heard and McDonald Islands","HEARD","HM"])
        self.country_list.append(["Honduras","HON","HN"])
        self.country_list.append(["Hong Kong","HKONG","HK"])
        self.country_list.append(["Hungary","HUNG","HU"])
        self.country_list.append(["Iceland","ICEL","IS"])
        self.country_list.append(["India","INDIA","IN"])
        self.country_list.append(["Indonesia","INDON","ID"])
        self.country_list.append(["Iran","IRAN","IR"])
        self.country_list.append(["Iraq","IRAQ","IQ"])
        self.country_list.append(["Ireland","IRE","IE"])
        self.country_list.append(["Israel","ISRAEL","IL"])
        self.country_list.append(["Italy","ITALY","IT"])
        self.country_list.append(["Jamaica","JAMA","JM"])
        self.country_list.append(["Japan","JAP","JP"])
        self.country_list.append(["Jordan","JORDAN","JO"])
        self.country_list.append(["Kazakhstan","KAZK","KZ"])
        self.country_list.append(["Kenya","KENYA","KE"])
        self.country_list.append(["Kiribati","KIRB","KI"])
        self.country_list.append(["Kuwait","KUWAIT","KW"])
        self.country_list.append(["Kyrgyzstan","KIRGH","KG"])
        self.country_list.append(["Laos","LAOS","LA"])
        self.country_list.append(["Latvia","LATV","LV"])
        self.country_list.append(["Lebanon","LEBAN","LB"])
        self.country_list.append(["Lesotho","LESOT","LS"])
        self.country_list.append(["Liberia","LIBER","LR"])
        self.country_list.append(["Libya","LIBYA","LY"])
        self.country_list.append(["Liechtenstein","LIECHT","LI"])
        self.country_list.append(["Lithuania","LITH","LT"])
        self.country_list.append(["Luxembourg","LUX","LU"])
        self.country_list.append(["Macau","MACAO","MO"])
        self.country_list.append(["Macedonia","MCDNIA","MK"])
        self.country_list.append(["Madagascar","MALAG","MG"])
        self.country_list.append(["Malawi","MALAW","MW"])
        self.country_list.append(["Malaysia","MALAY","MY"])
        self.country_list.append(["Maldives","MALDR","MV"])
        self.country_list.append(["Mali","MALI","ML"])
        self.country_list.append(["Malta","MALTA","MT"])
        self.country_list.append(["Marshall Islands","MAH","MH"])
        self.country_list.append(["Martinique","MARQ","MQ"])
        self.country_list.append(["Mauritania","MAURTN","MR"])
        self.country_list.append(["Mauritius","MAURTS","MU"])
        self.country_list.append(["Mayotte","MAYOT","YT"])
        self.country_list.append(["Mexico","MEX","MX"])
        self.country_list.append(["Micronesia","FESMIC","FM"])
        self.country_list.append(["Moldova","MOLDV","MD"])
        self.country_list.append(["Monaco","MONAC","MC"])
        self.country_list.append(["Mongolia","MONGLA","MN"])
        self.country_list.append(["Montserrat","MONT","MS"])
        self.country_list.append(["Morocco","MOROC","MA"])
        self.country_list.append(["Mozambique","MOZAM","MZ"])
        self.country_list.append(["Myanmar","BURMA","MM"])
        self.country_list.append(["Namibia","NAMIB","NA"])
        self.country_list.append(["Nauru","NAURU","NR"])
        self.country_list.append(["Nepal","NEPAL","NP"])
        self.country_list.append(["Netherlands","NETH","NL"])
        self.country_list.append(["Curacao","NANT","CW"])
        self.country_list.append(["New Caledonia","NEWCAL","NC"])
        self.country_list.append(["New Zealand","NZ","NZ"])
        self.country_list.append(["Nicaragua","NICG","NI"])
        self.country_list.append(["Niger","NIGER","NE"])
        self.country_list.append(["Nigeria","NIGEA","NG"])
        self.country_list.append(["Niue","NIUE","NU"])
        self.country_list.append(["Norfolk Island","NORFIS","NF"])
        self.country_list.append(["North Korea","NKOREA","KP"])
        self.country_list.append(["Northern Mariana Islands","NOMARI","MP"])
        self.country_list.append(["Norway","NORW","NO"])
        self.country_list.append(["Oman","OMAN","OM"])
        self.country_list.append(["Pakistan","PAKIS","PK"])
        self.country_list.append(["Palau","PALAU","PW"])
        self.country_list.append(["Palestine","PALEST","PS"])
        self.country_list.append(["Panama","PANA","PA"])
        self.country_list.append(["Papua New Guinea","PAPNG","PG"])
        self.country_list.append(["Paraguay","PARA","PY"])
        self.country_list.append(["Peru","PERU","PE"])
        self.country_list.append(["Philippines","PHLNS","PH"])
        self.country_list.append(["Pitcairn","PITCIS","PN"])
        self.country_list.append(["Poland","POL","PL"])
        self.country_list.append(["Portugal","PORL","PT"])
        self.country_list.append(["Puerto Rico","PURI","PR"])
        self.country_list.append(["Qatar","QATAR","QA"])
        self.country_list.append(["Reunion","REUNI","RE"])
        self.country_list.append(["Romania","ROM","RO"])
        self.country_list.append(["Russia","RUSS","RU"])
        self.country_list.append(["Rwanda","RWANDA","RW"])
        self.country_list.append(["Saint Lucia","SLUC","LC"])
        self.country_list.append(["Samoa","WSOMOA","WS"])
        self.country_list.append(["San Marino","SMARNO","SM"])
        self.country_list.append(["Sao Tome and Principe","PST","ST"])
        self.country_list.append(["Saudi Arabia","SAARAB","SA"])
        self.country_list.append(["Senegal","SENEG","SN"])
        self.country_list.append(["Seychelles","SEYCH","SC"])
        self.country_list.append(["Sierra Leone","SILEN","SL"])
        self.country_list.append(["Singapore","SINGP","SG"])
        self.country_list.append(["Slovakia","SLVAK","SK"])
        self.country_list.append(["Slovenia","SLVNIA","SI"])
        self.country_list.append(["Solomon Islands","SOLIL","SB"])
        self.country_list.append(["Somalia","SOMAL","SO"])
        self.country_list.append(["South Africa","SAFR","ZA"])
        self.country_list.append(["South Georgia and South Sandwich Islands","SGSSI","GS"])
        self.country_list.append(["South Korea","SKOREA","KR"])
        self.country_list.append(["Spain","SPAIN","ES"])
        self.country_list.append(["Sri Lanka","SRILAN","LK"])
        self.country_list.append(["St. Helena","STHEL","SH"])
        self.country_list.append(["St. Kitts and Nevis","SKIT","KN"])
        self.country_list.append(["St. Martin","STMART","MF"])
        self.country_list.append(["St. Pierre and Miquelon","STPM","PM"])
        self.country_list.append(["St. Vincent and the Grenadines","SVIN","VC"])
        self.country_list.append(["Sudan","SUDAN","SD"])
        self.country_list.append(["Suriname","SURM","SR"])
        self.country_list.append(["Svalbard and Jan Mayen Islands","SVALB","SJ"])
        self.country_list.append(["Swaziland","SWAZD","SZ"])
        self.country_list.append(["Sweden","SWED","SE"])
        self.country_list.append(["Switzerland","SWITZ","CH"])
        self.country_list.append(["Syria","SYRIA","SY"])
        self.country_list.append(["Taiwan","TAIWAN","TW"])
        self.country_list.append(["Tajikistan","TADZK","TJ"])
        self.country_list.append(["Tanzania","TANZA","TZ"])
        self.country_list.append(["Thailand","THAIL","TH"])
        self.country_list.append(["Togo","TOGO","TG"])
        self.country_list.append(["Tokelau","TOKLAU","TK"])
        self.country_list.append(["Tonga","TONGA","TO"])
        self.country_list.append(["Trinidad and Tobago","TRTO","TT"])
        self.country_list.append(["Tunisia","TUNIS","TN"])
        self.country_list.append(["Turkey","TURK","TR"])
        self.country_list.append(["Turkmenistan","TURKM","TM"])
        self.country_list.append(["Turks and Caicos Islands","TCAI","TC"])
        self.country_list.append(["Tuvalu","TVLU","TV"])
        self.country_list.append(["Uganda","UGANDA","UG"])
        self.country_list.append(["Ukraine","UKRN","UA"])
        self.country_list.append(["United Arab Emirates","UAE","AE"])
        self.country_list.append(["United Kingdom","UK","GB"])
        self.country_list.append(["United States","USA","US"])
        self.country_list.append(["Uruguay","URU","UY"])
        self.country_list.append(["Uzbekistan","UZBK","UZ"])
        self.country_list.append(["Vanuatu","VANU","VU"])
        self.country_list.append(["Vatican City","VCAN","VA"])
        self.country_list.append(["Venezuela","VEN","VE"])
        self.country_list.append(["Vietnam","VIETN","VN"])
        self.country_list.append(["Wallis and Futuna Islands","WALLIS","WF"])
        self.country_list.append(["Western Sahara","SPSAH","EH"])
        self.country_list.append(["Yemen","YEMAR","YE"])
        self.country_list.append(["Serbia","YUG","RS"])
        self.country_list.append(["Zambia","ZAMBIA","ZM"])
        self.country_list.append(["Zimbabwe","ZIMBAB","ZW"])
        self.country_list.append(["Montenegro","MNTNG","ME"])
        self.country_list.append(["U.S. Virgin Islands","VI","VI"])
        self.country_list.append(["Saint Barthelemy","SBRTHY","BL"])
        self.country_list.append(["Guernsey","GUERN","GG"])
        self.country_list.append(["Isle of Man","ISLEOM","IM"])
        self.country_list.append(["Jersey","JERSEY","JE"])
        self.country_list.append(["St. Maarten","SINTMA","SX"])
        self.country_list.append(["South Sudan","SOUSUD","SS"])

        return self.country_list