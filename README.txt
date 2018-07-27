TODO
ajouter README Alexandra
ajouter scene maya avec placement joint sur mesh squelette


HOWTO

1. init_spine.py
cree les 5 locators pour le labelling

2. aligner les cameras pour que y-axis soit la vraie verticale
createModel.placePlanes()

3. placer a la main les marqueurs puis pour chacun call placeLocator()
placeLocator() fait la triangulation 3D de mrkX1/mrkX2
0 => L6
1 => maximum local vertical (~T13)
2 => minimum local vertical (~T4)
3 => atlas
4 => upper jaw (base dent)

4. import skeleton.mb

5. 