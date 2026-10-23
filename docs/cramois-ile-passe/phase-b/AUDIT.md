# Audit préalable — phase B

Base approuvée : `1f335d268`, branche `feature/cramois-ile-passe`. Phase C exclue. EWRAM relue avant modification : 261348 octets, 796 libres ; IWRAM 29824 publique / 29888 privée.

Accès exacts : Cramois 24 × 20 cases ; Route 20 à l'est 120 × 20, raccord horizontal sans décalage ; Route 21 Sud au nord 24 × 50, raccord vertical sans décalage. La frontière sera exclusivement sur la portion maritime proche de l'île, jamais sur Cramois ou ses douze intérieurs.

Le brouillard horizontal natif utilise une texture de 2048 octets, des sprites semi-transparents et le mélange alpha GBA. Son système météo global crée vingt sprites, conserve un état météo sauvegardé, éclaircit certaines palettes et comporte déjà une adaptation verte pour Lavanville. L'activer comme météo de la route risquerait un nettoyage tardif sur l'île et un partage d'état avec Lavanville.

Solution retenue : réutiliser uniquement cette texture native, avec quinze sprites temporaires séparés, une palette blanche dédiée et une densité calculée depuis la position réelle du joueur en Surf. Le défilement et l'alpha seront locaux ; les registres de mélange seront rendus au moteur à la sortie. Une légère décoloration blanche de la sortie matérielle des palettes du monde accentuera la densité sans toucher aux buffers ni à l'interface. Aucun nouvel état sauvegardé, aucune modification de carte, de collision, de PNJ ou de ressource graphique approuvée.

La densité est lissée dans les deux sens et recalculée après chargement. Un changement de carte ou de contexte détruit l'effet ; aucune cinématique ni brume ne sera imposée aux déplacements instantanés. Les menus, combats et effets de fondu doivent être contrôlés explicitement. En manque de sprites/VRAM, l'effet doit se réduire ou se retirer sans supprimer d'acteur existant.
