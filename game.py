#imports
import main
import palavras
from random import randint
from google.appengine.ext import ndb

class GameState(ndb.Model):
    State = ndb.BooleanProperty(indexed=False, default=False)

def setGame(chat_id, bool):
    es = GameState.get_or_insert(str(chat_id))
    es.State = bool
    es.put()

def getGame(chat_id):
    es = GameState.get_by_id(str(chat_id))
    if es:
        return es.State
    return False

class Players(ndb.Model):
    jogadores = [ndb.StringProperty(indexed=False, default=False)]
    nomes = [ndb.StringProperty(indexed=False, default=False)]

def addPlayer(chat_id, uId, uName):
    es = Players.get_or_insert(str(chat_id))
    es.jogadores.append(uId)
    es.nomes.append(uName)
    es.put()

def getPlayer(chat_id,uId):
    es = Players.get_by_id(str(chat_id))
    pos = es.jogadores.index(uId)
    nome = es.jogadores[pos]
    return nome

class Jogo:
    update = palavras.update_list
    update(palavras.palavras, palavras.dicas)
    palavra = palavras.get_palavra(randint(0,2))

    def comandos(self, uId, uName, chat_id, text):
        state = getGame(chat_id)
        if text.startswith('/'):
            if text.startswith('/newgame') or text.startswith('/newgame@forca_bot'):
                if state:
                    str1 = 'Comecando um novo jogo!'
                    setGame(chat_id,True)
                    str2 = 'Vamos comecar definindo os jogadores? Quem quiser participar do jogo envie um /entrar :D'
                    rpl = [str1, str2]
                    #Continuar
                else:
                    str1 = 'Existe um jogo em andamento neste chat!\nCaso voce queira abandonar ele use o comando /cancelar_jogo'
                    rpl = [str1]
            elif text.startswith('/entrar') or text.startswith('/entrar@forca_bot'):
                    str1 = 'Certo, '+uName+' voce vai participar do jogo'
                    rpl = [str1]
            elif text.startswith('/help') or text.startswith('/help@forca_bot'):
                str1 = 'Sou o Forca_bot, para comecar um jogo use o comando /newgame\nnao sei se vou dar toda a help aqui ou varias helps dependendo do contexto'
                rpl = [str1]
        else:
            rpl = ['oi']
        #for i in range(0, len(rpl)):
        #    print rpl[i]
        return rpl
