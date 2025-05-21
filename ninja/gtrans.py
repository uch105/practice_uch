import googletrans
from googletrans import Translator

lang_codes = {
    'af':'Africans',
    'sq':'Albanian',
    'am':'Amharic',
    'ar':'Arabic',
    'hy':'Armenian',
    'as':'Assamese',
    'ay':'Aymara',
    'az':'Ajarbaijani',
    'bm':'Bambara',
    'eu':'Basque',
    'be':'Belarusian',
    'bn':'Bengali',
    'bho':'Bhojpuri',
    'bs':'Bosnian',
    'bg':'Bulgarian',
    'ca':'Catalan',
    'ceb':'Cebuano',
    'zh':'Chinese',
    'zh-CN':'Chinese (Simplified)',
    'zh-TW':'Chinese (Traditional)',
    'co':'Corsican',
    'hr':'Croatian',
    'cs':'Czech',
    'da':'Danish',
    'dv':'Dhivehi',
    'doi':'Dogri',
    'nl':'Dutch',
    'en':'English',
    'eo':'Esperanto',
    'et':'Estonian',
    'ee':'Ewe',
    'fil':'Filipino (Tagalog)',
    'fi':'Finnish',
    'fr':'French',
    'fy':'Frisian',
    'gl':'Galician',
    'ka':'Georgian',
    'de':'German',
    'el':'Greek',
    'gn':'Guarani',
    'gu':'Gujarati',
    'ht':'Haitian Creole',
    'ha':'Hausa',
    'haw':'Hawaiian',
    'he':'Hebrew',
    'iw':'Hebrew*',
    'hi':'Hindi',
    'hmn':'Hmong',
    'hu':'Hungarian',
    'is':'Icelandic',
    'ig':'Igbo',
    'ilo':'Ilocano',
    'id':'Indonesian',
    'ga':'Irish',
    'it':'Italian',
    'ja':'Japanese',
    'jv':'Javanese',
    'jw':'Javanese.',
    'kn':'Kannada',
    'kk':'Kazakh',
    'km':'Khmer',
    'rw':'Kinyarwanda',
    'gom':'Konkani',
    'ko':'Korean',
    'kri':'Krio',
    'ku':'Kurdish',
    'ckb':'Kurdish (Sorani)',
    'ky':'Kyrgyz',
    'lo':'Lao',
    'la':'Latin',
    'lv':'Latvian',
    'ln':'Lingala',
    'lt':'Lithuanian',
    'lg':'Luganda',
    'lb':'Luxembourgish',
    'mk':'Macedonian',
    'mai':'Maithili',
    'mg':'Malagasy',
    'ms':'Malay',
    'ml':'Malayalam',
    'mt':'Maltese',
    'mi':'Maori',
    'mr':'Marathi',
    'mni-Mtei':'Meiteilon (Manipuri)',
    'lus':'Mizo',
    'mn':'Mongolian',
    'my':'Myanmar (Burmese)',
    'ne':'Nepali',
    'no':'Norwegian',
    'ny':'Nyanja (Chichewa)',
    'or':'Odia (Oriya)',
    'om':'Oromo',
    'ps':'Pashto',
    'fa':'Persian',
    'pl':'Polish',
    'pt':'Portuguese (Portugal, Brazil)',
    'pa':'Punjabi',
    'qu':'Quechua',
    'ro':'Romanian',
    'ru':'Russian',
    'sm':'Samoan',
    'sa':'Sanskrit',
    'gd':'Scots Gaelic',
    'nso':'Sepedi',
    'sr':'Serbian',
    'st':'Sesotho',
    'sn':'Shona',
    'sd':'Sindhi',
    'si':'Sinhala (Sinhalese)',
    'sk':'Slovak',
    'sl':'Slovenian',
    'so':'Somali',
    'es':'Spanish',
    'su':'Sundanese',
    'sw':'Swahili',
    'sv':'Swedish',
    'tl':'Tagalog (Filipino)',
    'tg':'Tajik',
    'ta':'Tamil',
    'tt':'Tatar',
    'te':'Telugu',
    'th':'Thai',
    'ti':'Tigrinya',
    'ts':'Tsonga',
    'tr':'Turkish',
    'tk':'Turkmen',
    'ak':'Twi (Akan)',
    'uk':'Ukrainian',
    'ur':'Urdu',
    'ug':'Uyghur',
    'uz':'Uzbek',
    'vi':'Vietnamese',
    'cy':'Welsh',
    'xh':'Xhosa',
    'yi':'Yiddish',
    'yo':'Yoruba',
    'zu':'Zulu',
}

def detect_lang(t):
    translator = Translator(service_urls=['translate.googleapis.com'])
    result = translator.detect(t)
    if result.confidence == 1:
        try:
            l = lang_codes[result.lang]
            return str(l)
        except:
            return "Couldn't detect"
    else:
        return "Not sure!"

def trans_lang(t):
    translator = Translator(service_urls=['translate.googleapis.com'])
    if detect_lang(t) == "English":
        return t
    else:
        result = translator.translate(t,dest="en")
        return result.text

def trans_langwsrc(t):
    translator = Translator(service_urls=['translate.googleapis.com'])
    if detect_lang(t) == "English":
        return t
    else:
        result = translator.translate(t,dest="en")
        return "[From " + detect_lang(t) + "] " + result.origin + "    =>    " + result.text

text = 'Der Himmel ist blau und ich mag Bananen'
print(detect_lang(text))
print(trans_lang(text))
print(trans_langwsrc(text))