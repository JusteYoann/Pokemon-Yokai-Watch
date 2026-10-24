const struct Decoration gDecorations[] = {
    {
        DECOR_NONE,
        _("PETIT BUREAU"),
        DECORPERM_SOLID_FLOOR,
        DECORSHAPE_1x1,
        DECORCAT_DESK,
        0,
        DecorDesc_SMALL_DESK,
        DecorGfx_SMALL_DESK
    }, {
        DECOR_SMALL_DESK,
        _("PETIT BUREAU"),
        DECORPERM_SOLID_FLOOR,
        DECORSHAPE_1x1,
        DECORCAT_DESK,
        3000,
        DecorDesc_SMALL_DESK,
        DecorGfx_SMALL_DESK
    }, {
        DECOR_POKEMON_DESK,
        _("BUREAU YO-KAI"),
        DECORPERM_SOLID_FLOOR,
        DECORSHAPE_1x1,
        DECORCAT_DESK,
        3000,
        DecorDesc_POKEMON_DESK,
        DecorGfx_POKEMON_DESK
    }, {
        DECOR_HEAVY_DESK,
        _("BUREAU LOURD"),
        DECORPERM_SOLID_FLOOR,
        DECORSHAPE_3x2,
        DECORCAT_DESK,
        6000,
        DecorDesc_HEAVY_DESK,
        DecorGfx_HEAVY_DESK
    }, {
        DECOR_RAGGED_DESK,
        _("BUREAU RUSTIQUE"),
        DECORPERM_SOLID_FLOOR,
        DECORSHAPE_3x2,
        DECORCAT_DESK,
        6000,
        DecorDesc_RAGGED_DESK,
        DecorGfx_RAGGED_DESK
    }, {
        DECOR_COMFORT_DESK,
        _("BUREAU CONFORT"),
        DECORPERM_SOLID_FLOOR,
        DECORSHAPE_3x2,
        DECORCAT_DESK,
        6000,
        DecorDesc_COMFORT_DESK,
        DecorGfx_COMFORT_DESK
    }, {
        DECOR_PRETTY_DESK,
        _("JOLI BUREAU"),
        DECORPERM_SOLID_FLOOR,
        DECORSHAPE_3x3,
        DECORCAT_DESK,
        9000,
        DecorDesc_PRETTY_DESK,
        DecorGfx_PRETTY_DESK
    }, {
        DECOR_BRICK_DESK,
        _("BUREAU BRIQUES"),
        DECORPERM_SOLID_FLOOR,
        DECORSHAPE_3x3,
        DECORCAT_DESK,
        9000,
        DecorDesc_BRICK_DESK,
        DecorGfx_BRICK_DESK
    }, {
        DECOR_CAMP_DESK,
        _("BUREAU CAMPING"),
        DECORPERM_SOLID_FLOOR,
        DECORSHAPE_3x3,
        DECORCAT_DESK,
        9000,
        DecorDesc_CAMP_DESK,
        DecorGfx_CAMP_DESK
    }, {
        DECOR_HARD_DESK,
        _("BUREAU SOLIDE"),
        DECORPERM_SOLID_FLOOR,
        DECORSHAPE_3x3,
        DECORCAT_DESK,
        9000,
        DecorDesc_HARD_DESK,
        DecorGfx_HARD_DESK
    }, {
        DECOR_SMALL_CHAIR,
        _("PETITE CHAISE"),
        DECORPERM_PASS_FLOOR,
        DECORSHAPE_1x1,
        DECORCAT_CHAIR,
        2000,
        DecorDesc_SMALL_CHAIR,
        DecorGfx_SMALL_CHAIR
    }, {
        DECOR_POKEMON_CHAIR,
        _("CHAISE YO-KAI"),
        DECORPERM_PASS_FLOOR,
        DECORSHAPE_1x1,
        DECORCAT_CHAIR,
        2000,
        DecorDesc_POKEMON_CHAIR,
        DecorGfx_POKEMON_CHAIR
    }, {
        DECOR_HEAVY_CHAIR,
        _("CHAISE LOURDE"),
        DECORPERM_PASS_FLOOR,
        DECORSHAPE_1x1,
        DECORCAT_CHAIR,
        2000,
        DecorDesc_HEAVY_CHAIR,
        DecorGfx_HEAVY_CHAIR
    }, {
        DECOR_PRETTY_CHAIR,
        _("JOLIE CHAISE"),
        DECORPERM_PASS_FLOOR,
        DECORSHAPE_1x1,
        DECORCAT_CHAIR,
        2000,
        DecorDesc_PRETTY_CHAIR,
        DecorGfx_PRETTY_CHAIR
    }, {
        DECOR_COMFORT_CHAIR,
        _("CHAISE CONFORT"),
        DECORPERM_PASS_FLOOR,
        DECORSHAPE_1x1,
        DECORCAT_CHAIR,
        2000,
        DecorDesc_COMFORT_CHAIR,
        DecorGfx_COMFORT_CHAIR
    }, {
        DECOR_RAGGED_CHAIR,
        _("CHAISE RUSTIQUE"),
        DECORPERM_PASS_FLOOR,
        DECORSHAPE_1x1,
        DECORCAT_CHAIR,
        2000,
        DecorDesc_RAGGED_CHAIR,
        DecorGfx_RAGGED_CHAIR
    }, {
        DECOR_BRICK_CHAIR,
        _("CHAISE BRIQUES"),
        DECORPERM_PASS_FLOOR,
        DECORSHAPE_1x1,
        DECORCAT_CHAIR,
        2000,
        DecorDesc_BRICK_CHAIR,
        DecorGfx_BRICK_CHAIR
    }, {
        DECOR_CAMP_CHAIR,
        _("CHAISE CAMPING"),
        DECORPERM_PASS_FLOOR,
        DECORSHAPE_1x1,
        DECORCAT_CHAIR,
        2000,
        DecorDesc_CAMP_CHAIR,
        DecorGfx_CAMP_CHAIR
    }, {
        DECOR_HARD_CHAIR,
        _("CHAISE SOLIDE"),
        DECORPERM_PASS_FLOOR,
        DECORSHAPE_1x1,
        DECORCAT_CHAIR,
        2000,
        DecorDesc_HARD_CHAIR,
        DecorGfx_HARD_CHAIR
    }, {
        DECOR_RED_PLANT,
        _("PLANTE ROUGE"),
        DECORPERM_BEHIND_FLOOR,
        DECORSHAPE_1x2,
        DECORCAT_PLANT,
        3000,
        DecorDesc_RED_PLANT,
        DecorGfx_RED_PLANT
    }, {
        DECOR_TROPICAL_PLANT,
        _("PLANTE TROPIC."),
        DECORPERM_BEHIND_FLOOR,
        DECORSHAPE_1x2,
        DECORCAT_PLANT,
        3000,
        DecorDesc_TROPICAL_PLANT,
        DecorGfx_TROPICAL_PLANT
    }, {
        DECOR_PRETTY_FLOWERS,
        _("JOLIES FLEURS"),
        DECORPERM_BEHIND_FLOOR,
        DECORSHAPE_1x2,
        DECORCAT_PLANT,
        3000,
        DecorDesc_PRETTY_FLOWERS,
        DecorGfx_PRETTY_FLOWERS
    }, {
        DECOR_COLORFUL_PLANT,
        _("PLANTE COLORÉE"),
        DECORPERM_BEHIND_FLOOR,
        DECORSHAPE_2x2,
        DECORCAT_PLANT,
        5000,
        DecorDesc_COLORFUL_PLANT,
        DecorGfx_COLORFUL_PLANT
    }, {
        DECOR_BIG_PLANT,
        _("GRANDE PLANTE"),
        DECORPERM_BEHIND_FLOOR,
        DECORSHAPE_2x2,
        DECORCAT_PLANT,
        5000,
        DecorDesc_BIG_PLANT,
        DecorGfx_BIG_PLANT
    }, {
        DECOR_GORGEOUS_PLANT,
        _("PLANTE SUPERBE"),
        DECORPERM_BEHIND_FLOOR,
        DECORSHAPE_2x2,
        DECORCAT_PLANT,
        5000,
        DecorDesc_GORGEOUS_PLANT,
        DecorGfx_GORGEOUS_PLANT
    }, {
        DECOR_RED_BRICK,
        _("BRIQUE ROUGE"),
        DECORPERM_SOLID_FLOOR,
        DECORSHAPE_1x2,
        DECORCAT_ORNAMENT,
        500,
        DecorDesc_RED_BRICK,
        DecorGfx_RED_BRICK
    }, {
        DECOR_YELLOW_BRICK,
        _("BRIQUE JAUNE"),
        DECORPERM_SOLID_FLOOR,
        DECORSHAPE_1x2,
        DECORCAT_ORNAMENT,
        500,
        DecorDesc_YELLOW_BRICK,
        DecorGfx_YELLOW_BRICK
    }, {
        DECOR_BLUE_BRICK,
        _("BRIQUE BLEUE"),
        DECORPERM_SOLID_FLOOR,
        DECORSHAPE_1x2,
        DECORCAT_ORNAMENT,
        500,
        DecorDesc_BLUE_BRICK,
        DecorGfx_BLUE_BRICK
    }, {
        DECOR_RED_BALLOON,
        _("BALLON ROUGE"),
        DECORPERM_PASS_FLOOR,
        DECORSHAPE_1x1,
        DECORCAT_ORNAMENT,
        500,
        DecorDesc_RED_BALLOON,
        DecorGfx_RED_BALLOON
    }, {
        DECOR_BLUE_BALLOON,
        _("BALLON BLEU"),
        DECORPERM_PASS_FLOOR,
        DECORSHAPE_1x1,
        DECORCAT_ORNAMENT,
        500,
        DecorDesc_BLUE_BALLOON,
        DecorGfx_BLUE_BALLOON
    }, {
        DECOR_YELLOW_BALLOON,
        _("BALLON JAUNE"),
        DECORPERM_PASS_FLOOR,
        DECORSHAPE_1x1,
        DECORCAT_ORNAMENT,
        500,
        DecorDesc_YELLOW_BALLOON,
        DecorGfx_YELLOW_BALLOON
    }, {
        DECOR_RED_TENT,
        _("TENTE ROUGE"),
        DECORPERM_PASS_FLOOR,
        DECORSHAPE_3x3,
        DECORCAT_ORNAMENT,
        10000,
        DecorDesc_RED_TENT,
        DecorGfx_RED_TENT
    }, {
        DECOR_BLUE_TENT,
        _("TENTE BLEUE"),
        DECORPERM_PASS_FLOOR,
        DECORSHAPE_3x3,
        DECORCAT_ORNAMENT,
        10000,
        DecorDesc_BLUE_TENT,
        DecorGfx_BLUE_TENT
    }, {
        DECOR_SOLID_BOARD,
        _("PLANCHE SOLIDE"),
        DECORPERM_PASS_FLOOR,
        DECORSHAPE_1x2,
        DECORCAT_ORNAMENT,
        3000,
        DecorDesc_SOLID_BOARD,
        DecorGfx_SOLID_BOARD
    }, {
        DECOR_SLIDE,
        _("TOBOGGAN"),
        DECORPERM_PASS_FLOOR,
        DECORSHAPE_2x4,
        DECORCAT_ORNAMENT,
        8000,
        DecorDesc_SLIDE,
        DecorGfx_SLIDE
    }, {
        DECOR_FENCE_LENGTH,
        _("BARRIÈRE LONG."),
        DECORPERM_SOLID_FLOOR,
        DECORSHAPE_1x1,
        DECORCAT_ORNAMENT,
        500,
        DecorDesc_FENCE_LENGTH,
        DecorGfx_FENCE_LENGTH
    }, {
        DECOR_FENCE_WIDTH,
        _("BARRIÈRE LARG."),
        DECORPERM_SOLID_FLOOR,
        DECORSHAPE_1x1,
        DECORCAT_ORNAMENT,
        500,
        DecorDesc_FENCE_WIDTH,
        DecorGfx_FENCE_WIDTH
    }, {
        DECOR_TIRE,
        _("PNEU"),
        DECORPERM_SOLID_FLOOR,
        DECORSHAPE_2x2,
        DECORCAT_ORNAMENT,
        800,
        DecorDesc_TIRE,
        DecorGfx_TIRE
    }, {
        DECOR_STAND,
        _("SOCLE"),
        DECORPERM_PASS_FLOOR,
        DECORSHAPE_4x2,
        DECORCAT_ORNAMENT,
        7000,
        DecorDesc_STAND,
        DecorGfx_STAND
    }, {
        DECOR_MUD_BALL,
        _("BOULE DE BOUE"),
        DECORPERM_PASS_FLOOR,
        DECORSHAPE_1x1,
        DECORCAT_ORNAMENT,
        200,
        DecorDesc_MUD_BALL,
        DecorGfx_MUD_BALL
    }, {
        DECOR_BREAKABLE_DOOR,
        _("PORTE FRAGILE"),
        DECORPERM_PASS_FLOOR,
        DECORSHAPE_1x2,
        DECORCAT_ORNAMENT,
        3000,
        DecorDesc_BREAKABLE_DOOR,
        DecorGfx_BREAKABLE_DOOR
    }, {
        DECOR_SAND_ORNAMENT,
        _("OBJET EN SABLE"),
        DECORPERM_BEHIND_FLOOR,
        DECORSHAPE_1x2,
        DECORCAT_ORNAMENT,
        3000,
        DecorDesc_SAND_ORNAMENT,
        DecorGfx_SAND_ORNAMENT
    }, {
        DECOR_SILVER_SHIELD,
        _("BOUCLIER ARGENT"),
        DECORPERM_BEHIND_FLOOR,
        DECORSHAPE_1x2,
        DECORCAT_ORNAMENT,
        0,
        DecorDesc_SILVER_SHIELD,
        DecorGfx_SILVER_SHIELD
    }, {
        DECOR_GOLD_SHIELD,
        _("BOUCLIER OR"),
        DECORPERM_BEHIND_FLOOR,
        DECORSHAPE_1x2,
        DECORCAT_ORNAMENT,
        0,
        DecorDesc_GOLD_SHIELD,
        DecorGfx_GOLD_SHIELD
    }, {
        DECOR_GLASS_ORNAMENT,
        _("OBJET EN VERRE"),
        DECORPERM_BEHIND_FLOOR,
        DECORSHAPE_1x2,
        DECORCAT_ORNAMENT,
        0,
        DecorDesc_GLASS_ORNAMENT,
        DecorGfx_GLASS_ORNAMENT
    }, {
        DECOR_TV,
        _("TÉLÉ"),
        DECORPERM_SOLID_FLOOR,
        DECORSHAPE_1x1,
        DECORCAT_ORNAMENT,
        3000,
        DecorDesc_TV,
        DecorGfx_TV
    }, {
        DECOR_ROUND_TV,
        _("TÉLÉ RONDE"),
        DECORPERM_SOLID_FLOOR,
        DECORSHAPE_1x1,
        DECORCAT_ORNAMENT,
        4000,
        DecorDesc_ROUND_TV,
        DecorGfx_ROUND_TV
    }, {
        DECOR_CUTE_TV,
        _("JOLIE TÉLÉ"),
        DECORPERM_SOLID_FLOOR,
        DECORSHAPE_1x1,
        DECORCAT_ORNAMENT,
        4000,
        DecorDesc_CUTE_TV,
        DecorGfx_CUTE_TV
    }, {
        DECOR_GLITTER_MAT,
        _("TAPIS BRILLANT"),
        DECORPERM_PASS_FLOOR,
        DECORSHAPE_1x1,
        DECORCAT_MAT,
        2000,
        DecorDesc_GLITTER_MAT,
        DecorGfx_GLITTER_MAT
    }, {
        DECOR_JUMP_MAT,
        _("TAPIS SAUTEUR"),
        DECORPERM_PASS_FLOOR,
        DECORSHAPE_1x1,
        DECORCAT_MAT,
        2000,
        DecorDesc_JUMP_MAT,
        DecorGfx_JUMP_MAT
    }, {
        DECOR_SPIN_MAT,
        _("TAPIS TOURNANT"),
        DECORPERM_PASS_FLOOR,
        DECORSHAPE_1x1,
        DECORCAT_MAT,
        2000,
        DecorDesc_SPIN_MAT,
        DecorGfx_SPIN_MAT
    }, {
        DECOR_C_LOW_NOTE_MAT,
        _("TAPIS DO GRAVE"),
        DECORPERM_PASS_FLOOR,
        DECORSHAPE_1x1,
        DECORCAT_MAT,
        500,
        DecorDesc_C_LOW_NOTE_MAT,
        DecorGfx_C_LOW_NOTE_MAT
    }, {
        DECOR_D_NOTE_MAT,
        _("TAPIS RÉ"),
        DECORPERM_PASS_FLOOR,
        DECORSHAPE_1x1,
        DECORCAT_MAT,
        500,
        DecorDesc_D_NOTE_MAT,
        DecorGfx_D_NOTE_MAT
    }, {
        DECOR_E_NOTE_MAT,
        _("TAPIS MI"),
        DECORPERM_PASS_FLOOR,
        DECORSHAPE_1x1,
        DECORCAT_MAT,
        500,
        DecorDesc_E_NOTE_MAT,
        DecorGfx_E_NOTE_MAT
    }, {
        DECOR_F_NOTE_MAT,
        _("TAPIS FA"),
        DECORPERM_PASS_FLOOR,
        DECORSHAPE_1x1,
        DECORCAT_MAT,
        500,
        DecorDesc_F_NOTE_MAT,
        DecorGfx_F_NOTE_MAT
    }, {
        DECOR_G_NOTE_MAT,
        _("TAPIS SOL"),
        DECORPERM_PASS_FLOOR,
        DECORSHAPE_1x1,
        DECORCAT_MAT,
        500,
        DecorDesc_G_NOTE_MAT,
        DecorGfx_G_NOTE_MAT
    }, {
        DECOR_A_NOTE_MAT,
        _("TAPIS LA"),
        DECORPERM_PASS_FLOOR,
        DECORSHAPE_1x1,
        DECORCAT_MAT,
        500,
        DecorDesc_A_NOTE_MAT,
        DecorGfx_A_NOTE_MAT
    }, {
        DECOR_B_NOTE_MAT,
        _("TAPIS SI"),
        DECORPERM_PASS_FLOOR,
        DECORSHAPE_1x1,
        DECORCAT_MAT,
        500,
        DecorDesc_B_NOTE_MAT,
        DecorGfx_B_NOTE_MAT
    }, {
        DECOR_C_HIGH_NOTE_MAT,
        _("TAPIS DO AIGU"),
        DECORPERM_PASS_FLOOR,
        DECORSHAPE_1x1,
        DECORCAT_MAT,
        500,
        DecorDesc_C_HIGH_NOTE_MAT,
        DecorGfx_C_HIGH_NOTE_MAT
    }, {
        DECOR_SURF_MAT,
        _("TAPIS SURF"),
        DECORPERM_PASS_FLOOR,
        DECORSHAPE_3x3,
        DECORCAT_MAT,
        4000,
        DecorDesc_SURF_MAT,
        DecorGfx_SURF_MAT
    }, {
        DECOR_THUNDER_MAT,
        _("TAPIS FOUDRE"),
        DECORPERM_PASS_FLOOR,
        DECORSHAPE_3x3,
        DECORCAT_MAT,
        4000,
        DecorDesc_THUNDER_MAT,
        DecorGfx_THUNDER_MAT
    }, {
        DECOR_FIRE_BLAST_MAT,
        _("TAPIS DÉFLAG."),
        DECORPERM_PASS_FLOOR,
        DECORSHAPE_3x3,
        DECORCAT_MAT,
        4000,
        DecorDesc_FIRE_BLAST_MAT,
        DecorGfx_FIRE_BLAST_MAT
    }, {
        DECOR_POWDER_SNOW_MAT,
        _("TAPIS POUDREUSE"),
        DECORPERM_PASS_FLOOR,
        DECORSHAPE_3x3,
        DECORCAT_MAT,
        4000,
        DecorDesc_POWDER_SNOW_MAT,
        DecorGfx_POWDER_SNOW_MAT
    }, {
        DECOR_ATTRACT_MAT,
        _("TAPIS ATTRACT."),
        DECORPERM_PASS_FLOOR,
        DECORSHAPE_3x3,
        DECORCAT_MAT,
        4000,
        DecorDesc_ATTRACT_MAT,
        DecorGfx_ATTRACT_MAT
    }, {
        DECOR_FISSURE_MAT,
        _("TAPIS ABÎME"),
        DECORPERM_PASS_FLOOR,
        DECORSHAPE_3x3,
        DECORCAT_MAT,
        4000,
        DecorDesc_FISSURE_MAT,
        DecorGfx_FISSURE_MAT
    }, {
        DECOR_SPIKES_MAT,
        _("TAPIS PICOTS"),
        DECORPERM_PASS_FLOOR,
        DECORSHAPE_3x3,
        DECORCAT_MAT,
        4000,
        DecorDesc_SPIKES_MAT,
        DecorGfx_SPIKES_MAT
    }, {
        DECOR_BALL_POSTER,
        _("AFFICHE BALL"),
        DECORPERM_NA_WALL,
        DECORSHAPE_1x1,
        DECORCAT_POSTER,
        1000,
        DecorDesc_BALL_POSTER,
        DecorGfx_BALL_POSTER
    }, {
        DECOR_GREEN_POSTER,
        _("AFFICHE VERTE"),
        DECORPERM_NA_WALL,
        DECORSHAPE_1x1,
        DECORCAT_POSTER,
        1000,
        DecorDesc_GREEN_POSTER,
        DecorGfx_GREEN_POSTER
    }, {
        DECOR_RED_POSTER,
        _("AFFICHE ROUGE"),
        DECORPERM_NA_WALL,
        DECORSHAPE_1x1,
        DECORCAT_POSTER,
        1000,
        DecorDesc_RED_POSTER,
        DecorGfx_RED_POSTER
    }, {
        DECOR_BLUE_POSTER,
        _("AFFICHE BLEUE"),
        DECORPERM_NA_WALL,
        DECORSHAPE_1x1,
        DECORCAT_POSTER,
        1000,
        DecorDesc_BLUE_POSTER,
        DecorGfx_BLUE_POSTER
    }, {
        DECOR_CUTE_POSTER,
        _("JOLIE AFFICHE"),
        DECORPERM_NA_WALL,
        DECORSHAPE_1x1,
        DECORCAT_POSTER,
        1000,
        DecorDesc_CUTE_POSTER,
        DecorGfx_CUTE_POSTER
    }, {
        DECOR_PIKA_POSTER,
        _("AFFICHE PIKA"),
        DECORPERM_NA_WALL,
        DECORSHAPE_2x1,
        DECORCAT_POSTER,
        1500,
        DecorDesc_PIKA_POSTER,
        DecorGfx_PIKA_POSTER
    }, {
        DECOR_LONG_POSTER,
        _("AFFICHE LONGUE"),
        DECORPERM_NA_WALL,
        DECORSHAPE_2x1,
        DECORCAT_POSTER,
        1500,
        DecorDesc_LONG_POSTER,
        DecorGfx_LONG_POSTER
    }, {
        DECOR_SEA_POSTER,
        _("AFFICHE MARINE"),
        DECORPERM_NA_WALL,
        DECORSHAPE_2x1,
        DECORCAT_POSTER,
        1500,
        DecorDesc_SEA_POSTER,
        DecorGfx_SEA_POSTER
    }, {
        DECOR_SKY_POSTER,
        _("AFFICHE CÉLESTE"),
        DECORPERM_NA_WALL,
        DECORSHAPE_2x1,
        DECORCAT_POSTER,
        1500,
        DecorDesc_SKY_POSTER,
        DecorGfx_SKY_POSTER
    }, {
        DECOR_KISS_POSTER,
        _("AFFICHE BISOUS"),
        DECORPERM_NA_WALL,
        DECORSHAPE_2x1,
        DECORCAT_POSTER,
        1500,
        DecorDesc_KISS_POSTER,
        DecorGfx_KISS_POSTER
    }, {
        DECOR_PICHU_DOLL,
        _("POUP. PICHU"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x1,
        DECORCAT_DOLL,
        3000,
        DecorDesc_PICHU_DOLL,
        DecorGfx_PICHU_DOLL
    }, {
        DECOR_PIKACHU_DOLL,
        _("POUP. PIKACHU"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x1,
        DECORCAT_DOLL,
        3000,
        DecorDesc_PIKACHU_DOLL,
        DecorGfx_PIKACHU_DOLL
    }, {
        DECOR_MARILL_DOLL,
        _("POUP. MARILL"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x1,
        DECORCAT_DOLL,
        3000,
        DecorDesc_MARILL_DOLL,
        DecorGfx_MARILL_DOLL
    }, {
        DECOR_TOGEPI_DOLL,
        _("POUP. TOGEPI"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x1,
        DECORCAT_DOLL,
        3000,
        DecorDesc_TOGEPI_DOLL,
        DecorGfx_TOGEPI_DOLL
    }, {
        DECOR_CYNDAQUIL_DOLL,
        _("POUP. HÉRIC."),
        DECORPERM_SPRITE,
        DECORSHAPE_1x1,
        DECORCAT_DOLL,
        3000,
        DecorDesc_CYNDAQUIL_DOLL,
        DecorGfx_CYNDAQUIL_DOLL
    }, {
        DECOR_CHIKORITA_DOLL,
        _("POUP. GERMIGNON"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x1,
        DECORCAT_DOLL,
        3000,
        DecorDesc_CHIKORITA_DOLL,
        DecorGfx_CHIKORITA_DOLL
    }, {
        DECOR_TOTODILE_DOLL,
        _("POUP. KAIMINUS"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x1,
        DECORCAT_DOLL,
        3000,
        DecorDesc_TOTODILE_DOLL,
        DecorGfx_TOTODILE_DOLL
    }, {
        DECOR_JIGGLYPUFF_DOLL,
        _("POUP. RONDOUDOU"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x1,
        DECORCAT_DOLL,
        3000,
        DecorDesc_JIGGLYPUFF_DOLL,
        DecorGfx_JIGGLYPUFF_DOLL
    }, {
        DECOR_MEOWTH_DOLL,
        _("POUP. MIAOUSS"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x1,
        DECORCAT_DOLL,
        3000,
        DecorDesc_MEOWTH_DOLL,
        DecorGfx_MEOWTH_DOLL
    }, {
        DECOR_CLEFAIRY_DOLL,
        _("POUP. MÉLOFÉE"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x1,
        DECORCAT_DOLL,
        3000,
        DecorDesc_CLEFAIRY_DOLL,
        DecorGfx_CLEFAIRY_DOLL
    }, {
        DECOR_DITTO_DOLL,
        _("POUP. MÉTAMORPH"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x1,
        DECORCAT_DOLL,
        3000,
        DecorDesc_DITTO_DOLL,
        DecorGfx_DITTO_DOLL
    }, {
        DECOR_SMOOCHUM_DOLL,
        _("POUP. LIPPOUTI"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x1,
        DECORCAT_DOLL,
        3000,
        DecorDesc_SMOOCHUM_DOLL,
        DecorGfx_SMOOCHUM_DOLL
    }, {
        DECOR_TREECKO_DOLL,
        _("POUP. ARCKO"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x1,
        DECORCAT_DOLL,
        3000,
        DecorDesc_TREECKO_DOLL,
        DecorGfx_TREECKO_DOLL
    }, {
        DECOR_TORCHIC_DOLL,
        _("POUP. POUSSIFEU"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x1,
        DECORCAT_DOLL,
        3000,
        DecorDesc_TORCHIC_DOLL,
        DecorGfx_TORCHIC_DOLL
    }, {
        DECOR_MUDKIP_DOLL,
        _("POUP. GOBOU"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x1,
        DECORCAT_DOLL,
        3000,
        DecorDesc_MUDKIP_DOLL,
        DecorGfx_MUDKIP_DOLL
    }, {
        DECOR_DUSKULL_DOLL,
        _("POUP. SKELÉNOX"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x1,
        DECORCAT_DOLL,
        3000,
        DecorDesc_DUSKULL_DOLL,
        DecorGfx_DUSKULL_DOLL
    }, {
        DECOR_WYNAUT_DOLL,
        _("POUP. OKÉOKÉ"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x1,
        DECORCAT_DOLL,
        3000,
        DecorDesc_WYNAUT_DOLL,
        DecorGfx_WYNAUT_DOLL
    }, {
        DECOR_BALTOY_DOLL,
        _("POUP. BALBUTO"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x1,
        DECORCAT_DOLL,
        3000,
        DecorDesc_BALTOY_DOLL,
        DecorGfx_BALTOY_DOLL
    }, {
        DECOR_KECLEON_DOLL,
        _("POUP. KECLEON"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x1,
        DECORCAT_DOLL,
        3000,
        DecorDesc_KECLEON_DOLL,
        DecorGfx_KECLEON_DOLL
    }, {
        DECOR_AZURILL_DOLL,
        _("POUP. AZURILL"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x1,
        DECORCAT_DOLL,
        3000,
        DecorDesc_AZURILL_DOLL,
        DecorGfx_AZURILL_DOLL
    }, {
        DECOR_SKITTY_DOLL,
        _("POUP. SKITTY"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x1,
        DECORCAT_DOLL,
        3000,
        DecorDesc_SKITTY_DOLL,
        DecorGfx_SKITTY_DOLL
    }, {
        DECOR_SWABLU_DOLL,
        _("POUP. TYLTON"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x1,
        DECORCAT_DOLL,
        3000,
        DecorDesc_SWABLU_DOLL,
        DecorGfx_SWABLU_DOLL
    }, {
        DECOR_GULPIN_DOLL,
        _("POUP. GLOUPTI"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x1,
        DECORCAT_DOLL,
        3000,
        DecorDesc_GULPIN_DOLL,
        DecorGfx_GULPIN_DOLL
    }, {
        DECOR_LOTAD_DOLL,
        _("POUP. NÉNUPIOT"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x1,
        DECORCAT_DOLL,
        3000,
        DecorDesc_LOTAD_DOLL,
        DecorGfx_LOTAD_DOLL
    }, {
        DECOR_SEEDOT_DOLL,
        _("POUP. GRAINIP."),
        DECORPERM_SPRITE,
        DECORSHAPE_1x1,
        DECORCAT_DOLL,
        3000,
        DecorDesc_SEEDOT_DOLL,
        DecorGfx_SEEDOT_DOLL
    }, {
        DECOR_PIKA_CUSHION,
        _("COUSS. PIKACHU"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x1,
        DECORCAT_CUSHION,
        2000,
        DecorDesc_PIKA_CUSHION,
        DecorGfx_PIKA_CUSHION
    }, {
        DECOR_ROUND_CUSHION,
        _("COUSS. MARILL"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x1,
        DECORCAT_CUSHION,
        2000,
        DecorDesc_ROUND_CUSHION,
        DecorGfx_ROUND_CUSHION
    }, {
        DECOR_KISS_CUSHION,
        _("COUSS. LIPPOUTI"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x1,
        DECORCAT_CUSHION,
        2000,
        DecorDesc_KISS_CUSHION,
        DecorGfx_KISS_CUSHION
    }, {
        DECOR_ZIGZAG_CUSHION,
        _("COUSS. ZIGZATON"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x1,
        DECORCAT_CUSHION,
        2000,
        DecorDesc_ZIGZAG_CUSHION,
        DecorGfx_ZIGZAG_CUSHION
    }, {
        DECOR_SPIN_CUSHION,
        _("COUSS. SPINDA"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x1,
        DECORCAT_CUSHION,
        2000,
        DecorDesc_SPIN_CUSHION,
        DecorGfx_SPIN_CUSHION
    }, {
        DECOR_DIAMOND_CUSHION,
        _("COUSS. TÉNÉFIX"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x1,
        DECORCAT_CUSHION,
        2000,
        DecorDesc_DIAMOND_CUSHION,
        DecorGfx_DIAMOND_CUSHION
    }, {
        DECOR_BALL_CUSHION,
        _("COUSS. BALL"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x1,
        DECORCAT_CUSHION,
        2000,
        DecorDesc_BALL_CUSHION,
        DecorGfx_BALL_CUSHION
    }, {
        DECOR_GRASS_CUSHION,
        _("COUSS. PLANTE"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x1,
        DECORCAT_CUSHION,
        2000,
        DecorDesc_GRASS_CUSHION,
        DecorGfx_GRASS_CUSHION
    }, {
        DECOR_FIRE_CUSHION,
        _("COUSS. FEU"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x1,
        DECORCAT_CUSHION,
        2000,
        DecorDesc_FIRE_CUSHION,
        DecorGfx_FIRE_CUSHION
    }, {
        DECOR_WATER_CUSHION,
        _("COUSS. EAU"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x1,
        DECORCAT_CUSHION,
        2000,
        DecorDesc_WATER_CUSHION,
        DecorGfx_WATER_CUSHION
    }, {
        DECOR_SNORLAX_DOLL,
        _("POUP. RONFLEX"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x2,
        DECORCAT_DOLL,
        10000,
        DecorDesc_SNORLAX_DOLL,
        DecorGfx_SNORLAX_DOLL
    }, {
        DECOR_RHYDON_DOLL,
        _("POUP. RHINOF."),
        DECORPERM_SPRITE,
        DECORSHAPE_1x2,
        DECORCAT_DOLL,
        10000,
        DecorDesc_RHYDON_DOLL,
        DecorGfx_RHYDON_DOLL
    }, {
        DECOR_LAPRAS_DOLL,
        _("POUP. LOKHLASS"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x2,
        DECORCAT_DOLL,
        10000,
        DecorDesc_LAPRAS_DOLL,
        DecorGfx_LAPRAS_DOLL
    }, {
        DECOR_VENUSAUR_DOLL,
        _("POUP. FLORIZ."),
        DECORPERM_SPRITE,
        DECORSHAPE_1x2,
        DECORCAT_DOLL,
        10000,
        DecorDesc_VENUSAUR_DOLL,
        DecorGfx_VENUSAUR_DOLL
    }, {
        DECOR_CHARIZARD_DOLL,
        _("POUP. DRACAUFEU"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x2,
        DECORCAT_DOLL,
        10000,
        DecorDesc_CHARIZARD_DOLL,
        DecorGfx_CHARIZARD_DOLL
    }, {
        DECOR_BLASTOISE_DOLL,
        _("POUP. TORTANK"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x2,
        DECORCAT_DOLL,
        10000,
        DecorDesc_BLASTOISE_DOLL,
        DecorGfx_BLASTOISE_DOLL
    }, {
        DECOR_WAILMER_DOLL,
        _("POUP. WAILMER"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x2,
        DECORCAT_DOLL,
        10000,
        DecorDesc_WAILMER_DOLL,
        DecorGfx_WAILMER_DOLL
    }, {
        DECOR_REGIROCK_DOLL,
        _("POUP. REGIROCK"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x2,
        DECORCAT_DOLL,
        10000,
        DecorDesc_REGIROCK_DOLL,
        DecorGfx_REGIROCK_DOLL
    }, {
        DECOR_REGICE_DOLL,
        _("POUP. REGICE"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x2,
        DECORCAT_DOLL,
        10000,
        DecorDesc_REGICE_DOLL,
        DecorGfx_REGICE_DOLL
    }, {
        DECOR_REGISTEEL_DOLL,
        _("POUP. REGISTEEL"),
        DECORPERM_SPRITE,
        DECORSHAPE_1x2,
        DECORCAT_DOLL,
        10000,
        DecorDesc_REGISTEEL_DOLL,
        DecorGfx_REGISTEEL_DOLL}
};
