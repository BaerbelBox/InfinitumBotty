import random
import time
from FaustBot.Communication import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype

jokes = [['Was ist orange und geht über die Berge?'
,'Eine Wanderine.']
,['Was ist orange und schaut durchs Schlüsselloch?'
,'Eine Spannderine.']
,['Was ist violett und sitzt in der Kirche ganz vorne?'
,'Eine Frommbeere.']
,['Was ist grün und liegt im Sarg?'
,'Ein Sterbschen.']
,['Was ist bunt und läuft über den Tisch davon?'
,'Ein Fluchtsalat.']
,['Was ist braun und schwimmt im Wasser?'
,'Ein U-Brot.']
,['Was ist schwarz/weiß und hüpft von Eisscholle zu Eisscholle?'
,'Ein Springuin.']
,['Was ist rot und sitzt auf dem WC?'
,'Eine Klomate!']
,['Was ist braun und fährt einen verschneiten Hang hinunter?'
,'Ein Snowbrot.']
,['Was ist braun und späht durchs Schlafzimmerfenster?'
,'Ein Spannzapfen.']
,['Was ist weiß und springt im Wald umher?'
,'Ein Jumpignon.']
,['Was ist braun, süß und rennt durch den Wald?'
,'Eine Joggolade.']
,['Was ist braun und sitzt hinter Gittern?'
,'Eine Knastanie.']
,['Was ist rot, rund und hat ein Maschinengewehr?'
,'Ein Rambodischen.']
,['Was ist braun, knusprig und läuft mit dem Korb durch den Wald?'
,'Brotkäppchen.']
,['Was ist braun, klebrig und läuft in der Wüste umher?'
,'Ein Karamel.']
,['Was ist rot, sitzt in einer Konservendose und spielt Musik?'
,'Ein Radioli.']
,['Was ist grün und radelt durch die Gegend?'
,'Eine Velone.']
,['Was ist orange, tiefergelegt und hat einen Spoiler?'
,'Ein Mantarinchen']
,['Was ist gelb, krumm und schwimmt auf dem Wasser?'
,'Eine Schwanane']
,['Was ist orange und steckt traurig in der Erde?'
,'Ein Trübchen.']
,['Was ist orange, sauer und kann keine Minute ruhig sitzen?'
,'Eine Zappelsine.']
,['Was ist haarig und wird in der Pfanne frittiert?'
,'Bartkartoffeln.']
,['Was ist gesund und kräftig und spielt den Beleidigten?'
,'Ein Schmollkornbrot.']
,['Was steht im Schlafzimmer des Metzgers neben dem Bett?'
,'Ein Schlachttischlämpchen.']
,['Was ist grün, sauer und versteckt sich vor der Polizei?'
,'Ein Essig-Schurke.']
,['Was ist orange, rund und versteckt sich vor der Polizei?'
,'Ein Vandalinchen.']
,['Was ist grün und schaut durchs Schlüsselloch?'
,'Ein Spionat']
,['Was ist groß, grau und telefoniert aus Afrika?'
,'Ein Telefant.']
,['Was ist gelb und flattert im Wind?'
,'Eine Fahnane.']
,['Was ist grün und klopft an die Tür?'
,'Ein Klopfsalat.']
,['Was ist braun, sehr zäh und fliegt umher?'
,'Eine Ledermaus.']
,['Was macht "Muh" und hilft beim Anziehen?'
,'Ein Kuhlöffel.']
,['Was ist viereckig, hat Noppen und einen Sprachfehler?'
,'Ein Legosteniker.']
,['Was ist gelb und immer bekifft?'
,'Ein Bong-Frites.']
,['Was ist grün, glücklich und hüpft von Grashalm zu Grashalm?'
,'Eine Freuschrecke.']
,['Was ist ist braun, hat einen Beutel und hängt am Baum?'
,'Ein Hänguruh.']
,['Was ist orange-rot und riskiert alles?'
,'Eine Mutorange']
,['Was ist gelb, ölig und und sitzt in der Kirche in der ersten Reihe?'
,'Eine Frommfrites']
,['Was ist grün und irrt durch Istanbul?'
,'Ein Gürke']
,['Was ist hellbraun und hangelt sich von Tortenstück zu Tortenstück?'
,'Ein Tarzipan.']
,['Was ist braun und klebt an der Wand?'
,'Ein Klebkuchen']
,['Was ist rot und läuft die Straße auf und ab?'
,'Eine Hagenutte.']
,['Was ist weiss und läuft die Straße auf und ab?'
,'Schneeflittchen.']
,['Was ist grün und läuft die Straße auf und ab?'
,'Eine Frosch-tituierte.']
,['Was ist braun und trägt Strapse?'
,'Ein Haselnüttchen.']
,['Was ist gelb und steht frankiert und abgestempelt am Strassenrand?'
,'Eine Postituierte.']
,['Was leuchtet und geht fremd?'
,'Ein Schlampion.']
,['Was ist gelb und rutscht den Hang hinunter?'
,'Ein Cremeschlitten.']
,['Was ist weiss und tanzt ums Feuer?'
,'Rumpelpilzchen.']
,['Was ist weiss und liegt schnarchend auf der Wiese?'
,'Ein Schlaf.']
,['Was ist gelb, saftig und sitzt bei jedem Fussballspiel vor dem Fernseher?'
,'Eine Fananas.']
,['Was ist rosa und schwimmt im Wasser?'
,'Eine Meerjungsau.']
,['Was ist durchsichtig, stinkt und es ist ihm alles egal?'
,'Ein Schnurz.']
,['Was ist unordentlich und gibt Licht?'
,'Eine Schlampe.']
,['Was ist blöd, süß und bunt?'
,'Ein Dummibärchen.']
,['Was trägt einen Frack und hilft im Haushalt?'
,'Ein Diener Schnitzel.']
,['Was ist silbrig, sticht und hat Spass daran?'
,'Eine Sadistel.']
,['Was ist gelb und kann schießen?'
,'Eine Banone']
,['Was kommt nach Elch?'
,'Zwölch']
,['Was liegt am Strand und spricht undeutlich?'
,'Eine Nuschel']
,['Was hüpft über die Wiese und raucht?'
,'Ein Kaminchen']
,['Was ist knusprig und liegt unterm Baum?'
,'Schattenplätzle']
,['Kleines Schwein das nach Hilfe schreit?'
,'Ein Notrufsäule']
,['Was liegt am Strand und hat Schnupfen?'
,'Eine Niesmuschel']
,['Was ist ein Cowboy ohne Pferd?'
,'Ein Sattelschlepper']
,['Was ist grün und trägt Kopftuch?'
,'Eine Gürkin']
,['Was ist rot und sitzt unterm Tisch?'
,'Ne Paprikantin']
,['Was ist schwarz-weiß und kommt nicht vom Fleck?'
,'Ein Klebra']
,['Was ist rosa, quiekt und wird zum Hausbau verwendet?'
,'Ein Ziegelschwein']
,['Wer ist bei jeder Wanderung betrunken?'
,'Der Schlucksack']
,['Was ist rot und wiehert?'
,'Die Pferdbeere']
,['Was ist weiß, blau, grün und steht auf der Wiese?'
,'Eine Schlumpfdotterblume']
,['Was kaut und hat immer Verspätung?'
,'Die Essbahn']
,['Was fährt unter der Erde und macht Muh?'
,'Die Kuhbahn']
,['Was wühlt den Himmel auf?'
,'Ein Pflugzeug']
,['Welche Frucht wächst im Gerichtssaal?'
,'Advokado']
,['Wie nennt man einen “scharfen” Mann mit Kilt?'
,'Chilischotte']
,['Was lebt im Meer und kann gut rechnen?'
,'Der Octoplus']
,['Was ist tiefergelegt und schwimmt unter wasser?'
,'Der Tunefisch']
,['Was ist unter der Erde und stinkt?'
,'Eine Furzel']
,['Von was wird man nachts beobachtet?'
,'Vom Spannbettlaken']
,['Wo wohnen die meisten Katzen?'
,'Im Miezhaus']
,['Warum ging der Luftballon kaputt?'
,'Aus Platzgründen']
,['Wie nennt man einen ausgehungerten Frosch?'
,'Magerquak']
,['Was macht ein Dieb im Zirkus?'
,'Clown']
,['Was macht ein Clown im Büro?'
,'Faxen']
,['Wie nennt man eine Zauberin in der Wüste?'
,'Sand Witch']
,['Wo betrinkt sich eine Mücke?'
,'In Sekt']
,['Warum können Seeräuber keine Kreise berechnen?'
,'Weil sie pi raten']
,['Was sitzt in der Savanne und wäscht sich?'
,'Die Hygiäne']
,['Was sitzt im Dschungel und spielt unfair?'
,'Mogli']
,['Wie nennt man den Paarungsruf von Leutstofflampen?'
,'Neonröhren']]


class JokeObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".joke"]

    @staticmethod
    def help():
        return ".joke erzählt einen Flachwitz"

    def update_on_priv_msg(self, data: dict, connection: Connection):
        if data['message'].find('.joke') == -1:
            return
        joke = random.choice(jokes)
        connection.send_back(joke[0], data)
        time.sleep(30)
        connection.send_back(joke[1], data)
