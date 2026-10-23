#!/usr/bin/env python3
"""Reviewed Mafia dialogue source; wraps native text and preserves script controls."""
from pathlib import Path
import os
os.chdir(Path(__file__).resolve().parents[2])
import sys,json,re,collections
sys.path.insert(0,str(Path.cwd()/'tools/yokai'))
from cadrer_dialogues_fr import wrap,measure
from localiser_fr import replace,controls
rows={}
def add(m,label,text):rows[('data/maps/'+m+'/text.inc',m+'_Text_'+label if not label.startswith('Text_') else label)]=text if text.endswith('$') else text+'$'
def block(m,text):
 for line in text.strip().splitlines():
  k,t=line.split('|',1);add(m,k,t)
def triples(m,text):
 for line in text.strip().splitlines():
  k,a,b,c=line.split('|');
  for suf,t in zip(['Intro','Defeat','PostBattle'],[a,b,c]):add(m,k+suf,t)
triples('MtMoon_B2F',r'''
Grunt1|Ces fossiles sont réservés à la Mafiamille. Le Don sait reconnaître un bon placement!|Tu as fait échouer l'affaire!|Un fossile ne rapporte rien si tu le gardes pour toi. Réfléchis un peu!
Grunt2|La Mafiamille mène les fouilles. Tu peux repartir... ou tenter de passer.|Je n'avais pas prévu ça!|Mes collègues ne seront pas aussi conciliants. Enfin, j'espère.
Grunt3|Une grosse affaire se prépare ici. Les curieux restent dehors!|Tu sais te défendre...|Un fossile dans ton sac? On pourrait s'arranger. Non? Tant pis.
Grunt4|Les affaires de la famille ne regardent pas les enfants!|Ça va mal finir... pour moi.|Les Yo-kai vivaient ici bien avant nous. Le Don s'intéresse à leurs secrets.
''')
block('CeruleanCity',r'''
GruntIntro|Hé! Ce passage est privé!\pMoi, un cambrioleur? La Mafiamille préfère parler de récupération.{PLAY_BGM}{MUS_ENCOUNTER_ROCKET}
GruntDefeat|D'accord, je rends la CT! On évite de prévenir le Don?
RecoveredTM28FromGrunt|{PLAYER} récupère la CT28 dérobée par le sbire Mafiamille.
PeopleHereWereRobbed|Cette maison a été cambriolée. La Mafiamille est impliquée.\pMême la police peine à arrêter ses hommes.
''')
block('Route24',r'''
JustEarnedFabulousPrize|Cinq victoires! La famille apprécie le talent. Tu as mérité ton prix.
ReceivedNuggetFromMysteryTrainer|Le sbire Mafiamille remet une Pépite à {PLAYER}!
JoinTeamRocket|Un talent comme le tien intéresserait la Mafiamille.\pNous savons récompenser les amis de la famille. Tu veux nous rejoindre?\pNon? Le Don aime les gens décidés. Mais je peux insister un peu!
RocketDefeat|D'accord, tu sais dire non!
YoudBecomeTopRocketLeader|Tu aurais fait une belle carrière dans la famille.\pEnfin... je vais surtout éviter de raconter ce combat au Don.
''')
block('CeladonCity',r'''
KeepOutOfTeamRocketsWay|La Mafiamille règle ses affaires. Circule!
GameCornerSign|CASINO MAFIAMILLE\nLe rendez-vous des grandes mises!
''')
block('CeladonCity_House1',r'''
SlotsReelInTheDough|Héhéhé! Chaque jeton finit par remplir les caisses de la famille.
ShippedMonsAsSlotPrizes|Patron! Encore un lot de Yo-kai livré pour les lots du Casino!\pLes comptes vont vous plaire.
DontTouchGameCornerPoster|Ne touche pas à l'affiche du Casino!\pEt surtout pas à l'interrupteur... Euh, quelle affiche?
''')
block('CeladonCity_GameCorner',r'''
WelcomeBuySomeCoins|Bienvenue au Casino Mafiamille!\pIl vous faut des Jetons? Souhaitez-vous en acheter?
RumoredTeamRocketRunsThisPlace|Parle moins fort. Ce Casino appartiendrait à la Mafiamille.\pJe préfère ne pas savoir où vont les recettes.
GruntIntro|Cette affiche? Propriété privée. Tu as cinq secondes pour t'éloigner.
GruntDefeat|Le Don va me passer un savon!
GruntPostBattle|Le passage est découvert! Je dois prévenir Don Morléone!
SwitchBehindPosterPushIt|Un interrupteur derrière l'affiche!\pAppuyons dessus!
''')
triples('RocketHideout_B1F',r'''
Grunt1|Qui t'a donné l'adresse? La famille ne reçoit pas les visiteurs!|Tu n'es pas un simple visiteur!|Entrer ici sans invitation... Tu cherches vraiment des ennuis.
Grunt2|Tu as forcé l'entrée de notre repaire? Quelle audace!|Je n'ai rien pu faire!|Le Don n'aime pas qu'on dérange ses affaires.
Grunt3|Intrus repéré! La relève attendra!|Relève... demandée!|Le Scope Sylphe? Je ne sais pas où le patron l'a rangé.
Grunt4|Une visite guidée? Tu t'es trompé d'endroit.|Bon... tu gagnes.|Pour rencontrer le Don, prends l'ascenseur. Moi, je reste ici.
Grunt5|Une petite souris dans le garde-manger de la famille?|La souris mord!|Tout ce vacarme a ouvert la porte! J'étais censé la surveiller...
''')
triples('RocketHideout_B2F',r'''
Grunt|Avec le Scope Sylphe, on peut voir les fantômes. Une affaire pleine d'avenir!|Je préfère rester vivant!|Quatre sous-sols, et le Don au bout du chemin. Tu tiens tant à le voir?
''')
triples('RocketHideout_B3F',r'''
Grunt1|Les affaires de la Mafiamille ne te concernent pas!|Mon service est terminé...|Le Scope Sylphe? L'appareil dérobé par le patron? Il est quelque part ici.
Grunt2|On nous a prévenus de ton arrivée. Cette fois, on t'arrête!|Même avec un avertissement...|Sans Clé Ascenseur, tu n'iras pas bien loin.
''')
triples('RocketHideout_B4F',r'''
Grunt1|L'ascenseur est bloqué? Qui avait la clé, déjà?|Ah... c'était moi.|Oh non! J'ai fait tomber la Clé Ascenseur!
Grunt2|Je te reconnais! Tu as saboté nos fouilles au Mont Sélénite!|Encore toi!|Tu t'es donné pour mission de ruiner les affaires de la famille?
Grunt3|Un costume propre, des comptes bien tenus... et une équipe redoutable!|Le costume, lui, est intact.|Don Morléone, pardonnez-moi. Je n'ai pas tenu la porte.
Giovanni|On entre rarement ici sans mon accord. Tu as de l'audace.\pJe suis Don Morléone. La Mafiamille sait tirer profit du talent des Yo-kai.\pMais ton intervention nous coûte cher. Voyons comment tu comptes régler ta dette.|Tu as remporté cette manche.|Tu prends soin de tes Yo-kai. Cela se voit.\pJe vais me retirer pour cette fois. N'y vois pas une invitation à recommencer.
''')
triples('PokemonTower_7F',r'''
Grunt1|La tour est fermée aux curieux. Ordre de la famille!|Je laisse passer!|Tu nous fais perdre un temps précieux. Je retiens ton visage.
Grunt2|Ce vieil homme est venu dénoncer nos captures.\pNous lui expliquons simplement qu'on ne se mêle pas des affaires de la Mafiamille.|Ça suffit! J'ai compris!|Ces Yo-kai rapportent gros. C'est tout ce qui compte pour mes collègues.
Grunt3|Tu veux libérer ce vieux monsieur? Il faudra d'abord me convaincre!|Très convaincant...|Pars avant que je retrouve mon courage.
''')
# Preserve Fuji's existing plot and ghost identity; translate only his rescue exchange.
block('PokemonTower_7F',r'''
MrFujiThankYouFollowMe|M. FUJI: Tu es venu me sauver? Merci.\pJ'étais venu apaiser l'esprit de la mère d'OSSELAIT. Elle peut enfin reposer en paix.\pSuis-moi jusqu'à ma maison, au pied de la tour.
''')
block('SaffronCity',r'''
BossTakeTownForTeamRocket|Le Don veut contrôler les affaires de Safrania. Nous préparons le terrain.
SaffronBelongsToTeamRocket|La Mafiamille tient Safrania. Tu ferais mieux de le retenir.
YouBeatTeamRocket|Tu as chassé la Mafiamille sans aide? Quel courage!
SafeToGoOutAgain|Les sbires sont partis! On peut enfin sortir sans crainte.
PeopleComingBackToSaffron|L'occupation avait fait fuir beaucoup de monde.\pLes habitants reviennent depuis le départ de la Mafiamille.
SawRocketBossEscaping|J'ai vu Don Morléone quitter la Sylphe. Il n'avait pas l'air content.
''')
block('ViridianCity_Gym',r'''
GiovanniIntro|Te voilà encore. Ici, je suis aussi le Champion de Jadielle.\pCette fois, aucune affaire à discuter: tu viens chercher mon Badge.\pDon Morléone ne fait pas de cadeau. Montre-moi ce que vaut ton équipe!{PLAY_BGM}{MUS_ENCOUNTER_ROCKET}
GiovanniPostBattle|Tu as gagné. Je tiens parole.\pJ'arrête nos opérations à Kanto. Mes hommes devront se retirer.\pLa famille ne disparaît pas pour autant. Quant à moi, j'ai un entraînement à reprendre.
ReceivedTM26FromGiovanni|{PLAYER} reçoit la CT26 de Don Morléone.
GymGuyPostVictory|Don Morléone était le Champion de Jadielle?\pEt tu l'as battu! Quel exploit!
GymStatuePlayerWon|ARÈNE YO-KAI DE JADIELLE\nCHAMPION: DON MORLÉONE\pDRESSEURS VICTORIEUX:\n{RIVAL}, {PLAYER}
''')
triples('MtEmber_Exterior',r'''
Grunt1|Tu écoutais notre conversation? La discrétion, ça s'apprend!|Je parle trop fort, aussi...|Le Don n'aime pas qu'on divulgue les affaires de la famille.
Grunt2|Tu veux une part du trésor? Il est déjà réservé!|Les comptes ne sont pas bons!|Oublie ce que tu as entendu. Pour une fois, rends-nous service.
''')
block('MtEmber_Exterior',r'''
WellTryDiggingHere|C'est ici. On creuse. Le trésor dont on nous a parlé doit être dessous.
YoureInTheWayGetLost|Tu gênes le chantier. Va voir ailleurs!
PunchedThroughAtLast|Enfin une ouverture! À nous le trésor!
WhatsPasswordAgain|Tout ce qu'on trouve part à l'entrepôt de la Mafiamille. Compris?\pAu fait... tu te rappelles les mots de passe?
FirstPasswordGoldeen|Il y en a deux. Le premier est: “GOLDEEN need log.”\pEt le second...
SnoopsBeenListeningIn|Hé! Cet enfant nous écoute depuis le début!
WellRegroupDontStepInsideThere|On doit se regrouper. Toi, ne mets pas un pied là-dedans!\pEt oublie notre conversation!
''')
block('FourIsland_IcefallCave_Back',r'''
LoreleiKeepHandsOffMons|OLGA: Laissez les Yo-kai de cette grotte tranquilles!\pVous allez répondre de vos captures!
ShutItLadyLeaveUsBe|On travaille pour la Mafiamille. Vos leçons, gardez-les pour vos élèves!
LoreleiPlayerHelpMeKickPoachersOut|OLGA: {PLAYER}?! Nous discuterons plus tard.\pAide-moi à chasser ces braconniers avant qu'ils capturent d'autres Yo-kai!
GruntIntro|Nos prises appartiennent à la famille. Tu veux contester le contrat?
GruntDefeat|On n'avait pas prévu votre visite!
LoreleiWhereHaveYouTakenMons|OLGA: Où avez-vous emmené les Yo-kai capturés?\pRépondez. Je compte bien arrêter votre trafic!
NotTellingYouThat|Je... Je ne dirai rien!
LoreleiWellDeepFreezeYou|OLGA: Mon partenaire n'apprécie pas ce que vous faites à ses amis.\pUn petit Laser Glace t'aiderait-il à parler?
OkayRocketWareHouseFiveIsland|D'accord! Les Yo-kai sont dans l'entrepôt de la Mafiamille, sur l'Île 5!\pOn s'en va! De toute façon, vous n'entrerez jamais sans les mots de passe!
ThankYouThisIsAwful|Merci, {PLAYER}. J'ai grandi sur ces îles.\pJe ne pensais pas que ces criminels y avaient installé leur trafic.
''')
triples('FiveIsland_Meadow',r'''
Rocket1|Terrain privé de la Mafiamille! Demi-tour!|Tu n'as pas lu le panneau?|Tu n'as aucune affaire à régler ici. Rentre chez toi.
Rocket2|Il n'y a que notre entrepôt, au bout. Qu'est-ce que tu viens chercher?|Une mauvaise surprise...|Tu veux savoir ce qu'on garde? Tu dormirais mieux sans le savoir.
Rocket3|Passer devant moi ne te servira à rien!|Je vais froisser mon costume!|La porte demande deux mots de passe. Un combat ne l'ouvrira pas.
''')
block('FiveIsland_Meadow',r'''
DoorNeedsTwoPasswords|Il faut deux mots de passe pour ouvrir cette porte.
EnteredPasswordAnotherNeeded|{PLAYER} saisit un mot de passe.\p“GOLDEEN need log.”\pUn second mot de passe est nécessaire...
EnteredPasswordDoorOpened|{PLAYER} saisit les deux mots de passe.\p“GOLDEEN need log.”\n“Yes, nah, CHANSEY.”\pLa porte de l'entrepôt s'ouvre!
WarehouseDoorAlreadyOpen|La porte de l'entrepôt est déjà ouverte.
''')
triples('SixIsland_OutcastIsland',r'''
Rocket|Pas un Yo-kai rare à l'horizon! La famille attend des résultats.\pUn combat me changera les idées!|Même ma pause est ratée...|Si tu vois un Yo-kai rare, tu me préviens? On peut rêver.
''')
triples('FiveIsland_RocketWarehouse',r'''
Grunt1|Tes Yo-kai ont de la valeur. Tu veux les vendre à la famille?\pAh... tu viens te battre.|Mauvaise négociation!|Notre offre tient toujours. Non? Tu es vraiment attaché à eux.
Grunt2|Tu sais où tu mets les pieds? Cet entrepôt appartient à la Mafiamille!|Tu dépasses les bornes!|Le Don aurait ordonné le retrait? Personne ne nous a prévenus!
Grunt3|Les autres m'ont parlé de toi. Mais tu ne peux pas connaître le Don!|Pas un mot à mes collègues!|Les grandes affaires attirent toujours les petits curieux...
Admin1|Je fais confiance au Don. Quand la famille me confie une tâche, je l'accomplis.|J'ai manqué à ma parole...|Tu défends tes convictions. Je commence à comprendre pourquoi tu tiens bon.
Admin2|Assez joué les héros! Tu prétends que le Don a arrêté nos opérations?\pTu espères nous faire partir avec un mensonge?|Tu es trop fort...\pCe Badge! C'est celui de Don Morléone! Alors... le retrait est vraiment son ordre?|Nous quitterons l'entrepôt. Les affaires s'arrêtent ici.\pMais je retrouverai le Don pour savoir ce qu'il attend de nous. Adieu.
Gideon|J'allais vendre le Saphir à la Mafiamille pour une fortune!\pTu viens de ruiner ma meilleure affaire!|Ma commission! Envolée!|Sans acheteur, cette pierre ne me sert plus. Prends-la et laisse-moi!
''')
block('FiveIsland_RocketWarehouse',r'''
ManyMonsLockedInPen|De nombreux Yo-kai sont enfermés dans cet enclos...
PenUnlockedMonsFled|L'enclos est ouvert. Les Yo-kai semblent s'être échappés.
MadeItSoYouCanComeBackThrough|J'ai changé les flèches pour te laisser revenir par ici.\pVa reprendre des forces. Le prochain adversaire est bien plus redoutable que moi.
ReportWithGraphsAndText|Un rapport apparaît à l'écran:\p“Influence des ondes magnétiques sur l'évolution des Yo-kai”.\pCes calculs sont difficiles à comprendre...
GetLostLeaveMeBe|Encore toi? Laisse-moi tranquille.
GiovannisKidHasRedHair|Tu ne serais pas un envoyé de Don Morléone?\pNon... Il ne choisirait pas la personne qui a ruiné notre marché.\pCette affaire ne te concerne plus. Laisse-moi!
''')
# The complete ordinary Mafia exchanges at Silph, each with a distinct voice.
triples('SilphCo_2F',r'''
Grunt1|Les visites scolaires sont annulées. Ordre de la famille!|Tu apprends vite!|Les dalles en losange sont des téléporteurs. Voilà ton cours de technologie.
Grunt2|Hé! Qui t'a autorisé à parcourir nos nouveaux bureaux?|Je vais devoir le signaler...|La Sylphe travaillera bientôt pour la Mafiamille. C'est une question de temps.
''')
triples('SilphCo_3F',r'''
Grunt|Arrête de déranger la famille, tu veux?|Je prends ma pause!|Une Carte Magnétique ouvre les portes. Voilà, tu sais tout. Maintenant, laisse-moi.
''')
triples('SilphCo_4F',r'''
Grunt1|La Mafiamille contrôle la Sylphe. Les réclamations attendront!|Réclamation acceptée...|Le Don convoitait cette entreprise depuis longtemps.
Grunt2|Intrus en vue! Cette fois, j'ai bien regardé!|Mais qui es-tu?!|Je dois prévenir le Don au dernier étage!
''')
triples('SilphCo_5F',r'''
Grunt1|On parle d'un enfant dans les couloirs. Tu viens te rendre?|Pas du tout, apparemment.|Provoquer la Mafiamille, ce n'est pas une bonne stratégie de carrière.
Grunt2|Un peu de respect! Tu parles à un membre de la famille.|Je manque d'arguments...|Les Yo-kai grandissent, les affaires aussi. Moi, je devrais surtout m'entraîner.
''')
triples('SilphCo_6F',r'''
Grunt1|Nous sommes quatre frères au service de la Mafiamille. Tu commences par moi!|Premier frère à terre!|Les trois autres ne te laisseront pas passer si facilement.
Grunt2|Tu choisis vraiment de te mettre toute la famille à dos?|Tu assumes ton choix...|Les défenseurs de la justice compliquent toujours nos affaires.
''')
triples('SilphCo_7F',r'''
Grunt1|Un des quatre frères de la famille, pour te servir... enfin, te stopper!|Les frères! J'ai perdu!|Mes frères finiront ce travail. Nous sommes solidaires.
Grunt2|L'enfant qu'on recherche? Tu viens de te livrer tout seul!|C'est moi qu'on a retrouvé...|Pars avant que le Don perde patience.
Grunt3|Un bruit dans le couloir... Encore cette petite souris!|Elle a de bons Yo-kai!|Courir partout ne suffira pas pour trouver le bureau du Don.
''')
triples('SilphCo_8F',r'''
Grunt1|Ton ascension s'arrête ici. Le Don ne reçoit personne!|Mauvais étage pour moi...|Fais demi-tour, ou j'appelle du renfort!
Grunt2|Troisième frère de la Mafiamille! Tu ne nous arrêteras pas tous!|Mes frères... au secours!|Je laisse la suite à mon dernier frère.
''')
triples('SilphCo_9F',r'''
Grunt1|Tes Yo-kai ont l'air de t'adorer. Voyons s'ils savent aussi te défendre.|Ça répond à ma question.|Si j'avais commencé à ton âge... Enfin, on ne refait pas les comptes du passé.
Grunt2|Le dernier des quatre frères! Je vais laver l'honneur de la famille!|Quatre frères... quatre défaites?|On devrait peut-être s'entraîner ensemble avant de recommencer.
''')
triples('SilphCo_10F',r'''
Grunt|Bienvenue à cet étage! La famille t'offre un combat d'accueil.|L'accueil est fermé!|La salle du conseil est encore un étage plus haut.
''')
triples('SilphCo_11F',r'''
Grunt1|Halte! Tu as rendez-vous avec Don Morléone?|Rendez-vous confirmé...|Le Don choisit des Yo-kai robustes. Prépare-toi bien.
Grunt2|Pas un pas de plus! Tu approches du bureau du Don!|Doucement, s'il te plaît!|Tu veux toujours rencontrer le patron après tout ça?
Giovanni|Ah, {PLAYER}. Nous nous retrouvons.\pLe président et moi négocions un accord important.\pLa Mafiamille n'aime pas les interruptions. Tu vas devoir me convaincre de t'écouter.|Encore une affaire qui tourne mal!|Tu nous coûtes la Sylphe. Je n'oublierai pas ce nom: {PLAYER}.\pMais un revers ne suffit pas à faire tomber la famille.\pNous nous reverrons.
''')
# Related civilian and accomplice dialogue, not unrelated scientist battles.
for m,txt in {
'SilphCo_2F':r'''ConnorDefeat|Comment as-tu compris que j'aidais la Mafiamille?
ConnorPostBattle|La Sylphe paie mon salaire. La Mafiamille paie mes extras.
Text_ThunderWaveTeach|Au secours! Ne me faites pas de mal!\pOh! Tu n'es pas avec la Mafiamille. Excuse-moi...\pPour me faire pardonner, je peux enseigner Cage Éclair à un de tes Yo-kai.''',
'SilphCo_3F':r'''JoseIntro|La Mafiamille reconnaît mes talents mieux que la Sylphe!
JosePostBattle|Ils m'avaient promis de me laisser étudier les Yo-kai si je les aidais...''',
'SilphCo_4F':r'''TeamRocketIsGone|La Mafiamille est partie? Je peux enfin sortir de ma cachette!''',
'SilphCo_5F':r'''RocketsInUproarAboutIntruder|La Mafiamille s'agite à cause d'un intrus. C'est toi, n'est-ce pas?
YoureOurHeroThankYou|Les sbires sont partis! Tu nous as sauvés, merci!
RocketBossLookingForStrongMons|Le chef des occupants cherchait des Yo-kai puissants.\pJ'espère que notre président ne lui a rien cédé...''',
'SilphCo_6F':r'''RocketsTookOverBuilding|La Mafiamille a pris le contrôle du bâtiment!
RocketsTryingToConquerWorld|La Mafiamille veut étendre son influence grâce aux Yo-kai.
RocketsRanAwayBecauseOfYou|Les sbires ont fui grâce à toi!
TargetedSilphForOurMonProducts|Nos produits pour Yo-kai ont dû attirer la convoitise du Don.
TaylorIntro|Ce président m'a envoyé dans une filiale perdue!\pAprès ça, on s'étonne que certains préfèrent aider la Mafiamille!''',
'SilphCo_7F':r'''HaveMonForSavingUs|Tu n'es pas de la Mafiamille? Tu viens nous sauver?\pMerci! Je voudrais te confier ce Yo-kai.
RocketBossWentToBoardroom|Don Morléone est dans la salle du conseil!\pJe m'inquiète pour notre président.
RocketsAfterMasterBall|La Mafiamille voulait la Master Ball, capable de capturer n'importe quel Yo-kai.
CanceledMasterBallProject|Nous avons suspendu le projet Master Ball à cause de la Mafiamille.
BadIfTeamRocketTookOver|Si la Mafiamille contrôlait nos recherches et nos Yo-kai... Je préfère ne pas y penser.
WowYouChasedOffTeamRocket|Tu as chassé la Mafiamille sans aide? Incroyable!
RivalIntro|{RIVAL}: Ha! Je savais que tu finirais par venir!\pLa Mafiamille t'a retardé? Pas mon problème!\pJe t'ai aperçu à Safrania. Voyons si tu as progressé!
RivalDefeat|Ah, mince! Tu es prêt à affronter le Don!''',
'SilphCo_8F':r'''ToRocketBossMonsAreTools|Don Morléone fait peur aux employés.\pPour lui, les Yo-kai sont des outils au service de ses affaires.\pIl ne doit pas prendre notre entreprise!'''
}.items():block(m,txt)
# Translated references outside the occupied maps.
for m,txt in {
'CeruleanCity_House2':r'''RocketsStoleTMForDig|Ces voleurs de la Mafiamille ont saccagé ma maison!\pIls ont pris ma CT Tunnel. Je l'avais achetée pour mon Yo-kai!
TeamRocketTryingToDigIntoNoGood|La Mafiamille prépare encore un mauvais coup, c'est certain.
TeamRocketLeftWayOut|Les cambrioleurs ont laissé un passage vers l'extérieur!''',
'PewterCity_PokemonCenter_1F':r'''TeamRocketMtMoonImOnPhone|Quoi? La Mafiamille au Mont Sélénite?\pUn instant... Je suis au téléphone!''',
'Route4_PokemonCenter_1F':r'''TeamRocketAttacksCerulean|La Mafiamille s'en prend aux habitants d'Azuria.\pOn entend parler de ses méfaits tous les jours.''',
'MtMoon_1F':r'''KentPostBattle|Je les ai vus! Ces types travaillent pour la Mafiamille!''',
'LavenderTown':r'''GhostsAppearedInTower|Des fantômes hantent la tour. On dit que les captures de la Mafiamille y ont troublé les esprits.''',
'SSAnne_1F_Room1':r'''ImAGlobalPoliceAgent|Chut! Je suis un agent de la Police Internationale.\pJe suis la piste de la Mafiamille. Elle prépare quelque chose.''',
'Route15':r'''ErnestPostBattle|Vivre hors des règles, ça me plaît. Les affaires de la Mafiamille, par exemple...''',
'VictoryRoad_3F':r'''GeorgePostBattle|C'est donc toi qui as battu Don Morléone, le chef de la Mafiamille?'''
}.items():block(m,txt)
for m,txt in {
'LavenderTown_House1':r'''RocketsKilledCubonesMother|La Mafiamille ne recule devant rien. La mère d'OSSELAIT a été tuée en tentant de leur échapper.''',
'LavenderTown_PokemonCenter_1F':r'''RocketsDoAnythingForMoney|La Mafiamille ferait n'importe quoi pour de l'argent. Même les Yo-kai ne sont pas à l'abri.
CubonesMotherKilledByRockets|J'ai vu la mère d'OSSELAIT tenter de fuir la Mafiamille. Elle n'a pas survécu...''',
'SaffronCity_PokemonCenter_1F':r'''SilphCoVictimOfFame|La réputation de la Sylphe a attiré la Mafiamille. Ses inventions valent une fortune.
GreatIfEliteFourCameBeatRockets|Si le Conseil 4 venait chasser la Mafiamille... On pourrait enfin souffler!
TeamRocketTookOff|Les hommes du Don sont partis! On peut de nouveau sortir sans crainte.''',
'VermilionCity_House3':r'''DearPippiLetter|Chère Pippi, j'espère te revoir bientôt.\pLa Mafiamille fait des siennes à Safrania. Carmin sur Mer semble encore tranquille.''',
'VermilionCity_Mart':r'''TeamRocketAreWickedPeople|La Mafiamille fait du trafic de Yo-kai rares.\pElle abandonne ceux qui ne lui rapportent rien. Ces gens ne voient que le profit.''',
'SixIsland_DottedHole_SapphireRoom':r'''SellToTeamRocketTellPassword|Je savais que le Saphir était ici. Je vais le vendre à la Mafiamille!\pNe me regarde pas comme ça! Si tu le veux, va le reprendre à l'entrepôt.\pJe connais un des mots de passe: “Yes, nah, CHANSEY.”\pVoilà! Ne m'en veux pas trop.'''
}.items():block(m,txt)

# Read and report remaining explicit references rather than silently inventing translations.
base_rows=[]
import subprocess
originals={}
for (path,label),text in rows.items():
 p=Path(path)
 if path not in originals:originals[path]=subprocess.check_output(['git','show','6f143452a:'+path],text=True)
 t=originals[path];match=re.search(r'^'+re.escape(label)+r'::?\n((?:[ \t]*\.string "(?:\\.|[^"\\])*"[^\n]*\n)+)',t,re.M)
 if not match:raise AssertionError(('missing label',path,label))
 old=''.join(re.findall(r'\.string "((?:\\.|[^"\\])*)"',match[1]));text=wrap(text)
 assert controls(old)==controls(text),(label,controls(old),controls(text))
 replace(p,label,text);base_rows.append(dict(file=path,label=label,before=old,after=text))
Path('data/localisation/fr/mafiamille.tsv').write_text(''.join(r['file']+'\t'+r['label']+'\t'+r['after']+'\n' for r in base_rows))
Path('QA_RECETTE_FINALE/MAFIAMILLE_KANTO/DIALOGUES.json').write_text(json.dumps(base_rows,ensure_ascii=False,indent=2)+'\n')
print('Rewritten',len(base_rows),'dialogues')
