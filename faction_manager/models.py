from django.db import models


class Faction(models.Model):
    name = models.CharField(max_length=100)


# class Faction(models.Model):
# name (e.g. "the unseen")
# tier (e.g. 0, 1, 2, 3, 4, 5)
# hold (e.g. "strong", "weak")
# category text (e.g. "underworld", "institutions", "labor and trade", "the fringe", "citizenry")
# turf: [text] (e.g. ["stockyard", "slaughterhouse", "animal fighting pits"])
# headquarters: text (e.g. "A butcher shop")
# assets: [text] (e.g. "a large gang of bloodthirsty butchers", "a pack of death-dogs"])
# quirks: text


# class District(models.Model):
# name: text (e.g. "barrowcleft", "brightstone", "charhollow", "charterhall", "coalridge", "crow's foot", "the docks", "dunslough", "nightmarket", "silkshore", "six towers", "whitecrown", "the lost district")
# description: text
# scene: text
# streets: text
# building: text
# traits: [(text, int),] (e.g. [("WEALTH", 1), ("CRIME", 4)])

# class DistrictFaction(models.Model):
# district: fk.District
# faction: fk.Faction

# join table, but this will require some constraints. Could do {source_faction, target_faction, relationship} and likely have duplicate
# relationship entries, could do {faction_a, faction_b, relationship} but you'd need some way to say "get me faction_c's relationships" and pull
# all of the relevant ones into the query
# class FactionFaction(models.Model):


# class Landmark(models.Model):
# name: text
# description: text
# district: fk.District

# class NonPlayerCharacter(models.Model):
# name: text
# description: text
# district: fk.District
# faction: fk.Faction
# adjectives: [text] (e.g. ["calculating", "confident", "calm"])
