# Hovernyan — proportions de combat corrigées

Base `f584896d4`, branche `feature/cramois-ile-passe`. Aucun merge sur master.

L'ancien cadrage appliquait des facteurs différents en largeur et en hauteur : inverses GBA 173/247 de face et 120/161 de dos. Le sprite paraissait donc élargi. Le cadrage utilise désormais 247/247 de face et 161/161 de dos : la hauteur et le point d'ancrage sont conservés, la largeur retrouve les proportions du dessin. Le rectangle de présentation passe de 71×51 à 49×51 de face et de 77×46 à 57×46 de dos.

Les PNG, palettes, textures 4bpp, cape, découpe préexistante du dos et sprite overworld restent inchangés. Les 300 autres cadrages de combat restent identiques. La configuration du générateur conserve explicitement cette exception pour éviter que la déformation réapparaisse à la prochaine génération. Une génération complète dans un répertoire temporaire reproduit exactement le tableau et le rapport de géométrie corrigés.

- [Capture native agrandie](public/proportions-corrigees-x4.png).
- [GIF d'un véritable combat mGBA](public/combat-proportions-corrigees.gif).
- [Contrôles publics](public/TEST_MGBA.json) et [privés](prive/TEST_MGBA.json).
- [Résumé des vérifications et mémoire](VALIDATION.json).

Les deux versions compilent et passent cinq contrôles chacune : matrice matérielle uniforme et pixels originaux de face/dos ; conversion native de chaque silhouette vers le décor d'animation ; séquence de combat au contrôleur enregistrée. La texture produite par `CopyYokaiBattlerToBg` est comparée octet par octet au rééchantillonnage uniforme attendu, dans sa capacité native. Les attaques conservent leurs animations normales ; le cadrage au repos est corrigé.

Les captures utilisent une nouvelle partie, une position dans l'Arène de Cramois et deux Hovernyan niveau 45 comme fixtures annoncées. Aucun résultat de combat ni PV adverse n'est forcé. Les GIF proviennent de mGBA, agrandis au plus proche voisin. Il ne s'agit pas d'une nouvelle validation complète de la campagne ni de tous les effets d'attaque.

EWRAM inchangée : 261368 octets, **776 libres** ; IWRAM inchangée : 29824 publique et 29888 privée. Aucun script, niveau, statistique, musique ni format de sauvegarde modifié.
