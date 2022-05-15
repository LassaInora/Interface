import asyncio
import time
from subprocess import Popen, PIPE
from typing import Union


class Interface:
    def __init__(self):
        with Popen(r'Netsh WLAN show interfaces', stdout=PIPE, stderr=PIPE) as p:
            output, errors = p.communicate()
        lines = output.decode('ansi').splitlines()[2:]

        infos = ""
        self.infos = ""

        for line in lines:
            if line.startswith('    '):
                line = line[4:]
            aff = list(line)
            for char in aff:
                match char:
                    case 'Š':
                        lettre = 'è'
                    case 'ÿ':
                        lettre = ' '
                    case '‚':
                        lettre = 'é'
                    case '':
                        lettre = 'É'
                    case '?':
                        lettre = ''
                    case _:
                        lettre = char

                if lettre != ' ' or infos[-1] != ' ':
                    infos += lettre
                    self.infos += lettre

            if infos.split('\n')[-1].startswith('État du réseau hébergé: '):
                self.etat_reseau_heberge = self.infos.split('État du réseau hébergé: ')[1].split('§')[0]
                mem = ""
                for line in infos.splitlines()[:-1]:
                    mem += line + "\n"
                infos = mem

                mem = ""
                for line in self.infos.splitlines()[:-1]:
                    mem += line + "\n"
                self.infos = mem


            if infos.split('\n')[-1].startswith("Statut de la radio : ") and infos[-1] != ',':
                infos += ","
                self.infos += ","
            else:
                if len(infos) > 0 and infos[-1] == ',':
                    infos = infos[:-1]
                if len(infos) > 0:
                    if infos[-1] == '\n':
                        infos += "\n"
                    else:
                        infos += "§\n"

        self.liste_infos = infos.split('\n\n')
        self.liste_infos.pop(-1)

        self.connexions = []
        for infos_connexion in self.liste_infos:
            if len(infos_connexion) > 0:
                self.connexions.append(Connexion(infos_connexion))

    def __str__(self):
        texte = f"\nInterface réseau:\n" \
                f"\tNombre de connexion: {len(self.connexions)}\n" \
                f"\tÉtat du réseau hébergé: {self.etat_reseau_heberge}"

        if len(self.connexions) > 0:
            texte += "\n"
            for connect in self.connexions:
                texte += "\n\n"
                texte += str(connect)

        return texte


class Connexion:
    def __init__(self, infos: str):
        for ligne in infos.splitlines():
            if ligne.startswith('Nom : '):
                self.nom = ligne.split('Nom : ')[1].split('§')[0]
            elif ligne.startswith('Description : '):
                self.carte_reseau = ligne.split('Description : ')[1].split('§')[0]
            elif ligne.startswith('GUID : '):
                self.guid = ligne.split('GUID : ')[1].split('§')[0]
            elif ligne.startswith('Adresse physique : '):
                self.adresse_mac = ligne.split('Adresse physique : ')[1].split('§')[0]
            elif ligne.startswith('État : '):
                self.etat = ligne.split('État : ')[1].split('§')[0]
            elif ligne.startswith('SSID : '):
                self.ssid = ligne.split('SSID : ')[1].split('§')[0]
            elif ligne.startswith('BSSID : '):
                self.adresse_mac_routeur = ligne.split('BSSID : ')[1].split('§')[0]
            elif ligne.startswith('Type de réseau : '):
                self.type_reseau = ligne.split('Type de réseau : ')[1].split('§')[0]
            elif ligne.startswith('Type de radio : '):
                self.type_radio = ligne.split('Type de radio : ')[1].split('§')[0]
            elif ligne.startswith('Authentification : '):
                self.securite = ligne.split('Authentification : ')[1].split('§')[0]
            elif ligne.startswith('Chiffrement : '):
                self.chiffrement = ligne.split('Chiffrement : ')[1].split('§')[0]
            elif ligne.startswith('Mode de connexion : '):
                self.mode_connexion = ligne.split('Mode de connexion : ')[1].split('§')[0]
            elif ligne.startswith('Canal : '):
                self.canal = int(ligne.split('Canal : ')[1].split('§')[0])
            elif ligne.startswith('Réception (Mbits/s) : '):
                self.debit_reception = float(ligne.split('Réception (Mbits/s) : ')[1].split('§')[0])
            elif ligne.startswith('Transmission (Mbits/s) : '):
                self.debit_transmission = float(ligne.split('Transmission (Mbits/s) : ')[1].split('§')[0])
            elif ligne.startswith('Signal : '):
                self.force_signal = int(ligne.split('Signal : ')[1].split('§')[0][:-2]) / 100
            elif ligne.startswith('Profil : '):
                self.nom_reseau = ligne.split('Profil : ')[1].split('§')[0]
            elif ligne.startswith('Statut de la radio : '):
                self.statut_radio = ligne.split('Statut de la radio : ')[1].split('§')[0].split(', ')

    def get_me(self, an_interface: Interface) -> None | object:
        """
        Récupère l'instance correspondant à la variable Connexion actuel
        :param an_interface : L'interface où chercher l'instance Connexion
        :return : L'instance correspondant à la variable Connexion actuel ou None
        """
        for connect in an_interface.connexions:
            if self.nom == connect.nom:
                return connect
        return None

    def speedtest(self, duree: int = 60) -> str:
        """
        Test de la vitesse de la connexion.
        :param duree: Durée du test en secondes.
        :return: String avec la force du signal et le débit moyen
        """
        def moyenne(liste: list[Union[int, float]]) -> float:
            return sum(liste) / len(liste)

        def test(duree: int, mode: str) -> list[float]:
            debit = []
            force = []
            for t in range(duree):
                now: Connexion = self.get_me(Interface())
                if mode == 'transmission':
                    debit.append(now.debit_transmission)
                else:
                    debit.append(now.debit_reception)
                force.append(now.force_signal)
                print(end='\r')
                print(f""
                      f"[{'#' * int(t * 100 / duree) + ' ' * int(100 - (t * 100 / duree))}] "
                      f"Débit de {mode}: {debit[-1]} Mbits/s "
                      f"(Signal : {int(now.force_signal * 10000) / 100}%)",
                      end='')
                time.sleep(1)
            print(end='\r')
            return [moyenne(debit), moyenne(force)]

        reception, force_r = test(round(duree/2), 'reception')
        transmission, force_t = test(round(duree/2), 'transmission')
        force = int(moyenne([force_t, force_r]) * 10000) / 100

        return f"Force moyen du signal      : {force}%\n" \
               f"Débit moyen de reception au routeur   : {reception} Mbits/s\n" \
               f"Débit moyen de transmission au routeur: {transmission} Mbits/s"

    async def async_speedtest(self, duree: int = 60) -> str:
        """
        Test de la vitesse de la connexion de façon asynchrone.
        :param duree: Durée du test en secondes.
        :return: String avec la force du signal et le débit moyen
        """
        def moyenne(liste: list[Union[int, float]]) -> float:
            return sum(liste) / len(liste)

        async def test(duree: int, mode: str) -> list[float]:
            debit = []
            force = []
            for t in range(duree):
                now: Connexion = self.get_me(Interface())
                if mode == 'transmission':
                    debit.append(now.debit_transmission)
                else:
                    debit.append(now.debit_reception)
                force.append(now.force_signal)
                await asyncio.sleep(1)
            return [moyenne(debit), moyenne(force)]

        transmission, force_t = await test(round(duree/2), 'transmission')
        reception, force_r = await test(round(duree/2), 'reception')
        force = int(moyenne([force_t, force_r]) * 10000) / 100

        return f"Force moyen du signal                    : {force}%\n" \
               f"Débit moyen de reception au routeur      : {reception} Mbits/s\n" \
               f"Débit moyen de transmission au routeur   : {transmission} Mbits/s"

    def __str__(self):
        def ignore(_):
            pass

        text = f"\n = - = - == {str(self.nom)} == - = - = \n\n"

        # == - = - = - == Info carte réseau == - = - = - == #
        ok = 0
        prepare = ""
        try:
            prepare = "\tGUID: " + str(self.guid) + "\n" + prepare
            ok += 1
        except Exception as e:
            ignore(e)
        try:
            prepare = "\tAdresse MAC: " + str(self.adresse_mac) + "\n" + prepare
            ok += 1
        except Exception as e:
            ignore(e)
        try:
            prepare = "\tModèle de la carte: " + str(self.carte_reseau) + "\n" + prepare
            ok += 1
        except Exception as e:
            ignore(e)
        if ok > 0:
            prepare = "\nInfo carte réseau: " + "\n" + prepare

        text += prepare

        # == - = - = - == Info connexion == - = - = - == #
        ok = 0
        prepare = ""
        try:
            statut = ""
            for stat_radio in self.statut_radio:
                statut += "\n\t\t - " + stat_radio

            prepare = "\tStatut de la radio: " + statut + "\n" + prepare
            ok += 1
        except Exception as e:
            ignore(e)
        try:
            prepare = "\tType de radio: " + str(self.type_radio) + "\n" + prepare
            ok += 1
        except Exception as e:
            ignore(e)
        try:
            prepare = "\tType de réseau: " + str(self.type_reseau) + "\n" + prepare
            ok += 1
        except Exception as e:
            ignore(e)
        try:
            prepare = "\tCanal: " + str(self.canal) + "\n" + prepare
            ok += 1
        except Exception as e:
            ignore(e)
        try:
            prepare = "\tMode de connexion: " + str(self.mode_connexion) + "\n" + prepare
            ok += 1
        except Exception as e:
            ignore(e)
        if ok > 0:
            prepare = "\nInfo connexion: " + "\n" + prepare

        text += prepare

        # == - = - = - == Info routeur == - = - = - == #
        ok = 0
        prepare = ""
        try:
            prepare = "\tChiffrement: " + str(self.chiffrement) + "\n" + prepare
            ok += 1
        except Exception as e:
            ignore(e)
        try:
            prepare = "\tSécurité: " + str(self.securite) + "\n" + prepare
            ok += 1
        except Exception as e:
            ignore(e)
        try:
            prepare = "\tNom du réseau: " + str(self.nom_reseau) + "\n" + prepare
            ok += 1
        except Exception as e:
            ignore(e)
        try:
            prepare = "\tSSID: " + str(self.ssid) + "\n" + prepare
            ok += 1
        except Exception as e:
            ignore(e)
        try:
            prepare = "\tAdresse MAC: " + str(self.adresse_mac_routeur) + "\n" + prepare
            ok += 1
        except Exception as e:
            ignore(e)
        if ok > 0:
            prepare = "\nInfo routeur: " + "\n" + prepare

        text += prepare

        # == - = - = - == Info signal == - = - = - == #
        ok = 0
        prepare = ""
        try:
            prepare = "\tTransmission: " + str(self.debit_transmission) + "Mbits/s\n" + prepare
            ok += 1
        except Exception as e:
            ignore(e)
        try:
            prepare = "\tRéception: " + str(self.debit_reception) + "Mbits/s\n" + prepare
            ok += 1
        except Exception as e:
            ignore(e)
        try:
            prepare = "\tForce du signal: " + str(self.force_signal * 100) + "%\n" + prepare
            ok += 1
        except Exception as e:
            ignore(e)
        try:
            prepare = "\tÉtat: " + str(self.etat) + "\n" + prepare
            ok += 1
        except Exception as e:
            ignore(e)
        if ok > 0:
            prepare = "\nInfo signal: " + "\n" + prepare

        text += prepare

        return text


if __name__ == '__main__':
    interface = Interface()
    print(interface)
