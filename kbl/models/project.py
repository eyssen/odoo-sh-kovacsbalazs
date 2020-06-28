# -*- coding: utf-8 -*-
from odoo import api, fields, models
from werkzeug.urls import url_encode

import logging
_logger = logging.getLogger(__name__)





CONTROL = {
    ('isnot', 'Nincsen'),
    ('builtinprocess', 'Folyamatba épített'),
    ('followup', 'Utóellenőrzés'),
}

KSTATE = {
    ('preparation', 'Előkészítés alatt'),
    ('progress', 'Folyamatban'),
    ('closed1', 'Lezárt 1'),
    ('closed2', 'Lezárt 2'),
}

PROCEDURE = {
    ('union', 'Uniós'),
    ('national', 'Nemzeti'),
}

WAGE_VERSION = {
    ('1_1', 'Egyszakaszos, 1. verzió'),
    ('1_2', 'Egyszakaszos, 2. verzió'),
    ('1_3', 'Egyszakaszos, 3. verzió'),
}

KFF_TASK = {
    ('quality', 'Minőségellenőrzés'),
    ('regularity', 'Szabályossági ellenőrzés'),
    ('contractmodification', 'Szerződésmódosítás ellenőrzés'),
    ('acquisition', 'Beszerzés'),
}

PR_TASK = {
    ('professional', 'Szakmai cikk'),
    ('other', 'Egyéb cikk'),
    ('photovideo', 'Kép/Videó és komment'),
}

KEF = {
    ('kef', 'KEF-es eljárás'),
    ('nokef', 'Nem KEF-es eljárás'),
}

WAGE = {
    # 1 szakaszos
    ('wage1', 'Az eljárás előkészítése és kiírása / A Kbt. 115. §-a szerinti, vagy hirdetmény nélküli tárgyalásos eljárás esetén (építési beruházás)'),
    ('wage2', 'Az eljárás lefolytatásának első részteljesítése / A Kbt. 115. §-a szerinti, vagy hirdetmény nélküli tárgyalásos eljárás esetén (építési beruházás)'),
    ('wage3', 'Az eljárás lefolytatásának végteljesítése / A Kbt. 115. §-a szerinti, vagy hirdetmény nélküli tárgyalásos eljárás esetén (építési beruházás)'),
    ('wage4', 'Az eljárás lezárása / A Kbt. 115. §-a szerinti, vagy hirdetmény nélküli tárgyalásos eljárás esetén (építési beruházás)'),
    ('wage5', 'Az eljárás előkészítése és kiírása / Összefoglaló tájékoztatással, vagy hirdetmény közzétételével induló eljárás esetén'),
    ('wage6', 'Az eljárás lefolytatásának első részteljesítése / Összefoglaló tájékoztatással, vagy hirdetmény közzétételével induló eljárás esetén'),
    ('wage7', 'Az eljárás lefolytatásának végteljesítése / Összefoglaló tájékoztatással, vagy hirdetmény közzétételével induló eljárás esetén'),
    ('wage8', 'Az eljárás lezárása / Összefoglaló tájékoztatással, vagy hirdetmény közzétételével induló eljárás esetén'),
    ('wage9', 'Az eljárás előkészítése és kiírása / Keretmegállapodásos eljárás második része esetén'),
    ('wage10', 'Az eljárás lefolytatásának első részteljesítése / Keretmegállapodásos eljárás második része esetén'),
    ('wage11', 'Az eljárás lefolytatásának végteljesítése / Keretmegállapodásos eljárás második része esetén'),
    ('wage12', 'Az eljárás lezárása / Keretmegállapodásos eljárás második része esetén'),
    ('wage13', 'Az eljárás előkészítése és kiírása / Amennyiben közbeszerzési részek vannak, közbeszerzési részenként, ha nagyobb mint 1'),
    ('wage14', 'Az eljárás lefolytatásának első részteljesítése / Amennyiben közbeszerzési részek vannak, közbeszerzési részenként, ha nagyobb mint 1'),
    ('wage15', 'Az eljárás lefolytatásának végteljesítése / Amennyiben közbeszerzési részek vannak, közbeszerzési részenként, ha nagyobb mint 1'),
    ('wage16', 'Az eljárás lezárása / Amennyiben közbeszerzési részek vannak, közbeszerzési részenként, ha nagyobb mint 1'),
    ('wage17', 'Az eljárás előkészítése és kiírása / Uniós eljárásrend alkalmazása esetén (tehát ha az eljárásrend uniós és nem a becsült érték)'),
    ('wage18', 'Az eljárás lefolytatásának első részteljesítése / Uniós eljárásrend alkalmazása esetén (tehát ha az eljárásrend uniós és nem a becsült érték)'),
    ('wage19', 'Az eljárás lefolytatásának végteljesítése / Uniós eljárásrend alkalmazása esetén (tehát ha az eljárásrend uniós és nem a becsült érték)'),
    ('wage20', 'Az eljárás lezárása / Uniós eljárásrend alkalmazása esetén (tehát ha az eljárásrend uniós és nem a becsült érték)'),
    ('wage21', 'Az eljárás előkészítése és kiírása / Ha a közbeszerzési eljárás jogszabályban előírt utóellenőrzés hatálya alá tartozik'),
    ('wage22', 'Az eljárás lefolytatásának első részteljesítése / Ha a közbeszerzési eljárás jogszabályban előírt utóellenőrzés hatálya alá tartozik'),
    ('wage23', 'Az eljárás lefolytatásának végteljesítése / Ha a közbeszerzési eljárás jogszabályban előírt utóellenőrzés hatálya alá tartozik'),
    ('wage24', 'Az eljárás lezárása / Ha a közbeszerzési eljárás jogszabályban előírt utóellenőrzés hatálya alá tartozik'),
    ('wage25', 'Folyamatba épített ellenőrzés megindításra került / Ha a közbeszerzési eljárás jogszabályban előírt folyamatba épített ellenőrzés hatálya alá tartozik'),
    ('wage26', 'Az eljárás lefolytatásának első részteljesítése / Ha a közbeszerzési eljárás jogszabályban előírt folyamatba épített ellenőrzés hatálya alá tartozik'),
    ('wage27', 'Az eljárás lefolytatásának végteljesítése / Ha a közbeszerzési eljárás jogszabályban előírt folyamatba épített ellenőrzés hatálya alá tartozik'),
    ('wage28', 'Az eljárás lezárása / Ha a közbeszerzési eljárás jogszabályban előírt folyamatba épített ellenőrzés hatálya alá tartozik'),
    ('wage29', 'Az eljárás lefolytatásának végteljesítése / Az eljárásban bírált ajánlatok számának megfelelően (ajánlatonként)'),
    ('wage74', 'Az eljárás lefolytatásának végteljesítése / Az eljárásban értékelt ajánlatok számának megfelelően (ajánlatonként)'),
    ('wage30', 'Megtartott tárgyalás / Megtartott tárgyalásonként (ha egy fordulóban külön-külön tárgyal az ajánlatkérő, akkor külön-külön számítandó)'),
    # 2 szakaszos
    ('wage31', 'Az eljárás előkészítése és kiírása / Összefoglaló tájékoztatással, vagy hirdetmény közzétételével induló eljárás esetén'),
    ('wage32', 'A részvételi szakasz lefolytatásának első részteljesítése / Összefoglaló tájékoztatással, vagy hirdetmény közzétételével induló eljárás esetén'),
    ('wage33', 'A részvételi szakasz lefolytatásának végteljesítése / Összefoglaló tájékoztatással, vagy hirdetmény közzétételével induló eljárás esetén'),
    ('wage34', 'Az ajánlattételi szakasz lefolytatásának első részteljesítése / Összefoglaló tájékoztatással, vagy hirdetmény közzétételével induló eljárás esetén'),
    ('wage35', 'Az eljárás lefolytatásának végteljesítése / Összefoglaló tájékoztatással, vagy hirdetmény közzétételével induló eljárás esetén'),
    ('wage36', 'Az eljárás lezárása / Összefoglaló tájékoztatással, vagy hirdetmény közzétételével induló eljárás esetén'),
    ('wage37', 'Az eljárás előkészítése és kiírása / Amennyiben közbeszerzési részek vannak, közbeszerzési részenként'),
    ('wage38', 'A részvételi szakasz lefolytatásának első részteljesítése / Amennyiben közbeszerzési részek vannak, közbeszerzési részenként'),
    ('wage39', 'A részvételi szakasz lefolytatásának végteljesítése / Amennyiben közbeszerzési részek vannak, közbeszerzési részenként'),
    ('wage40', 'Az ajánlattételi szakasz lefolytatásának első részteljesítése / Amennyiben közbeszerzési részek vannak, közbeszerzési részenként'),
    ('wage41', 'Az eljárás lefolytatásának végteljesítése / Amennyiben közbeszerzési részek vannak, közbeszerzési részenként'),
    ('wage42', 'Az eljárás lezárása / Amennyiben közbeszerzési részek vannak, közbeszerzési részenként'),
    ('wage43', 'Az eljárás előkészítése és kiírása / Uniós eljárásrend alkalmazása esetén (tehát ha az eljárásrend uniós és nem a becsült érték)'),
    ('wage44', 'A részvételi szakasz lefolytatásának első részteljesítése / Uniós eljárásrend alkalmazása esetén (tehát ha az eljárásrend uniós és nem a becsült érték)'),
    ('wage45', 'A részvételi szakasz lefolytatásának végteljesítése / Uniós eljárásrend alkalmazása esetén (tehát ha az eljárásrend uniós és nem a becsült érték)'),
    ('wage46', 'Az ajánlattételi szakasz lefolytatásának első részteljesítése / Uniós eljárásrend alkalmazása esetén (tehát ha az eljárásrend uniós és nem a becsült érték)'),
    ('wage47', 'Az eljárás lefolytatásának végteljesítése / Uniós eljárásrend alkalmazása esetén (tehát ha az eljárásrend uniós és nem a becsült érték)'),
    ('wage48', 'Az eljárás lezárása / Uniós eljárásrend alkalmazása esetén (tehát ha az eljárásrend uniós és nem a becsült érték)'),
    ('wage49', 'Az eljárás előkészítése és kiírása / Ha a közbeszerzési eljárás jogszabályban előírt utóellenőrzés hatálya alá tartozik'),
    ('wage50', 'A részvételi szakasz lefolytatásának első részteljesítése / Ha a közbeszerzési eljárás jogszabályban előírt utóellenőrzés hatálya alá tartozik'),
    ('wage51', 'A részvételi szakasz lefolytatásának végteljesítése / Ha a közbeszerzési eljárás jogszabályban előírt utóellenőrzés hatálya alá tartozik'),
    ('wage52', 'Az ajánlattételi szakasz lefolytatásának első részteljesítése / Ha a közbeszerzési eljárás jogszabályban előírt utóellenőrzés hatálya alá tartozik'),
    ('wage53', 'Az eljárás lefolytatásának végteljesítése / Ha a közbeszerzési eljárás jogszabályban előírt utóellenőrzés hatálya alá tartozik'),
    ('wage54', 'Az eljárás lezárása / Ha a közbeszerzési eljárás jogszabályban előírt utóellenőrzés hatálya alá tartozik'),
    ('wage55', 'Folyamatba épített ellenőrzés megindításra került / Ha a közbeszerzési eljárás jogszabályban előírt folyamatba épített ellenőrzés hatálya alá tartozik'),
    ('wage56', 'A részvételi szakasz lefolytatásának első részteljesítése / Ha a közbeszerzési eljárás jogszabályban előírt folyamatba épített ellenőrzés hatálya alá tartozik'),
    ('wage57', 'A részvételi szakasz lefolytatásának végteljesítése / Ha a közbeszerzési eljárás jogszabályban előírt folyamatba épített ellenőrzés hatálya alá tartozik'),
    ('wage58', 'Az ajánlattételi szakasz lefolytatásának első részteljesítése / Ha a közbeszerzési eljárás jogszabályban előírt folyamatba épített ellenőrzés hatálya alá tartozik'),
    ('wage59', 'Az eljárás lefolytatásának végteljesítése / Ha a közbeszerzési eljárás jogszabályban előírt folyamatba épített ellenőrzés hatálya alá tartozik'),
    ('wage60', 'Az eljárás lezárása / Ha a közbeszerzési eljárás jogszabályban előírt folyamatba épített ellenőrzés hatálya alá tartozik'),
    ('wage61', 'A részvételi szakasz lefolytatásának végteljesítése / Az eljárásban benyújtott részvételre jelentkezések számának megfelelően (jelentkezésenként)'),
    ('wage62', 'Az eljárás lefolytatásának végteljesítése / Az eljárásban bírált ajánlatok számának megfelelően (ajánlatonként)'),
    ('wage75', 'Az eljárás lefolytatásának végteljesítése / Az eljárásban értékelt ajánlatok számának megfelelően (ajánlatonként)'),
    ('wage63', 'Megtartott tárgyalás / Megtartott tárgyalásonként (ha egy fordulóban külön-külön tárgyal az ajánlatkérő, akkor külön-külön számítandó)'),
    # kff
    ('wage64', 'KFF minőség-ellenőrzés / A "Feladat" mezőben a "Minőség-ellenőrzés" van kiválasztva ÉS a "Feladat lezárulása" mező kitöltésre kerül a dátummal'),
    ('wage65', 'KFF szabályossági ellenőrzés / A "Feladat" mezőben a "Szabályossági ellenőrzés" van kiválasztva ÉS a "Feladat lezárulása" mező kitöltésre kerül a dátummal'),
    ('wage66', 'KFF szerződésmódosítás / A "Feladat" mezőben a "Szerződésmódosítás ellenőrzés" van kiválasztva ÉS a "Feladat lezárulása" mező kitöltésre kerül a dátummal'),
    # szerződésmódosítás
    ('wage67', 'Szerződésmódosítás / A "Tájékoztató feladva" kitöltésre került ÉS az "Aláírt ügyfél teljesítésigazolás beérkezett" mező kitöltésre kerül a dátummal'),
    # versenyeztetés
    ('wage68', 'Versenyeztetés / Az "Az iratok átadásra kerültek" kitöltésre került ÉS az "Aláírt ügyfél teljesítésigazolás beérkezett" mező kitöltésre kerül a dátummal'),
    # PR, marketing
    ('wage69', 'PR, marketing / Szakmai cikk'),
    ('wage70', 'PR, marketing / Egyéb cikk'),
    ('wage71', 'PR, marketing / Kép/Videó és komment'),
    # Óradíjas és Irodavezetői óradíjas
    ('wage72', 'Óradíj / Óradíjas feladatok'),
    ('wage73', 'Óradíj / Irodavezetői óradíjas feladatok'),
    ('wage82', 'Óradíj / Eljárásokkal kapcsolatos óradíj'),
    # dku
    ('wage76', 'DKÜ-s ellennőrzés / KEF-es eljárás minőség-ellenőrzési szakasz (KEF / NEM KEF mezőnél a „KEF-es eljárás” opció kerül kiválasztásra, a „Feladat” mezőnél pedig a „minőség-ellenőrzés”)'),
    ('wage77', 'DKÜ-s ellennőrzés / KEF-es eljárás szabályossági ellenőrzési szakasz (KEF / NEM KEF mezőnél a „KEF-es eljárás” opció kerül kiválasztásra, a „Feladat” mezőnél pedig a „szabályossági ellenőrzés”)'),
    ('wage78', 'DKÜ-s ellennőrzés / Nem KEF-es eljárás minőség-ellenőrzési szakasz (KEF / NEM KEF mezőnél a „Nem KEF-es eljárás” opció kerül kiválasztásra, a „Feladat” mezőnél pedig a „minőség-ellenőrzés”)'),
    ('wage79', 'DKÜ-s ellennőrzés / Nem KEF-es eljárás szabályossági ellenőrzési szakasz (KEF / NEM KEF mezőnél a „Nem KEF-es eljárás” opció kerül kiválasztásra, a „Feladat” mezőnél pedig a „minőség-ellenőrzés”)'),
    ('wage80', 'DKÜ-s ellennőrzés / Szerződésmódosítás (Feladat mezőnél a Szerződésmódosítás opció kerül kiválasztásra)'),
    ('wage81', 'DKÜ-s ellennőrzés / Beszerzés (Feladat mezőnél a Beszerzés opció kerül kiválasztásra)'),
}





class ProjectProject(models.Model):
    
    _name = 'project.project'
    _inherit = 'project.project'
    
    
    # 1 szakaszos
    wage1 = fields.Float(u'Az eljárás előkészítése és kiírása', help='Az eljárást megindító felhívás megküldése / feladása Mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage2 = fields.Float(u'Az eljárás lefolytatásának első részteljesítése', help='Az ajánlatok bontása Mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage3 = fields.Float(u'Az eljárás lefolytatásának végteljesítése', help='EREDMÉNYTELENSÉGRŐL szóló tájékoztató /KIZÁRÓ VAGY/  "A szerződéstervezet megküldése az ügyfélnek" VALAMELYIK mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage4 = fields.Float(u'Az eljárás lezárása', help='"Aláírt ügyfél teljesítésigazolás beérkezett" ÉS "Aláírt referenciaigazolás(ok) beérkeztek" ÉS "Az eljárási iratok átadásra kerültek" ÉS "Tanúsítvány kiállításra került" Mezők kitöltése és a beírt legkésőbbi dátum alapján kerül be a havi teljesítésigazolásba.')
    wage5 = fields.Float(u'Az eljárás előkészítése és kiírása', help='Az eljárást megindító felhívás megküldése / feladása Mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage6 = fields.Float(u'Az eljárás lefolytatásának első részteljesítése', help='Az ajánlatok bontása Mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage7 = fields.Float(u'Az eljárás lefolytatásának végteljesítése', help='EREDMÉNYTELENSÉGRŐL szóló tájékoztató /KIZÁRÓ VAGY/  "A szerződéstervezet megküldése az ügyfélnek" VALAMELYIK mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage8 = fields.Float(u'Az eljárás lezárása', help='"Aláírt ügyfél teljesítésigazolás beérkezett" ÉS "Aláírt referenciaigazolás(ok) beérkeztek" ÉS "Az eljárási iratok átadásra kerültek" ÉS "Tanúsítvány kiállításra került" Mezők kitöltése és a beírt legkésőbbi dátum alapján kerül be a havi teljesítésigazolásba.')
    wage9 = fields.Float(u'Az eljárás előkészítése és kiírása', help='Az eljárást megindító felhívás megküldése / feladása Mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage10 = fields.Float(u'Az eljárás lefolytatásának első részteljesítése', help='Az ajánlatok bontása Mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage11 = fields.Float(u'Az eljárás lefolytatásának végteljesítése', help='EREDMÉNYTELENSÉGRŐL szóló tájékoztató /KIZÁRÓ VAGY/  "A szerződéstervezet megküldése az ügyfélnek" VALAMELYIK mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage12 = fields.Float(u'Az eljárás lezárása', help='"Aláírt ügyfél teljesítésigazolás beérkezett" ÉS "Aláírt referenciaigazolás(ok) beérkeztek" ÉS "Az eljárási iratok átadásra kerültek" ÉS "Tanúsítvány kiállításra került" Mezők kitöltése és a beírt legkésőbbi dátum alapján kerül be a havi teljesítésigazolásba.')
    wage13 = fields.Float(u'Az eljárás előkészítése és kiírása', help='Az eljárást megindító felhívás megküldése / feladása Mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage14 = fields.Float(u'Az eljárás lefolytatásának első részteljesítése', help='Az ajánlatok bontása Mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage15 = fields.Float(u'Az eljárás lefolytatásának végteljesítése', help='EREDMÉNYTELENSÉGRŐL szóló tájékoztató /KIZÁRÓ VAGY/  "A szerződéstervezet megküldése az ügyfélnek" VALAMELYIK mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage16 = fields.Float(u'Az eljárás lezárása', help='"Aláírt ügyfél teljesítésigazolás beérkezett" ÉS "Aláírt referenciaigazolás(ok) beérkeztek" ÉS "Az eljárási iratok átadásra kerültek" ÉS "Tanúsítvány kiállításra került" Mezők kitöltése és a beírt legkésőbbi dátum alapján kerül be a havi teljesítésigazolásba.')
    wage17 = fields.Float(u'Az eljárás előkészítése és kiírása', help='Az eljárást megindító felhívás megküldése / feladása Mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage18 = fields.Float(u'Az eljárás lefolytatásának első részteljesítése', help='Az ajánlatok bontása Mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage19 = fields.Float(u'Az eljárás lefolytatásának végteljesítése', help='EREDMÉNYTELENSÉGRŐL szóló tájékoztató /KIZÁRÓ VAGY/  "A szerződéstervezet megküldése az ügyfélnek" VALAMELYIK mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage20 = fields.Float(u'Az eljárás lezárása', help='"Aláírt ügyfél teljesítésigazolás beérkezett" ÉS "Aláírt referenciaigazolás(ok) beérkeztek" ÉS "Az eljárási iratok átadásra kerültek" ÉS "Tanúsítvány kiállításra került" Mezők kitöltése és a beírt legkésőbbi dátum alapján kerül be a havi teljesítésigazolásba.')
    wage21 = fields.Float(u'Az eljárás előkészítése és kiírása', help='Az eljárást megindító felhívás megküldése / feladása Mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage22 = fields.Float(u'Az eljárás lefolytatásának első részteljesítése', help='Az ajánlatok bontása Mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage23 = fields.Float(u'Az eljárás lefolytatásának végteljesítése', help='EREDMÉNYTELENSÉGRŐL szóló tájékoztató /KIZÁRÓ VAGY/  "A szerződéstervezet megküldése az ügyfélnek" VALAMELYIK mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage24 = fields.Float(u'Az eljárás lezárása', help='"Aláírt ügyfél teljesítésigazolás beérkezett" ÉS "Aláírt referenciaigazolás(ok) beérkeztek" ÉS "Az eljárási iratok átadásra kerültek" ÉS "Tanúsítvány kiállításra került" Mezők kitöltése és a beírt legkésőbbi dátum alapján kerül be a havi teljesítésigazolásba.')
    wage25 = fields.Float(u'Az eljárás előkészítése és kiírása', help='A folyamatba épített ellenőrzés megindításra került Mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage26 = fields.Float(u'Az eljárás lefolytatásának első részteljesítése', help='Az ajánlatok bontása Mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage27 = fields.Float(u'Az eljárás lefolytatásának végteljesítése', help='EREDMÉNYTELENSÉGRŐL szóló tájékoztató /KIZÁRÓ VAGY/  "A szerződéstervezet megküldése az ügyfélnek" VALAMELYIK mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage28 = fields.Float(u'Az eljárás lezárása', help='"Aláírt ügyfél teljesítésigazolás beérkezett" ÉS "Aláírt referenciaigazolás(ok) beérkeztek" ÉS "Az eljárási iratok átadásra kerültek" ÉS "Tanúsítvány kiállításra került" Mezők kitöltése és a beírt legkésőbbi dátum alapján kerül be a havi teljesítésigazolásba.')
    wage29 = fields.Float(u'Az eljárás lefolytatásának végteljesítése', help='EREDMÉNYTELENSÉGRŐL szóló tájékoztató /KIZÁRÓ VAGY/  "A szerződéstervezet megküldése az ügyfélnek" VALAMELYIK mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage74 = fields.Float(u'Az eljárás lefolytatásának végteljesítése', help='EREDMÉNYTELENSÉGRŐL szóló tájékoztató /KIZÁRÓ VAGY/  "A szerződéstervezet megküldése az ügyfélnek" VALAMELYIK mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage30 = fields.Float(u'Megtartott tárgyalás', help='A Megtartott tárgyalás Mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    # 2 szakaszos
    wage31 = fields.Float(u'Az eljárás előkészítése és kiírása', help='Az eljárást megindító felhívás megküldése / feladása Mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage32 = fields.Float(u'A részvételi szakasz lefolytatásának első részteljesítése', help='A Jelentkezések bontása Mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage33 = fields.Float(u'A részvételi szakasz lefolytatásának végteljesítése', help='Az eljárás visszavonásának dátuma /KIZÁRÓ VAGY/  "Részvételi összegezés megküldése" VALAMELYIK mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage34 = fields.Float(u'Az ajánlattételi szakasz lefolytatásának első részteljesítése', help='Az ajánlatok bontása Mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage35 = fields.Float(u'Az eljárás lefolytatásának végteljesítése', help='EREDMÉNYTELENSÉGRŐL szóló tájékoztató /KIZÁRÓ VAGY/  "A szerződéstervezet megküldése az ügyfélnek" VALAMELYIK mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage36 = fields.Float(u'Az eljárás lezárása', help='"Aláírt ügyfél teljesítésigazolás beérkezett" ÉS "Aláírt referenciaigazolás(ok) beérkeztek" ÉS "Az eljárási iratok átadásra kerültek" ÉS "Tanúsítvány kiállításra került" Mezők kitöltése és a beírt legkésőbbi dátum alapján kerül be a havi teljesítésigazolásba.')
    wage37 = fields.Float(u'Az eljárás előkészítése és kiírása', help='Az eljárást megindító felhívás megküldése / feladása Mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage38 = fields.Float(u'A részvételi szakasz lefolytatásának első részteljesítése', help='A Jelentkezések bontása Mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage39 = fields.Float(u'A részvételi szakasz lefolytatásának végteljesítése', help='Az eljárás visszavonásának dátuma /KIZÁRÓ VAGY/  "Részvételi összegezés megküldése" VALAMELYIK mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage40 = fields.Float(u'Az ajánlattételi szakasz lefolytatásának első részteljesítése', help='Az ajánlatok bontása Mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage41 = fields.Float(u'Az eljárás lefolytatásának végteljesítése', help='EREDMÉNYTELENSÉGRŐL szóló tájékoztató /KIZÁRÓ VAGY/  "A szerződéstervezet megküldése az ügyfélnek" VALAMELYIK mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage42 = fields.Float(u'Az eljárás lezárása', help='"Aláírt ügyfél teljesítésigazolás beérkezett" ÉS "Aláírt referenciaigazolás(ok) beérkeztek" ÉS "Az eljárási iratok átadásra kerültek" ÉS "Tanúsítvány kiállításra került" Mezők kitöltése és a beírt legkésőbbi dátum alapján kerül be a havi teljesítésigazolásba.')
    wage43 = fields.Float(u'Az eljárás előkészítése és kiírása', help='Az eljárást megindító felhívás megküldése / feladása Mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage44 = fields.Float(u'A részvételi szakasz lefolytatásának első részteljesítése', help='A Jelentkezések bontása Mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage45 = fields.Float(u'A részvételi szakasz lefolytatásának végteljesítése', help='Az eljárás visszavonásának dátuma /KIZÁRÓ VAGY/  "Részvételi összegezés megküldése" VALAMELYIK mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage46 = fields.Float(u'Az ajánlattételi szakasz lefolytatásának első részteljesítése', help='Az ajánlatok bontása Mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage47 = fields.Float(u'Az eljárás lefolytatásának végteljesítése', help='EREDMÉNYTELENSÉGRŐL szóló tájékoztató /KIZÁRÓ VAGY/  "A szerződéstervezet megküldése az ügyfélnek" VALAMELYIK mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage48 = fields.Float(u'Az eljárás lezárása', help='"Aláírt ügyfél teljesítésigazolás beérkezett" ÉS "Aláírt referenciaigazolás(ok) beérkeztek" ÉS "Az eljárási iratok átadásra kerültek" ÉS "Tanúsítvány kiállításra került" Mezők kitöltése és a beírt legkésőbbi dátum alapján kerül be a havi teljesítésigazolásba.')
    wage49 = fields.Float(u'Az eljárás előkészítése és kiírása', help='Az eljárást megindító felhívás megküldése / feladása Mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage50 = fields.Float(u'A részvételi szakasz lefolytatásának első részteljesítése', help='A Jelentkezések bontása Mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage51 = fields.Float(u'A részvételi szakasz lefolytatásának végteljesítése', help='Az eljárás visszavonásának dátuma /KIZÁRÓ VAGY/  "Részvételi összegezés megküldése" VALAMELYIK mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage52 = fields.Float(u'Az ajánlattételi szakasz lefolytatásának első részteljesítése', help='Az ajánlatok bontása Mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage53 = fields.Float(u'Az eljárás lefolytatásának végteljesítése', help='EREDMÉNYTELENSÉGRŐL szóló tájékoztató /KIZÁRÓ VAGY/  "A szerződéstervezet megküldése az ügyfélnek" VALAMELYIK mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage54 = fields.Float(u'Az eljárás lezárása', help='"Aláírt ügyfél teljesítésigazolás beérkezett" ÉS "Aláírt referenciaigazolás(ok) beérkeztek" ÉS "Az eljárási iratok átadásra kerültek" ÉS "Tanúsítvány kiállításra került" Mezők kitöltése és a beírt legkésőbbi dátum alapján kerül be a havi teljesítésigazolásba.')
    wage55 = fields.Float(u'Az eljárás előkészítése és kiírása', help='A folyamatba épített ellenőrzés megindításra került Mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage56 = fields.Float(u'A részvételi szakasz lefolytatásának első részteljesítése', help='A Jelentkezések bontása Mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage57 = fields.Float(u'A részvételi szakasz lefolytatásának végteljesítése', help='Az eljárás visszavonásának dátuma /KIZÁRÓ VAGY/  "Részvételi összegezés megküldése" VALAMELYIK mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage58 = fields.Float(u'Az ajánlattételi szakasz lefolytatásának első részteljesítése', help='Az ajánlatok bontása Mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage59 = fields.Float(u'Az eljárás lefolytatásának végteljesítése', help='EREDMÉNYTELENSÉGRŐL szóló tájékoztató /KIZÁRÓ VAGY/  "A szerződéstervezet megküldése az ügyfélnek" VALAMELYIK mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage60 = fields.Float(u'Az eljárás lezárása', help='"Aláírt ügyfél teljesítésigazolás beérkezett" ÉS "Aláírt referenciaigazolás(ok) beérkeztek" ÉS "Az eljárási iratok átadásra kerültek" ÉS "Tanúsítvány kiállításra került" Mezők kitöltése és a beírt legkésőbbi dátum alapján kerül be a havi teljesítésigazolásba.')
    wage61 = fields.Float(u'A részvételi szakasz lefolytatásának végteljesítése', help='"Részvételi összegezés megküldése" mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage62 = fields.Float(u'Az eljárás lefolytatásának végteljesítése', help='EREDMÉNYTELENSÉGRŐL szóló tájékoztató /KIZÁRÓ VAGY/  "A szerződéstervezet megküldése az ügyfélnek" VALAMELYIK mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage75 = fields.Float(u'Az eljárás lefolytatásának végteljesítése', help='EREDMÉNYTELENSÉGRŐL szóló tájékoztató /KIZÁRÓ VAGY/  "A szerződéstervezet megküldése az ügyfélnek" VALAMELYIK mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    wage63 = fields.Float(u'Megtartott tárgyalás', help='A Megtartott tárgyalás Mező kitöltése és a beírt dátum hónapjában számolható el a teljesítménybér.')
    # kff
    wage64 = fields.Float(u'KFF minőség-ellenőrzés', help='A "Feladat" mezőben a "Minőség-ellenőrzés" van kiválasztva ÉS a "Feladat lezárulása" mező kitöltésre kerül a dátummal')
    wage65 = fields.Float(u'KFF szabályossági ellenőrzés', help='A "Feladat" mezőben a "Szabályossági ellenőrzés" van kiválasztva ÉS a "Feladat lezárulása" mező kitöltésre kerül a dátummal')
    wage66 = fields.Float(u'KFF szerződésmódosítás', help='A "Feladat" mezőben a "Szerződésmódosítás ellenőrzés" van kiválasztva ÉS a "Feladat lezárulása" mező kitöltésre kerül a dátummal')
    # szerződésmódosítás
    wage67 = fields.Float(u'Szerződésmódosítás', help='A "Tájékoztató feladva" kitöltésre került ÉS az "Aláírt ügyfél teljesítésigazolás beérkezett" mező kitöltésre kerül a dátummal')
    # versenyeztetés
    wage68 = fields.Float(u'Versenyeztetés', help='Az "Az iratok átadásra kerültek" kitöltésre került ÉS az "Aláírt ügyfél teljesítésigazolás beérkezett" mező kitöltésre kerül a dátummal')
    # PR, marketing
    wage69 = fields.Float(u'Szakmai cikk', help='Ha a „Feladat mezőben” a „szakmai cikk” került kiválasztásra, ÉS mindhárom dátum mező kitöltésre került (azaz a feladat automatikusan lezárva státuszba került, akkor számolódjon el a rendszerben.')
    wage70 = fields.Float(u'Egyéb cikk', help='Ha a „Feladat mezőben” a „egyéb cikk” került kiválasztásra, ÉS mindhárom dátum mező kitöltésre került (azaz a feladat automatikusan lezárva státuszba került, akkor számolódjon el a rendszerben.')
    wage71 = fields.Float(u'Kép/Videó és komment', help='Ha a „Feladat mezőben” a „Kép/Videó és komment” került kiválasztásra, ÉS mindhárom dátum mező kitöltésre került (azaz a feladat automatikusan lezárva státuszba került, akkor számolódjon el a rendszerben.')
    # Óradíjas és Irodavezetői óradíjas
    wage72 = fields.Float(u'Óradíj / Óradíjas feladatok')
    wage73 = fields.Float(u'Óradíj / Irodavezetői óradíjas feladatok')
    wage82 = fields.Float(u'Óradíj / Eljárásokkal kapcsolatos óradíj')
    # dku
    wage76 = fields.Float(u'KEF-es eljárás minőség-ellenőrzési szakasz (KEF / NEM KEF mezőnél a „KEF-es eljárás” opció kerül kiválasztásra, a „Feladat” mezőnél pedig a „minőség-ellenőrzés”)')
    wage77 = fields.Float(u'KEF-es eljárás szabályossági ellenőrzési szakasz (KEF / NEM KEF mezőnél a „KEF-es eljárás” opció kerül kiválasztásra, a „Feladat” mezőnél pedig a „szabályossági ellenőrzés”)')
    wage78 = fields.Float(u'Nem KEF-es eljárás minőség-ellenőrzési szakasz (KEF / NEM KEF mezőnél a „Nem KEF-es eljárás” opció kerül kiválasztásra, a „Feladat” mezőnél pedig a „minőség-ellenőrzés”)')
    wage79 = fields.Float(u'Nem KEF-es eljárás szabályossági ellenőrzési szakasz (KEF / NEM KEF mezőnél a „Nem KEF-es eljárás” opció kerül kiválasztásra, a „Feladat” mezőnél pedig a „minőség-ellenőrzés”)')
    wage80 = fields.Float(u'Szerződésmódosítás (Feladat mezőnél a Szerződésmódosítás opció kerül kiválasztásra)')
    wage81 = fields.Float(u'Beszerzés (Feladat mezőnél a Beszerzés opció kerül kiválasztásra)')





class ProjectTask(models.Model):
    
    _inherit = 'project.task'
    
    
    project_name = fields.Char(u'Project name', related='project_id.name', readonly=True)

    next_step = fields.Char(u'Soron következő lépés')
    invoice_plan_date = fields.Date(u'Várható számlázási dátum')
    weekly_notofy_emails = fields.Char(u'Heti értesítés emailcímei')
    progress_ids = fields.One2many('project.task.progress', 'task_id', u'Tevékenységek')
    requesting_partner_id = fields.Many2one('res.partner', u'Ajánlatkérő')
    requesting_partner_nickname = fields.Char(u'Ajánlatkérő becenév', related='requesting_partner_id.nickname', store=True)
    consultant = fields.Many2one('res.users', u'Tanácsadó')
    inspector = fields.Many2one('res.users', u'Ellenőr')
    estimated_price = fields.Float(u'Becsült érték')
    control = fields.Selection(CONTROL, u'Ellenőrzés')
    bidding_deadline = fields.Datetime(u'Ajánlattételi határidő')
    invoice_partial_plan_date = fields.Date(u'Várható részszámla számlázási dátum')
    nops = fields.Integer(u'Közbeszerzési részek száma')
    notsdtp = fields.Integer(u'Az eljárásban benyújtott részvételi jelentkezések száma')
    noooe = fields.Integer(u'Értékelt ajánlatok száma')
    notsitp = fields.Integer(u'Bírált ajánlatok száma')
    server_link = fields.Char(u'Az ügy linkes elérhetősége a szerveren')
    procedure = fields.Selection(PROCEDURE, u'Eljárásrend')
    procedure_type_id = fields.Many2one('project.task.procedure.type', u'Eljárás fajtája')
    kff_task = fields.Selection(KFF_TASK, u'Feladat')
    registration_code = fields.Char(u'Iktatási kód')
    order_send_date = fields.Date(u'Megrendelés kiküldésének időpontja')
    kff_identification = fields.Char(u'Azonosító')
    contact = fields.Char(u'Kapcsolattartó')
    proceedings_type = fields.Char(u'Eljárás típusa')
    expert_date = fields.Datetime(u'Szakértő határideje')
    document = fields.Text(u'Megküldött dokumentum')
    expert_sent = fields.Datetime(u'Szakértő megküldte')
    foureyes_sent = fields.Datetime(u'Négyszemes szakértő megküldte')
    kff_desc = fields.Text(u'Projekt neve/Feladat típusa/Feladatleírás')
    kff_guru_deadline = fields.Datetime(u'Saját teljesítési határidő')
    date_deadline = fields.Datetime(u'Határidő')
    sent_kff_guru_notify_3 = fields.Datetime(u'3 órás figyelmeztetés elküldve', readonly=True)
    description = fields.Html(u'Leírás', placeholder=u'Bármi amit fontosnak tartasz azt ide írhatod, pl: kiküldetés eredményének összefoglalása, stb.')
    bid_validity_expires = fields.Date(u'Ajánlati kötöttség lejárta')
    sent_bid_validity_expires_3 = fields.Datetime(u'3 napos figyelmeztetés elküldve', readonly=True)
    sent_bid_validity_expires_7 = fields.Datetime(u'7 napos figyelmeztetés elküldve', readonly=True)
    trainee_task = fields.Boolean(u'Gyakornoki feladat')
    scheduled_date_of_contract = fields.Datetime(u'Szerződéskötés tervezett időpontja')
    kmok_responsible = fields.Char(u'Ajánlatkérő szakmai felelőse')
    kmok_state = fields.Many2one('project.task.kmok.state', u'Közbeszerzési eljárás állapota (státuszkódok)')
    kmok_recent_act = fields.Text(u'Legutóbbi (eljárási) cselekmény')
    kmok_next_act = fields.Text(u'Soron következő (eljárási) cselekmény')
    pr_task = fields.Selection(PR_TASK, u'Feladat')
    kef = fields.Selection(KEF, u'KEF / NEM KEF')
    
    date1_date = fields.Date(u'Előkészítési szakaszba került')
    date2_date = fields.Date(u'A folyamatba épített ellenőrzés megindításra került')
    date2_file1 = fields.Binary(u'E-mail', attachment=True)
    date3_date = fields.Date(u'Az eljárást megindító felhívás megküldése / feladása')
    date3_file1 = fields.Binary(u'Feladott / megküldött felhívás', attachment=True)
    date4_date = fields.Date(u'Az eljárás visszavonásának dátuma')
    date4_file1 = fields.Binary(u'Feladott / megküldött visszavonás', attachment=True)
    date5_date = fields.Date(u'Jelentkezések bontása')
    date6_date = fields.Date(u'Részvételi összegezés megküldése')
    date7_date = fields.Date(u'Az ajánlatok bontása')
    date7_file1 = fields.Binary(u'Bontási jegyzőkönyv', attachment=True)
    date8_date = fields.Date(u'Az összegezés megküldése')
    date9_date = fields.Date(u'EREDMÉNYTELENSÉGRŐL szóló tájékoztató')
    date9_file1 = fields.Binary(u'Eredménytelenségről szóló tájékoztató', attachment=True)
    date10_date = fields.Date(u'A szerződéstervezet megküldése az ügyfélnek')
    date10_file1 = fields.Binary(u'Előkészített szerződéstervezet(ek)', attachment=True)
    date11_date = fields.Date(u'EREDMÉNYES eljárásról tájékoztató')
    date11_file1 = fields.Binary(u'Eredményről szóló tájékoztató', attachment=True)
    date12_date = fields.Date(u'Aláírt ügyfél teljesítésigazolás beérkezett')
    date12_file1 = fields.Binary(u'Teljesítésigazolás', attachment=True)
    date13_date = fields.Date(u'Aláírt referenciaigazolás(ok) beérkeztek')
    date13_file1 = fields.Binary(u'Referenciaigazolás', attachment=True)
    date14_date = fields.Date(u'Az iratok átadásra kerültek')
    date14_file1 = fields.Binary(u'Iratátadási jegyzőkönyv', attachment=True)
    date15_date = fields.Date(u'Tanúsítvány kiállításra került')
    date15_file1 = fields.Binary(u'Tanúsítvány', attachment=True)
    meeting_log_id = fields.One2many('project.task.meeting.log', 'task_id', u'Megtartott tárgyalás')
    date17_date = fields.Date(u'Minőségellenőrzési szakasz lázárulása') #TODO: Elvileg törölhető
    date18_date = fields.Date(u'Szabályossági szakasz lezárulása') #TODO: Elvileg törölhető
    date19_date = fields.Date(u'Utólagos ellenőrzés lezárulása') #TODO: Elvileg törölhető
    date20_date = fields.Date(u'Szerződésmódosítás állásfoglalás elkészítése') #TODO: Elvileg törölhető
    date21_date = fields.Date(u'Tájékoztató feladva')
    date21_file1 = fields.Binary(u'Feladott tájékoztató', attachment=True)
    date22_date = fields.Date(u'Tanúsítvány kiállításra került')
    date22_file1 = fields.Binary(u'Tanúsítvány', attachment=True)
    date23_date = fields.Date(u'Az iratok átadásra kerültek')
    date23_file1 = fields.Binary(u'Iratátadási jegyzőkönyv', attachment=True)
    date24_date = fields.Date(u'Aláírt ügyfél teljesítésigazolás beérkezett')
    date24_file1 = fields.Binary(u'Teljesíatésigazolás', attachment=True)
    date25_date = fields.Date(u'Feladat kiosztása')
    date26_date = fields.Date(u'Feladat lezárulása')
    # PR, Marketing
    date27_date = fields.Date(u'Ellenőrzésre küldve')
    date28_date = fields.Date(u'Marketinges jóváhagyta')
    date29_date = fields.Date(u'Koordinátor jóváhagyta')
    
    wage_version = fields.Selection(WAGE_VERSION, u'Teljesítménybér elszámolás', readonly=True)
    wage_ids = fields.One2many('project.task.wage', 'task_id', u'Teljesítménybér elszámolások', readonly=True)


    def get_share_url(self):
        self.ensure_one()
        params = {
            'model': self._name,
            'id': self.id,
        }
        if hasattr(self, 'access_token') and self.access_token:
            params['access_token'] = self.access_token
        if hasattr(self, 'partner_id') and self.partner_id:
            params.update(self.partner_id.signup_get_auth_param()[self.partner_id.id])

        return '/web#' + url_encode(params) + '&view_type=form'


    def task_weekly_notify(self):
        Tasks = self.env['project.task'].search([('weekly_notofy_emails', '!=', False), ('stage_id', 'in', [5])])
        for Task in Tasks:
            self.env.ref('kbl.notify_weekly').with_context().send_mail(Task.id, force_send=True)





class ProjectTaskProgress(models.Model):
    
    _name = 'project.task.progress'
    _order = 'task_id, date'


    company_id = fields.Many2one('res.company', 'Company', index=True)
    name = fields.Char(u'Leírás', required=True)
    task_id = fields.Many2one('project.task', u'Feladat', required=True)
    date = fields.Date(u'Dátum', required=True)





class ProjectTaskMeetingLog(models.Model):
    
    _name = 'project.task.meeting.log'
    
    
    company_id = fields.Many2one('res.company', 'Company', index=True)
    task_id = fields.Many2one(u'Task', required=True)
    name = fields.Char(u'Tárgyalás tárgya', required=True)
    date = fields.Date(u'Tárgyalás időpontja', required=True)
    file1 = fields.Binary(u'Teljesíatésigazolás', attachment=True)
    
    
    
    

class ProjectTaskProcedureType(models.Model):
    
    _name = 'project.task.procedure.type'


    name = fields.Char(u'Eljárás fajtája', required=True)
    procedure = fields.Selection(PROCEDURE, u'Eljárásrend', required=True)





class ProjectTaskWage(models.Model):
    
    _name = 'project.task.wage'
    _rec_name = 'wage'
    _order = 'user_id, project_id, task_id'
    
    
    company_id = fields.Many2one('res.company', 'Company', index=True)
    task_id = fields.Many2one('project.task', u'Feladat', readonly=True)
    project_id = fields.Many2one('project.project', related='task_id.project_id', store=True, readonly=True)
    user_id = fields.Many2one('res.users', u'Tanácsadó', readonly=True)
    state = fields.Selection([('open', 'Elszámolható'), ('confirmed', 'Jóváhagyva'), ('complete', 'Elszámolva')], string='Státusz', required=True, default='open')
    wage = fields.Selection(WAGE, u'A részteljesítést eredményező cselekmény', readonly=True)
    amount = fields.Float(u'Elszámolható összeg (HUF)', readonly=True)
    date_set = fields.Date(u'Dátum mező értéke elszámoláskor', readonly=True)
    date_accounted = fields.Date(u'Elszámolva', readonly=True)
    meeting_log_id = fields.Many2one(u'project.task.meeting.log', u'Megtartott tárgyalás', readonly=True)
    comment = fields.Text(u'Megjegyzés', readonly=True)
    employee_wage_id = fields.Many2one('hr.employee.wage', u'Elszámolás', readonly=True)
    aal_id = fields.Many2one('account_analytic_line', u'Account analytic line', readonly=True)

    
    def action_confirm(self):
        if self.user_has_groups('kozbeszguru.group_task_wage_wizard') and self.state == 'open':
            self.sudo().write({'state': 'confirmed'})

    def action_revoke(self):
        if self.user_has_groups('kozbeszguru.group_task_wage_wizard') and self.state == 'confirmed':
            self.sudo().write({'state': 'open'})
    
    def action_complete(self):
        if self.user_has_groups('kozbeszguru.group_task_wage_wizard') and self.state == 'open':
            self.sudo().write({'state': 'complete'})
    
    def action_delete(self):
        if self.user_has_groups('kozbeszguru.group_task_wage_wizard') and self.state == 'open':
            self.sudo().unlink()
            return ({'type': 'ir.actions.client', 'tag': 'reload'})
    
    def action_null(self):
        if self.user_has_groups('kozbeszguru.group_task_wage_wizard') and self.state == 'open':
            self.sudo().write({'amount': 0})
            self.sudo().write({'state': 'complete'})
        

    def create_auto_wage_settlement(self):
        
        sql = """
            SELECT DISTINCT(project_task_wage.user_id), hr_employee.id AS employee_id FROM project_task_wage
            JOIN hr_employee ON project_task_wage.user_id=hr_employee.user_id
            WHERE state='confirmed';
        """
        self.env.cr.execute(sql)
        userS = self.env.cr.dictfetchall()

        for user in userS:
        
            employeeWage = self.env['hr.employee.wage'].sudo().create({
                'employee_id': user['employee_id'],
                'accounting_period_start': '2019-01-01', #TODO
                'accounting_period_end': '2019-01-31', #TODO
            })

            wageS = self.env['project.task.wage'].sudo().search([('user_id', '=', user['user_id']), ('state', '=', 'confirmed')])
            sum = 0
            for wage in wageS:
                wage.employee_wage_id = employeeWage.id
                wage.state = 'complete'
                wage.date_accounted = '2019-02-01'  #TODO: fields.Date.today()
                sum += wage.amount

            Employee = self.env['hr.employee'].browse(user['employee_id'])
            employeeWage.sum = sum
            employeeWage.basic_wage = Employee['basic_wage']
            employeeWage.previous_sum = Employee['balance_previous']
            employeeWage.grand_total = employeeWage.sum + employeeWage.previous_sum
            if employeeWage.grand_total < employeeWage.basic_wage:
                employeeWage.payable = employeeWage.basic_wage
                employeeWage.next_base = employeeWage.grand_total - employeeWage.basic_wage
                Employee['balance_previous'] = employeeWage.next_base
            else:
                employeeWage.payable = employeeWage.grand_total
                employeeWage.next_base = 0
                Employee['balance_previous'] = 0

            employeeWage.state = 'created'





class WageBulkConfirm(models.TransientModel):

    _name = 'project.task.wage.bulk.confirm'
    _description = 'Tömeges jóváhagyás'


    wage_ids = fields.Many2many('project.task.wage', 'wage_bulk_confirm_rel', 'bulk_id', 'wage_id', string='Elszámolások', domain="[('state', '=', 'open')]")


    def default_get(self, fields):
        record_ids = self._context.get('active_ids')
        result = super(WageBulkConfirm, self).default_get(fields)
 
        if record_ids:
            if 'wage_ids' in fields:
                wage_ids = self.env['project.task.wage'].browse(record_ids).filtered(lambda stmt: stmt.state == 'open').ids
                result['wage_ids'] = wage_ids
 
        return result


    def action_confirm(self):
        self.ensure_one()

        for wage in self.wage_ids:
            if wage.state == 'open':
                wage.sudo().write({'state': 'confirmed'})





class ProjectTaskWageWizard(models.TransientModel):
    
    _name = 'project.task.wage.wizard'


    user_id = fields.Many2one('res.users', u'Tanácsadó', required=True)
    amount = fields.Float(u'Elszámolható összeg (HUF)', required=True)
    date = fields.Date(u'Időpont', required=True)
    comment = fields.Text(u'Megjegyzés', required=True)


    def action_create_wage(self):
        self.ensure_one()
        
        if self.user_has_groups('kozbeszguru.group_task_wage_wizard'):
            wage = self.env['project.task.wage'].sudo().create({
                'user_id': self.user_id.id,
                'amount': self.amount,
                'date_accounted': self.date,
                'comment': self.comment,
            })
        else:
            wage = self.env['project.task.wage'].create({
                'user_id': self.user_id.id,
                'amount': self.amount,
                'date_accounted': self.date,
                'comment': self.comment,
            })

        return {
            'name': 'Wage created',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('kozbeszguru.view_project_task_wage_form').id,
            'res_model': 'project.task.wage',
            'type': 'ir.actions.act_window',
            'res_id': wage.id,
            'context': self.env.context
        }





class ProjectTaskWageProcessor(models.TransientModel):
    
    _name = 'project.task.wage.processor'


    def wage_processor(self):
        
        # Teljesítménybér elszámolás verzió beállítás
        # Egy szakaszos közbeszerzési eljárások
        TaskS = self.env['project.task'].search([
            ('project_name', '=', 'Egy szakaszos közbeszerzési eljárások'),
            ('wage_version', '=', False),
        ])
        if TaskS:
            for Task in TaskS:
                if Task.procedure_type_id.id in (2, 8, 9, 12):
                    Task.wage_version = '1_1'
                elif Task.procedure_type_id.id in (1, 3, 5, 6, 7, 10, 11, 13):
                    Task.wage_version = '1_2'
                elif Task.procedure_type_id.id in (4, 14):
                    Task.wage_version = '1_3'
                else:
                    _logger.info('ERROR - Teljesítménybér elszámolás verzió nem határozható meg: ' + str(Task.id) + ' ' + Task.name)
        

        # Teljesítménybér sorok ellenőrzése és létrehozása
        # Egy szakaszos közbeszerzési eljárások
        TaskS = self.env['project.task'].search([
            ('project_name', '=', 'Egy szakaszos közbeszerzési eljárások'),
            ('wage_version', '!=', False),
        ])
        if TaskS:
            for Task in TaskS:
                if Task.consultant.id and Task.project_id.wage1 and Task.wage_version:
                    # Vagylagos szempontok (kizáró vagy)
                    if Task.wage_version == '1_1':
                        if Task.date3_date:
                            TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage1')])
                            if not TaskWageS:
                                self.env['project.task.wage'].sudo().create({
                                    'task_id': Task.id, 'user_id': Task.consultant.id,
                                    'wage': 'wage1', 'amount': Task.project_id.wage1 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                    'date_set': Task.date3_date,
                                })
                        if Task.date7_date:
                            TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage2')])
                            if not TaskWageS:
                                self.env['project.task.wage'].sudo().create({
                                    'task_id': Task.id, 'user_id': Task.consultant.id,
                                    'wage': 'wage2', 'amount': Task.project_id.wage2 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                    'date_set': Task.date7_date,
                                })
                        if Task.date9_date or Task.date10_date:
                            TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage3')])
                            if not TaskWageS:
                                self.env['project.task.wage'].sudo().create({
                                    'task_id': Task.id, 'user_id': Task.consultant.id,
                                    'wage': 'wage3', 'amount': Task.project_id.wage3 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                    'date_set': Task.date9_date or Task.date10_date,
                                })
                        if Task.control and (Task.control == 'followup' or Task.control == 'builtinprocess'):
                            if Task.date12_date and Task.date13_date and Task.date14_date and Task.date15_date:
                                TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage4')])
                                if not TaskWageS:
                                    self.env['project.task.wage'].sudo().create({
                                        'task_id': Task.id, 'user_id': Task.consultant.id,
                                        'wage': 'wage4', 'amount': Task.project_id.wage4 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                        'date_set': Task.date15_date,
                                    })
                        else:
                            if Task.date12_date and Task.date13_date and Task.date14_date:
                                TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage4')])
                                if not TaskWageS:
                                    self.env['project.task.wage'].sudo().create({
                                        'task_id': Task.id, 'user_id': Task.consultant.id,
                                        'wage': 'wage4', 'amount': Task.project_id.wage4 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                        'date_set': Task.date14_date,
                                    })
                    elif Task.wage_version == '1_2':
                        if Task.date3_date:
                            TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage5')])
                            if not TaskWageS:
                                self.env['project.task.wage'].sudo().create({
                                    'task_id': Task.id, 'user_id': Task.consultant.id,
                                    'wage': 'wage5', 'amount': Task.project_id.wage5 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                    'date_set': Task.date3_date,
                                })
                        if Task.date7_date:
                            TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage6')])
                            if not TaskWageS:
                                self.env['project.task.wage'].sudo().create({
                                    'task_id': Task.id, 'user_id': Task.consultant.id,
                                    'wage': 'wage6', 'amount': Task.project_id.wage6 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                    'date_set': Task.date7_date,
                                })
                        if Task.date9_date or Task.date10_date:
                            TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage7')])
                            if not TaskWageS:
                                self.env['project.task.wage'].sudo().create({
                                    'task_id': Task.id, 'user_id': Task.consultant.id,
                                    'wage': 'wage7', 'amount': Task.project_id.wage7 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                    'date_set': Task.date9_date or Task.date10_date,
                                })
                        if Task.control and (Task.control == 'followup' or Task.control == 'builtinprocess'):
                            if Task.date12_date and Task.date13_date and Task.date14_date and Task.date15_date:
                                TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage8')])
                                if not TaskWageS:
                                    self.env['project.task.wage'].sudo().create({
                                        'task_id': Task.id, 'user_id': Task.consultant.id,
                                        'wage': 'wage8', 'amount': Task.project_id.wage8 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                        'date_set': Task.date15_date,
                                    })
                        else:
                            if Task.date12_date and Task.date13_date and Task.date14_date:
                                TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage8')])
                                if not TaskWageS:
                                    self.env['project.task.wage'].sudo().create({
                                        'task_id': Task.id, 'user_id': Task.consultant.id,
                                        'wage': 'wage8', 'amount': Task.project_id.wage8 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                        'date_set': Task.date14_date,
                                    })
                    elif Task.wage_version == '1_3':
                        if Task.date3_date:
                            TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage9')])
                            if not TaskWageS:
                                self.env['project.task.wage'].sudo().create({
                                    'task_id': Task.id, 'user_id': Task.consultant.id,
                                    'wage': 'wage9', 'amount': Task.project_id.wage9 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                    'date_set': Task.date3_date,
                                })
                        if Task.date7_date:
                            TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage10')])
                            if not TaskWageS:
                                self.env['project.task.wage'].sudo().create({
                                    'task_id': Task.id, 'user_id': Task.consultant.id,
                                    'wage': 'wage10', 'amount': Task.project_id.wage10 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                    'date_set': Task.date7_date,
                                })
                        if Task.date9_date or Task.date10_date:
                            TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage11')])
                            if not TaskWageS:
                                self.env['project.task.wage'].sudo().create({
                                    'task_id': Task.id, 'user_id': Task.consultant.id,
                                    'wage': 'wage11', 'amount': Task.project_id.wage11 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                    'date_set': Task.date9_date or Task.date10_date,
                                })
                        if Task.control and (Task.control == 'followup' or Task.control == 'builtinprocess'):
                            if Task.date12_date and Task.date13_date and Task.date14_date and Task.date15_date:
                                TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage12')])
                                if not TaskWageS:
                                    self.env['project.task.wage'].sudo().create({
                                        'task_id': Task.id, 'user_id': Task.consultant.id,
                                        'wage': 'wage12', 'amount': Task.project_id.wage12 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                        'date_set': Task.date15_date,
                                    })
                        else:
                            if Task.date12_date and Task.date13_date and Task.date14_date:
                                TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage12')])
                                if not TaskWageS:
                                    self.env['project.task.wage'].sudo().create({
                                        'task_id': Task.id, 'user_id': Task.consultant.id,
                                        'wage': 'wage12', 'amount': Task.project_id.wage12 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                        'date_set': Task.date14_date,
                                    })
                    else:
                        _logger.info('ERROR - Teljesítménybér elszámolás verzió nem ismert: ' + str(Task.id) + ' ' + Task.name)
                    # Kiegészítő szempontok, azaz többlet bérek (megengedő vagy, tehát több is előfordulhat)
                    # Akkor érvényesül, ha az "A közbeszerzési részek száma" mező kitöltésre került.
                    if Task.nops > 1:
                        if Task.date3_date:
                            TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage13')])
                            if not TaskWageS:
                                self.env['project.task.wage'].sudo().create({
                                    'task_id': Task.id, 'user_id': Task.consultant.id,
                                    'wage': 'wage13', 'amount': Task.project_id.wage13 * Task.nops * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                    'date_set': Task.date3_date,
                                })
                        if Task.date7_date:
                            TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage14')])
                            if not TaskWageS:
                                self.env['project.task.wage'].sudo().create({
                                    'task_id': Task.id, 'user_id': Task.consultant.id,
                                    'wage': 'wage14', 'amount': Task.project_id.wage14 * Task.nops * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                    'date_set': Task.date7_date,
                                })
                        if Task.date9_date or Task.date10_date:
                            TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage15')])
                            if not TaskWageS:
                                self.env['project.task.wage'].sudo().create({
                                    'task_id': Task.id, 'user_id': Task.consultant.id,
                                    'wage': 'wage15', 'amount': Task.project_id.wage15 * Task.nops * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                    'date_set': Task.date9_date or Task.date10_date,
                                })
                        if Task.control and (Task.control == 'followup' or Task.control == 'builtinprocess'):
                            if Task.date12_date and Task.date13_date and Task.date14_date and Task.date15_date:
                                TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage16')])
                                if not TaskWageS:
                                    self.env['project.task.wage'].sudo().create({
                                        'task_id': Task.id, 'user_id': Task.consultant.id,
                                        'wage': 'wage16', 'amount': Task.project_id.wage16 * Task.nops * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                        'date_set': Task.date15_date,
                                    })
                        else:
                            if Task.date12_date and Task.date13_date and Task.date14_date:
                                TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage16')])
                                if not TaskWageS:
                                    self.env['project.task.wage'].sudo().create({
                                        'task_id': Task.id, 'user_id': Task.consultant.id,
                                        'wage': 'wage16', 'amount': Task.project_id.wage16 * Task.nops * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                        'date_set': Task.date14_date,
                                    })
                    # Akkor érvényesül, ha az eljárásrendnek uniós került kiválasztásra
                    if Task.procedure == 'union':
                        if Task.date3_date:
                            TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage17')])
                            if not TaskWageS:
                                self.env['project.task.wage'].sudo().create({
                                    'task_id': Task.id, 'user_id': Task.consultant.id,
                                    'wage': 'wage17', 'amount': Task.project_id.wage17 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                    'date_set': Task.date3_date,
                                })
                        if Task.date7_date:
                            TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage18')])
                            if not TaskWageS:
                                self.env['project.task.wage'].sudo().create({
                                    'task_id': Task.id, 'user_id': Task.consultant.id,
                                    'wage': 'wage18', 'amount': Task.project_id.wage18 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                    'date_set': Task.date7_date,
                                })
                        if Task.date9_date or Task.date10_date:
                            TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage19')])
                            if not TaskWageS:
                                self.env['project.task.wage'].sudo().create({
                                    'task_id': Task.id, 'user_id': Task.consultant.id,
                                    'wage': 'wage19', 'amount': Task.project_id.wage19 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                    'date_set': Task.date9_date or Task.date10_date,
                                })
                        if Task.control and (Task.control == 'followup' or Task.control == 'builtinprocess'):
                            if Task.date12_date and Task.date13_date and Task.date14_date and Task.date15_date:
                                TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage20')])
                                if not TaskWageS:
                                    self.env['project.task.wage'].sudo().create({
                                        'task_id': Task.id, 'user_id': Task.consultant.id,
                                        'wage': 'wage20', 'amount': Task.project_id.wage20 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                        'date_set': Task.date15_date,
                                    })
                        else:
                            if Task.date12_date and Task.date13_date and Task.date14_date:
                                TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage20')])
                                if not TaskWageS:
                                    self.env['project.task.wage'].sudo().create({
                                        'task_id': Task.id, 'user_id': Task.consultant.id,
                                        'wage': 'wage20', 'amount': Task.project_id.wage20 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                        'date_set': Task.date14_date,
                                    })
                    # Akkor érvényesül, ha az "Ellenőrzés" mezőnél "Utóellenőrzés" került kiválasztásra
                    if Task.control and Task.control == 'followup':
                        if Task.date3_date:
                            TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage21')])
                            if not TaskWageS:
                                self.env['project.task.wage'].sudo().create({
                                    'task_id': Task.id, 'user_id': Task.consultant.id,
                                    'wage': 'wage21', 'amount': Task.project_id.wage21 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                    'date_set': Task.date3_date,
                                })
                        if Task.date7_date:
                            TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage22')])
                            if not TaskWageS:
                                self.env['project.task.wage'].sudo().create({
                                    'task_id': Task.id, 'user_id': Task.consultant.id,
                                    'wage': 'wage22', 'amount': Task.project_id.wage22 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                    'date_set': Task.date7_date,
                                })
                        if Task.date9_date or Task.date10_date:
                            TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage23')])
                            if not TaskWageS:
                                self.env['project.task.wage'].sudo().create({
                                    'task_id': Task.id, 'user_id': Task.consultant.id,
                                    'wage': 'wage23', 'amount': Task.project_id.wage23 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                    'date_set': Task.date9_date or Task.date10_date,
                                })
                        if Task.control and (Task.control == 'followup' or Task.control == 'builtinprocess'):
                            if Task.date12_date and Task.date13_date and Task.date14_date and Task.date15_date:
                                TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage24')])
                                if not TaskWageS:
                                    self.env['project.task.wage'].sudo().create({
                                        'task_id': Task.id, 'user_id': Task.consultant.id,
                                        'wage': 'wage24', 'amount': Task.project_id.wage24 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                        'date_set': Task.date15_date,
                                    })
                        else:
                            if Task.date12_date and Task.date13_date and Task.date14_date:
                                TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage24')])
                                if not TaskWageS:
                                    self.env['project.task.wage'].sudo().create({
                                        'task_id': Task.id, 'user_id': Task.consultant.id,
                                        'wage': 'wage24', 'amount': Task.project_id.wage24 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                        'date_set': Task.date14_date,
                                    })
                    # Akkor érvényesül, ha az "Ellenőrzés" mezőnél "Folyamatba épített" került kiválasztásra
                    if Task.control and Task.control == 'builtinprocess':
                        if Task.date2_date:
                            TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage25')])
                            if not TaskWageS:
                                self.env['project.task.wage'].sudo().create({
                                    'task_id': Task.id, 'user_id': Task.consultant.id,
                                    'wage': 'wage25', 'amount': Task.project_id.wage25 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                    'date_set': Task.date2_date,
                                })
                        if Task.date7_date:
                            TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage26')])
                            if not TaskWageS:
                                self.env['project.task.wage'].sudo().create({
                                    'task_id': Task.id, 'user_id': Task.consultant.id,
                                    'wage': 'wage26', 'amount': Task.project_id.wage26 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                    'date_set': Task.date7_date,
                                })
                        if Task.date9_date or Task.date10_date:
                            TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage27')])
                            if not TaskWageS:
                                self.env['project.task.wage'].sudo().create({
                                    'task_id': Task.id, 'user_id': Task.consultant.id,
                                    'wage': 'wage27', 'amount': Task.project_id.wage27 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                    'date_set': Task.date9_date or Task.date10_date,
                                })
                        if Task.control and (Task.control == 'followup' or Task.control == 'builtinprocess'):
                            if Task.date12_date and Task.date13_date and Task.date14_date and Task.date15_date:
                                TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage28')])
                                if not TaskWageS:
                                    self.env['project.task.wage'].sudo().create({
                                        'task_id': Task.id, 'user_id': Task.consultant.id,
                                        'wage': 'wage28', 'amount': Task.project_id.wage28 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                        'date_set': Task.date15_date,
                                    })
                        else:
                            if Task.date12_date and Task.date13_date and Task.date14_date:
                                TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage28')])
                                if not TaskWageS:
                                    self.env['project.task.wage'].sudo().create({
                                        'task_id': Task.id, 'user_id': Task.consultant.id,
                                        'wage': 'wage28', 'amount': Task.project_id.wage28 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                        'date_set': Task.date14_date,
                                    })
                    # Akkor érvényesül, ha a "Bírált ajánlatok száma" mező kitöltésre került.
                    if Task.notsitp:
                        if Task.date9_date or Task.date10_date:
                            TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage29')])
                            if not TaskWageS:
                                self.env['project.task.wage'].sudo().create({
                                    'task_id': Task.id, 'user_id': Task.consultant.id,
                                    'wage': 'wage29', 'amount': Task.project_id.wage29 * (Task.notsitp or 1) * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                    'date_set': Task.date9_date or Task.date10_date,
                                })
                    # Akkor érvényesül, ha az "Értékelt ajánlatok száma" mező kitöltésre került.
                    if Task.noooe:
                        if Task.date9_date or Task.date10_date:
                            TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage74')])
                            if not TaskWageS:
                                self.env['project.task.wage'].sudo().create({
                                    'task_id': Task.id, 'user_id': Task.consultant.id,
                                    'wage': 'wage74', 'amount': Task.project_id.wage74 * (Task.noooe or 1) * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                    'date_set': Task.date9_date or Task.date10_date,
                                })
                    # Akkor és annyiszor érvényesül, amikor és ahányszor a "Megtartott tárgyalás" mező(k) kitöltésre került(ek)
                    ProjectTaskMeetingLogS = self.env['project.task.meeting.log'].search([('task_id', '=', Task.id)])
                    if ProjectTaskMeetingLogS:
                        for ProjectTaskMeetingLog in ProjectTaskMeetingLogS:
                            TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage30'), ('meeting_log_id', '=', ProjectTaskMeetingLog.id)])
                            if not TaskWageS:
                                self.env['project.task.wage'].sudo().create({
                                    'task_id': Task.id, 'user_id': Task.consultant.id,
                                    'wage': 'wage30', 'amount': Task.project_id.wage30 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                    'date_set': ProjectTaskMeetingLog.date,
                                    'meeting_log_id': ProjectTaskMeetingLog.id,
                                })
                else:
                    _logger.info('ERROR - Teljesítménybér elszámolásához hiányosak az adatok: ' + str(Task.id) + ' ' + Task.name)
        # Két szakaszos közbeszerzési eljárások
        TaskS = self.env['project.task'].search([
            ('project_name', '=', 'Két szakaszos közbeszerzési eljárások'),
        ])
        if TaskS:
            for Task in TaskS:
                # Összefoglaló tájékoztatással, vagy hirdetmény közzétételével induló eljárás esetén
                #TODO: Ez elvileg nem kell: if Task.procedure_type_id.id in (1, 3, 5, 6, 7, 10, 11, 12, 13):
                if Task.date3_date:
                    TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage31')])
                    if not TaskWageS:
                        self.env['project.task.wage'].sudo().create({
                            'task_id': Task.id, 'user_id': Task.consultant.id,
                            'wage': 'wage31', 'amount': Task.project_id.wage31 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                            'date_set': Task.date3_date,
                        })
                if Task.date5_date:
                    TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage32')])
                    if not TaskWageS:
                        self.env['project.task.wage'].sudo().create({
                            'task_id': Task.id, 'user_id': Task.consultant.id,
                            'wage': 'wage32', 'amount': Task.project_id.wage32 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                            'date_set': Task.date5_date,
                        })
                if Task.date4_date or Task.date6_date:
                    TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage33')])
                    if not TaskWageS:
                        self.env['project.task.wage'].sudo().create({
                            'task_id': Task.id, 'user_id': Task.consultant.id,
                            'wage': 'wage33', 'amount': Task.project_id.wage33 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                            'date_set': Task.date4_date or Task.date6_date,
                        })
                if Task.date7_date:
                    TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage34')])
                    if not TaskWageS:
                        self.env['project.task.wage'].sudo().create({
                            'task_id': Task.id, 'user_id': Task.consultant.id,
                            'wage': 'wage34', 'amount': Task.project_id.wage34 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                            'date_set': Task.date7_date,
                        })
                if Task.date9_date or Task.date10_date:
                    TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage35')])
                    if not TaskWageS:
                        self.env['project.task.wage'].sudo().create({
                            'task_id': Task.id, 'user_id': Task.consultant.id,
                            'wage': 'wage35', 'amount': Task.project_id.wage35 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                            'date_set': Task.date9_date or Task.date10_date,
                        })
                if Task.control and (Task.control == 'followup' or Task.control == 'builtinprocess'):
                    if Task.date12_date and Task.date13_date and Task.date14_date and Task.date15_date:
                        TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage36')])
                        if not TaskWageS:
                            self.env['project.task.wage'].sudo().create({
                                'task_id': Task.id, 'user_id': Task.consultant.id,
                                'wage': 'wage36', 'amount': Task.project_id.wage36 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                'date_set': Task.date15_date,
                            })
                else:
                    if Task.date12_date and Task.date13_date and Task.date14_date:
                        TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage36')])
                        if not TaskWageS:
                            self.env['project.task.wage'].sudo().create({
                                'task_id': Task.id, 'user_id': Task.consultant.id,
                                'wage': 'wage36', 'amount': Task.project_id.wage36 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                'date_set': Task.date14_date,
                            })
                # Amennyiben közbeszerzési részek vannak, közbeszerzési részenként
                if Task.nops > 1:
                    if Task.date3_date:
                        TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage37')])
                        if not TaskWageS:
                            self.env['project.task.wage'].sudo().create({
                                'task_id': Task.id, 'user_id': Task.consultant.id,
                                'wage': 'wage37', 'amount': Task.project_id.wage37 * Task.nops * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                'date_set': Task.date3_date,
                            })
                    if Task.date5_date:
                        TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage38')])
                        if not TaskWageS:
                            self.env['project.task.wage'].sudo().create({
                                'task_id': Task.id, 'user_id': Task.consultant.id,
                                'wage': 'wage38', 'amount': Task.project_id.wage38 * Task.nops * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                'date_set': Task.date5_date,
                            })
                    if Task.date4_date or Task.date6_date:
                        TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage39')])
                        if not TaskWageS:
                            self.env['project.task.wage'].sudo().create({
                                'task_id': Task.id, 'user_id': Task.consultant.id,
                                'wage': 'wage39', 'amount': Task.project_id.wage39 * Task.nops * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                'date_set': Task.date4_date or Task.date6_date,
                            })
                    if Task.date7_date:
                        TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage40')])
                        if not TaskWageS:
                            self.env['project.task.wage'].sudo().create({
                                'task_id': Task.id, 'user_id': Task.consultant.id,
                                'wage': 'wage40', 'amount': Task.project_id.wage40 * Task.nops * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                'date_set': Task.date7_date,
                            })
                    if Task.date9_date or Task.date10_date:
                        TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage41')])
                        if not TaskWageS:
                            self.env['project.task.wage'].sudo().create({
                                'task_id': Task.id, 'user_id': Task.consultant.id,
                                'wage': 'wage41', 'amount': Task.project_id.wage41 * Task.nops * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                'date_set': Task.date9_date or Task.date10_date,
                            })
                    if Task.control and (Task.control == 'followup' or Task.control == 'builtinprocess'):
                        if Task.date12_date and Task.date13_date and Task.date14_date and Task.date15_date:
                            TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage42')])
                            if not TaskWageS:
                                self.env['project.task.wage'].sudo().create({
                                    'task_id': Task.id, 'user_id': Task.consultant.id,
                                    'wage': 'wage42', 'amount': Task.project_id.wage42 * Task.nops * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                    'date_set': Task.date15_date,
                                })
                    else:
                        if Task.date12_date and Task.date13_date and Task.date14_date:
                            TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage42')])
                            if not TaskWageS:
                                self.env['project.task.wage'].sudo().create({
                                    'task_id': Task.id, 'user_id': Task.consultant.id,
                                    'wage': 'wage42', 'amount': Task.project_id.wage42 * Task.nops * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                    'date_set': Task.date14_date,
                                })
                # Uniós eljárásrend alkalmazása esetén (tehát ha az eljárásrend uniós és nem a becsült érték)
                if Task.procedure == 'union':
                    if Task.date3_date:
                        TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage43')])
                        if not TaskWageS:
                            self.env['project.task.wage'].sudo().create({
                                'task_id': Task.id, 'user_id': Task.consultant.id,
                                'wage': 'wage43', 'amount': Task.project_id.wage43 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                'date_set': Task.date3_date,
                            })
                    if Task.date5_date:
                        TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage44')])
                        if not TaskWageS:
                            self.env['project.task.wage'].sudo().create({
                                'task_id': Task.id, 'user_id': Task.consultant.id,
                                'wage': 'wage44', 'amount': Task.project_id.wage44 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                'date_set': Task.date5_date,
                            })
                    if Task.date4_date or Task.date6_date:
                        TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage45')])
                        if not TaskWageS:
                            self.env['project.task.wage'].sudo().create({
                                'task_id': Task.id, 'user_id': Task.consultant.id,
                                'wage': 'wage45', 'amount': Task.project_id.wage45 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                'date_set': Task.date4_date or Task.date6_date,
                            })
                    if Task.date7_date:
                        TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage46')])
                        if not TaskWageS:
                            self.env['project.task.wage'].sudo().create({
                                'task_id': Task.id, 'user_id': Task.consultant.id,
                                'wage': 'wage46', 'amount': Task.project_id.wage46 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                'date_set': Task.date7_date,
                            })
                    if Task.date9_date or Task.date10_date:
                        TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage47')])
                        if not TaskWageS:
                            self.env['project.task.wage'].sudo().create({
                                'task_id': Task.id, 'user_id': Task.consultant.id,
                                'wage': 'wage47', 'amount': Task.project_id.wage47 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                'date_set': Task.date9_date or Task.date10_date,
                            })
                    if Task.control and (Task.control == 'followup' or Task.control == 'builtinprocess'):
                        if Task.date12_date and Task.date13_date and Task.date14_date and Task.date15_date:
                            TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage48')])
                            if not TaskWageS:
                                self.env['project.task.wage'].sudo().create({
                                    'task_id': Task.id, 'user_id': Task.consultant.id,
                                    'wage': 'wage48', 'amount': Task.project_id.wage48 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                    'date_set': Task.date15_date,
                                })
                    else:
                        if Task.date12_date and Task.date13_date and Task.date14_date:
                            TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage48')])
                            if not TaskWageS:
                                self.env['project.task.wage'].sudo().create({
                                    'task_id': Task.id, 'user_id': Task.consultant.id,
                                    'wage': 'wage48', 'amount': Task.project_id.wage48 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                    'date_set': Task.date14_date,
                                })
                # Ha a közbeszerzési eljárás jogszabályban előírt utóellenőrzés hatálya alá tartozik
                if Task.control and Task.control == 'followup':
                    if Task.date3_date:
                        TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage49')])
                        if not TaskWageS:
                            self.env['project.task.wage'].sudo().create({
                                'task_id': Task.id, 'user_id': Task.consultant.id,
                                'wage': 'wage49', 'amount': Task.project_id.wage49 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                'date_set': Task.date3_date,
                            })
                    if Task.date5_date:
                        TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage50')])
                        if not TaskWageS:
                            self.env['project.task.wage'].sudo().create({
                                'task_id': Task.id, 'user_id': Task.consultant.id,
                                'wage': 'wage50', 'amount': Task.project_id.wage50 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                'date_set': Task.date5_date,
                            })
                    if Task.date4_date or Task.date6_date:
                        TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage51')])
                        if not TaskWageS:
                            self.env['project.task.wage'].sudo().create({
                                'task_id': Task.id, 'user_id': Task.consultant.id,
                                'wage': 'wage51', 'amount': Task.project_id.wage51 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                'date_set': Task.date4_date or Task.date6_date,
                            })
                    if Task.date7_date:
                        TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage52')])
                        if not TaskWageS:
                            self.env['project.task.wage'].sudo().create({
                                'task_id': Task.id, 'user_id': Task.consultant.id,
                                'wage': 'wage52', 'amount': Task.project_id.wage52 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                'date_set': Task.date7_date,
                            })
                    if Task.date9_date or Task.date10_date:
                        TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage53')])
                        if not TaskWageS:
                            self.env['project.task.wage'].sudo().create({
                                'task_id': Task.id, 'user_id': Task.consultant.id,
                                'wage': 'wage53', 'amount': Task.project_id.wage53 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                'date_set': Task.date9_date or Task.date10_date,
                            })
                    if Task.control and (Task.control == 'followup' or Task.control == 'builtinprocess'):
                        if Task.date12_date and Task.date13_date and Task.date14_date and Task.date15_date:
                            TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage54')])
                            if not TaskWageS:
                                self.env['project.task.wage'].sudo().create({
                                    'task_id': Task.id, 'user_id': Task.consultant.id,
                                    'wage': 'wage54', 'amount': Task.project_id.wage54 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                    'date_set': Task.date15_date,
                                })
                    else:
                        if Task.date12_date and Task.date13_date and Task.date14_date:
                            TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage54')])
                            if not TaskWageS:
                                self.env['project.task.wage'].sudo().create({
                                    'task_id': Task.id, 'user_id': Task.consultant.id,
                                    'wage': 'wage54', 'amount': Task.project_id.wage54 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                    'date_set': Task.date14_date,
                                })
                # Ha a közbeszerzési eljárás jogszabályban előírt folyamatba épített ellenőrzés hatálya alá tartozik
                if Task.control and Task.control == 'builtinprocess':
                    if Task.date2_date:
                        TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage55')])
                        if not TaskWageS:
                            self.env['project.task.wage'].sudo().create({
                                'task_id': Task.id, 'user_id': Task.consultant.id,
                                'wage': 'wage55', 'amount': Task.project_id.wage55 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                'date_set': Task.date2_date,
                            })
                    if Task.date5_date:
                        TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage56')])
                        if not TaskWageS:
                            self.env['project.task.wage'].sudo().create({
                                'task_id': Task.id, 'user_id': Task.consultant.id,
                                'wage': 'wage56', 'amount': Task.project_id.wage56 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                'date_set': Task.date5_date,
                            })
                    if Task.date4_date or Task.date6_date:
                        TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage57')])
                        if not TaskWageS:
                            self.env['project.task.wage'].sudo().create({
                                'task_id': Task.id, 'user_id': Task.consultant.id,
                                'wage': 'wage57', 'amount': Task.project_id.wage57 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                'date_set': Task.date4_date or Task.date6_date,
                            })
                    if Task.date7_date:
                        TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage58')])
                        if not TaskWageS:
                            self.env['project.task.wage'].sudo().create({
                                'task_id': Task.id, 'user_id': Task.consultant.id,
                                'wage': 'wage58', 'amount': Task.project_id.wage58 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                'date_set': Task.date7_date,
                            })
                    if Task.date9_date or Task.date10_date:
                        TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage59')])
                        if not TaskWageS:
                            self.env['project.task.wage'].sudo().create({
                                'task_id': Task.id, 'user_id': Task.consultant.id,
                                'wage': 'wage59', 'amount': Task.project_id.wage59 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                'date_set': Task.date9_date or Task.date10_date,
                            })
                    if Task.control and (Task.control == 'followup' or Task.control == 'builtinprocess'):
                        if Task.date12_date and Task.date13_date and Task.date14_date and Task.date15_date:
                            TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage60')])
                            if not TaskWageS:
                                self.env['project.task.wage'].sudo().create({
                                    'task_id': Task.id, 'user_id': Task.consultant.id,
                                    'wage': 'wage60', 'amount': Task.project_id.wage60 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                    'date_set': Task.date15_date,
                                })
                    else:
                        if Task.date12_date and Task.date13_date and Task.date14_date:
                            TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage60')])
                            if not TaskWageS:
                                self.env['project.task.wage'].sudo().create({
                                    'task_id': Task.id, 'user_id': Task.consultant.id,
                                    'wage': 'wage60', 'amount': Task.project_id.wage60 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                    'date_set': Task.date14_date,
                                })
                # Az eljárásban benyújtott részvételre jelentkezések számának megfelelően (jelentkezésenként)
                if Task.notsdtp:
                    if Task.date6_date:
                        TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage61')])
                        if not TaskWageS:
                            if Task.notsdtp and Task.notsdtp > 1:
                                amount = Task.project_id.wage61 * Task.notsdtp
                            else:
                                amount = Task.project_id.wage61
                            self.env['project.task.wage'].sudo().create({
                                'task_id': Task.id, 'user_id': Task.consultant.id,
                                'wage': 'wage61', 'amount': amount * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                'date_set': Task.date6_date,
                            })
                # Akkor érvényesül, ha a "Bírált ajánlatok száma" mező kitöltésre került.
                if Task.notsitp:
                    if Task.date9_date or Task.date10_date:
                        TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage62')])
                        if not TaskWageS:
                            self.env['project.task.wage'].sudo().create({
                                'task_id': Task.id, 'user_id': Task.consultant.id,
                                'wage': 'wage62', 'amount': Task.project_id.wage62 * (Task.notsitp or 1) * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                'date_set': Task.date9_date or Task.date10_date,
                            })
                # Akkor érvényesül, ha az "Értékelt ajánlatok száma" mező kitöltésre került.
                if Task.noooe:
                    if Task.date9_date or Task.date10_date:
                        TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage75')])
                        if not TaskWageS:
                            self.env['project.task.wage'].sudo().create({
                                'task_id': Task.id, 'user_id': Task.consultant.id,
                                'wage': 'wage75', 'amount': Task.project_id.wage75 * (Task.noooe or 1) * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                'date_set': Task.date9_date or Task.date10_date,
                            })
                # Akkor és annyiszor érvényesül, amikor és ahányszor a "Megtartott tárgyalás" mező(k) kitöltésre került(ek)
                ProjectTaskMeetingLogS = self.env['project.task.meeting.log'].search([('task_id', '=', Task.id)])
                if ProjectTaskMeetingLogS:
                    for ProjectTaskMeetingLog in ProjectTaskMeetingLogS:
                        TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage63'), ('meeting_log_id', '=', ProjectTaskMeetingLog.id)])
                        if not TaskWageS:
                            self.env['project.task.wage'].sudo().create({
                                'task_id': Task.id, 'user_id': Task.consultant.id,
                                'wage': 'wage63', 'amount': Task.project_id.wage63,
                                'date_set': ProjectTaskMeetingLog.date,
                                'meeting_log_id': ProjectTaskMeetingLog.id,
                            })
        # KFF ellenőrzés
        TaskS = self.env['project.task'].search([
            ('project_name', '=', 'KFF ellenőrzés'),
        ])
        if TaskS:
            for Task in TaskS:
                if Task.kff_task == 'quality':
                    if Task.date26_date:
                        TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage64')])
                        if not TaskWageS:
                            self.env['project.task.wage'].sudo().create({
                                'task_id': Task.id, 'user_id': Task.consultant.id,
                                'wage': 'wage64', 'amount': Task.project_id.wage64 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                'date_set': Task.date26_date,
                            })
                if Task.kff_task == 'regularity':
                    if Task.date26_date:
                        TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage65')])
                        if not TaskWageS:
                            self.env['project.task.wage'].sudo().create({
                                'task_id': Task.id, 'user_id': Task.consultant.id,
                                'wage': 'wage65', 'amount': Task.project_id.wage65 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                'date_set': Task.date26_date,
                            })
                if Task.kff_task == 'contractmodification':
                    if Task.date26_date:
                        TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage66')])
                        if not TaskWageS:
                            self.env['project.task.wage'].sudo().create({
                                'task_id': Task.id, 'user_id': Task.consultant.id,
                                'wage': 'wage66', 'amount': Task.project_id.wage66 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                'date_set': Task.date26_date,
                            })
        # Szerződésmódosítás
        TaskS = self.env['project.task'].search([
            ('project_name', '=', 'Szerződésmódosítás'),
        ])
        if TaskS:
            for Task in TaskS:
                if Task.date21_date and Task.date24_date:
                    TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage67')])
                    if not TaskWageS:
                        self.env['project.task.wage'].sudo().create({
                            'task_id': Task.id, 'user_id': Task.consultant.id,
                            'wage': 'wage67', 'amount': Task.project_id.wage67 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                            'date_set': Task.date24_date,
                        })
        # Versenyeztetés
        TaskS = self.env['project.task'].search([
            ('project_name', '=', 'Versenyeztetés'),
        ])
        if TaskS:
            for Task in TaskS:
                if Task.date23_date and Task.date24_date:
                    TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage68')])
                    if not TaskWageS:
                        self.env['project.task.wage'].sudo().create({
                            'task_id': Task.id, 'user_id': Task.consultant.id,
                            'wage': 'wage68', 'amount': Task.project_id.wage68 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                            'date_set': Task.date24_date,
                        })
        # PR, marketing
        TaskS = self.env['project.task'].search([
            ('project_name', '=', 'PR, marketing'),
        ])
        if TaskS:
            for Task in TaskS:
                if Task.date27_date and Task.date28_date and Task.date29_date:
                    if Task.pr_task and Task.pr_task == 'professional':
                        TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage69')])
                        if not TaskWageS:
                            self.env['project.task.wage'].sudo().create({
                                'task_id': Task.id, 'user_id': Task.user_id.id,
                                'wage': 'wage69', 'amount': Task.project_id.wage69 * self.env['hr.employee'].search([('user_id', '=', Task.user_id.id)], limit=1).wage_multiplier,
                                'date_set': Task.date29_date,
                            })
                    if Task.pr_task and Task.pr_task == 'other':
                        TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage70')])
                        if not TaskWageS:
                            self.env['project.task.wage'].sudo().create({
                                'task_id': Task.id, 'user_id': Task.user_id.id,
                                'wage': 'wage70', 'amount': Task.project_id.wage70 * self.env['hr.employee'].search([('user_id', '=', Task.user_id.id)], limit=1).wage_multiplier,
                                'date_set': Task.date29_date,
                            })
                    if Task.pr_task and Task.pr_task == 'photovideo':
                        TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage71')])
                        if not TaskWageS:
                            self.env['project.task.wage'].sudo().create({
                                'task_id': Task.id, 'user_id': Task.user_id.id,
                                'wage': 'wage71', 'amount': Task.project_id.wage71 * self.env['hr.employee'].search([('user_id', '=', Task.user_id.id)], limit=1).wage_multiplier,
                                'date_set': Task.date29_date,
                            })
        # Óradíjas feladatok
        TaskS = self.env['project.task'].search([
            ('project_name', '=', 'Óradíjas feladatok'),
        ])
        if TaskS:
            for Task in TaskS:
                LineS = self.env['account.analytic.line'].search([('task_id', '=', Task.id), ('coa', '=', True), ('include_in_colleaggue', '=', True)])
                if LineS:
                    for Line in LineS:
                        User = self.env['hr.employee'].browse(Line.employee_id.id).user_id
                        if User:
                            TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage72'), ('aal_id', '=', Line.id)])
                            if not TaskWageS:
                                if Line.foreign_language == True:
                                    amount = Task.project_id.wage72 * 2
                                else:
                                    amount = Task.project_id.wage72
                                self.env['project.task.wage'].sudo().create({
                                    'task_id': Task.id, 'user_id': User.id,
                                    'wage': 'wage72', 'amount': amount * Line.unit_amount * self.env['hr.employee'].search([('user_id', '=', User.id)], limit=1).wage_multiplier,
                                    'aal_id': Line.id,
                                    'date_set': Line.date,
                                })
        # Irodavezetői óradíjas feladatok
        TaskS = self.env['project.task'].search([
            ('project_name', '=', 'Irodavezetői óradíjas feladatok'),
        ])
        if TaskS:
            for Task in TaskS:
                LineS = self.env['account.analytic.line'].search([('task_id', '=', Task.id), ('coa', '=', True), ('include_in_colleaggue', '=', True)])
                if LineS:
                    for Line in LineS:
                        User = self.env['hr.employee'].browse(Line.employee_id.id).user_id
                        if User:
                            TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage73'), ('aal_id', '=', Line.id)])
                            if not TaskWageS:
                                self.env['project.task.wage'].sudo().create({
                                    'task_id': Task.id, 'user_id': User.id,
                                    'wage': 'wage73', 'amount': Task.project_id.wage73 * Line.unit_amount * self.env['hr.employee'].search([('user_id', '=', User.id)], limit=1).wage_multiplier,
                                    'aal_id': Line.id,
                                    'date_set': Line.date,
                                })
        # Óradíj / Eljárásokkal kapcsolatos óradíj
        TaskS = self.env['project.task'].search([
            ('project_name', 'not in', ['Óradíjas feladatok', 'Irodavezetői óradíjas feladatok']),
        ])
        if TaskS:
            for Task in TaskS:
                LineS = self.env['account.analytic.line'].search([('task_id', '=', Task.id), ('coa', '=', True), ('include_in_colleaggue', '=', True)])
                if LineS:
                    for Line in LineS:
                        User = self.env['hr.employee'].browse(Line.employee_id.id).user_id
                        if User:
                            TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage82'), ('aal_id', '=', Line.id)])
                            if not TaskWageS:
                                self.env['project.task.wage'].sudo().create({
                                    'task_id': Task.id, 'user_id': User.id,
                                    'wage': 'wage82', 'amount': Task.project_id.wage82 * Line.unit_amount * self.env['hr.employee'].search([('user_id', '=', User.id)], limit=1).wage_multiplier,
                                    'aal_id': Line.id,
                                    'date_set': Line.date,
                                })
        # DKÜ-s ellennőrzés
        TaskS = self.env['project.task'].search([
            ('project_name', '=', 'DKÜ-s ellennőrzés'),
        ])
        if TaskS:
            for Task in TaskS:
                # Minőségellenőrzés / KEF-es
                if Task.kff_task == 'quality' and Task.kef == 'kef':
                    if Task.date26_date:
                        TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage76')])
                        if not TaskWageS:
                            self.env['project.task.wage'].sudo().create({
                                'task_id': Task.id, 'user_id': Task.consultant.id,
                                'wage': 'wage76', 'amount': Task.project_id.wage76 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                'date_set': Task.date26_date,
                            })
                # Minőségellenőrzés / Nem KEF-es
                if Task.kff_task == 'quality' and Task.kef == 'nokef':
                    if Task.date26_date:
                        TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage78')])
                        if not TaskWageS:
                            self.env['project.task.wage'].sudo().create({
                                'task_id': Task.id, 'user_id': Task.consultant.id,
                                'wage': 'wage78', 'amount': Task.project_id.wage78 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                'date_set': Task.date26_date,
                            })
                # Szabályossági ellenőrzés / KEF-es
                if Task.kff_task == 'regularity' and Task.kef == 'kef':
                    if Task.date26_date:
                        TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage77')])
                        if not TaskWageS:
                            self.env['project.task.wage'].sudo().create({
                                'task_id': Task.id, 'user_id': Task.consultant.id,
                                'wage': 'wage77', 'amount': Task.project_id.wage77 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                'date_set': Task.date26_date,
                            })
                # Szabályossági ellenőrzés / Nem KEF-es
                if Task.kff_task == 'regularity' and Task.kef == 'nokef':
                    if Task.date26_date:
                        TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage79')])
                        if not TaskWageS:
                            self.env['project.task.wage'].sudo().create({
                                'task_id': Task.id, 'user_id': Task.consultant.id,
                                'wage': 'wage79', 'amount': Task.project_id.wage79 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                'date_set': Task.date26_date,
                            })
                # Szerződésmódosítás ellenőrzés
                if Task.kff_task == 'contractmodification':
                    if Task.date26_date:
                        TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage80')])
                        if not TaskWageS:
                            self.env['project.task.wage'].sudo().create({
                                'task_id': Task.id, 'user_id': Task.consultant.id,
                                'wage': 'wage80', 'amount': Task.project_id.wage80 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                'date_set': Task.date26_date,
                            })
                # Beszerzés
                if Task.kff_task == 'acquisition':
                    if Task.date26_date:
                        TaskWageS = self.env['project.task.wage'].search([('task_id', '=', Task.id), ('wage', '=', 'wage81')])
                        if not TaskWageS:
                            self.env['project.task.wage'].sudo().create({
                                'task_id': Task.id, 'user_id': Task.consultant.id,
                                'wage': 'wage81', 'amount': Task.project_id.wage81 * self.env['hr.employee'].search([('user_id', '=', Task.consultant.id)], limit=1).wage_multiplier,
                                'date_set': Task.date26_date,
                            })





class ProjectTaskWageCloseWizard(models.TransientModel):
    
    _name = 'project.task.wage.close.wizard'


    user_id = fields.Many2one('res.users', u'Tanácsadó', help=u'Ha nincs megadva, akkor mindenki!')
    accounting_date = fields.Date(u'Elszámolás időpontja', required=True)
    accounting_last_date = fields.Date(u'Utolsó dátum ami belekerül az elszámolásba', required=True)
    accounting_period_start = fields.Date(u'Elszámolási időszak kezdete', required=True)
    accounting_period_end = fields.Date(u'Elszámolási időszak vége', required=True)

    def action_close_wage(self):
        
        if self.user_id:
            sql = """
                SELECT DISTINCT(project_task_wage.user_id), hr_employee.id AS employee_id FROM project_task_wage
                JOIN hr_employee ON project_task_wage.user_id=hr_employee.user_id
                WHERE state='confirmed' AND project_task_wage.user_id = %s;
            """
            self.env.cr.execute(sql, [self.user_id.id])
        else:
            sql = """
                SELECT DISTINCT(project_task_wage.user_id), hr_employee.id AS employee_id FROM project_task_wage
                JOIN hr_employee ON project_task_wage.user_id=hr_employee.user_id
                WHERE state='confirmed';
            """
            self.env.cr.execute(sql)

        userS = self.env.cr.dictfetchall()
        
        for user in userS:
        
            employeeWage = self.env['hr.employee.wage'].sudo().create({
                'employee_id': user['employee_id'],
                'date': self.accounting_date,
                'accounting_period_start': self.accounting_period_start,
                'accounting_period_end': self.accounting_period_end,
            })

            wageS = self.env['project.task.wage'].sudo().search([('user_id', '=', user['user_id']), ('state', '=', 'confirmed'), ('create_date', '<=', self.accounting_last_date)])
            sum = 0
            for wage in wageS:
                wage.employee_wage_id = employeeWage.id
                wage.state = 'complete'
                wage.date_accounted = self.accounting_date
                sum += wage.amount

            Employee = self.env['hr.employee'].browse(user['employee_id'])
            employeeWage.sum = sum
            employeeWage.basic_wage = Employee['basic_wage']
            employeeWage.previous_sum = Employee['balance_previous']
            employeeWage.grand_total = employeeWage.sum + employeeWage.previous_sum
            if employeeWage.grand_total < employeeWage.basic_wage:
                employeeWage.payable = employeeWage.basic_wage
                employeeWage.next_base = employeeWage.grand_total - employeeWage.basic_wage
                Employee['balance_previous'] = employeeWage.next_base
            else:
                employeeWage.payable = employeeWage.grand_total
                employeeWage.next_base = 0
                Employee['balance_previous'] = 0

            employeeWage.state = 'created'





class ProjectTaskKmokState(models.Model):
    
    _name = 'project.task.kmok.state'
    _order = 'name'

    
    name = fields.Char(u'Közbeszerzési eljárás állapota (státuszkódok)')
