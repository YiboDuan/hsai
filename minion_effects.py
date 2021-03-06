# alphabetical order!

import actions
import events
import utils


def acolyte_of_pain(game, trigger, id):
    if trigger[0] == 'deal_damage' and trigger[1] == id:
        game.action_queue.append((events.draw, (game.minion_pool[id].owner,)))

'''def amani_berserker(game, trigger, id): # this is probably wrong in conjunction with Auchenai Soulpriest
   minion = game.minion_pool[id]
   if trigger[0] == 'deal_damage' and trigger[1] == id:
      minion.attack += 3
   elif trigger[0] == 'heal' and trigger[1] == id and minion.health < minion.max_health and minion.health + trigger[2] >= minion.max_health:
      minion.attack -= 3
effects['Amani Berserker'] = amani_berserker'''  # work in progress


def arcane_golem(game, trigger, id):
    if trigger[0] == 'battlecry' and trigger[1] == id:
        game.enemy.crystals += 1
        return True


def armorsmith(game, trigger, id):
    if trigger[0] == 'deal_damage' and game.minion_pool[trigger[1]] in game.minion_pool[id].owner.board[1:]:
        game.minion_pool[id].owner.armor += 1


def cairne_bloodhoof(game, trigger, id):
    if trigger[0] == 'kill_minion' and trigger[1] == id:
        game.action_queue.append(
            (events.spawn, (game, game.minion_pool[id].owner, utils.get_card('Baine Bloodhoof'))))
        return True


# hero power (TODO: this doesn't belong in this file)
def druid(game, trigger, player):
    if trigger[0] == 'end_turn':
        game.player.board[0].attack -= 1
        return True


def earthen_ring_farseer(game, trigger, id):
    if trigger[0] == 'battlecry' and trigger[1] == id:
        target_id = events.target(game)
        game.action_queue.append((events.heal, (game, target_id, 3)))
        return True
    return False


def gnomish_inventor(game, trigger, id):
    if trigger[0] == 'battlecry' and trigger[1] == id:
        game.action_queue.append((events.draw, (game, game.player,)))
        return True


def harvest_golem(game, trigger, id):
    if trigger[0] == 'kill_minion' and trigger[1] == id:
        game.action_queue.append(
            (events.spawn, (game, game.minion_pool[id].owner, utils.get_card('Damaged Golem'))))
        return True


def healing_totem(game, trigger, id):
    if trigger[0] == 'end_turn' and game.minion_pool[id].owner == trigger[1]:
        for minion in game.minion_pool[id].owner.board[1:]:
            game.action_queue.append(
                (events.heal, (game, minion.minion_id, 1)))


def leper_gnome(game, trigger, id):
    if trigger[0] == 'kill_minion' and trigger[1] == id:
        game.action_queue.append((deal_damage, (game, utils.opponent(
            game, game.minion_pool[id].owner).board[0].minion_id, 2)))
        return True


# id gets partially applied when effect is created
def loot_hoarder(game, trigger, id):
    if trigger[0] == 'kill_minion' and trigger[1] == id:
        game.action_queue.append(
            (events.draw, (game, game.minion_pool[id].owner,)))
        return True


def nightblade(game, trigger, id):
    if trigger[0] == 'battlecry' and trigger[1] == id:
        game.action_queue.append((deal_damage, (game, utils.opponent(
            game, game.minion_pool[id].owner).board[0].minion_id, 3)))
        return True


def novice_engineer(game, trigger, id):
    if trigger[0] == 'battlecry' and trigger[1] == id:
        game.action_queue.append((events.draw, (game, game.player,)))
        return True


def raid_leader(game, trigger, id):
    def modifier(game, object, stat, value):
        if isinstance(object, utils.Minion) and not utils.is_hero(object) and object != game.minion_pool[id] and object.owner == game.minion_pool[id].owner and stat == 'attack':
            return value + 1
        else:
            return value
    game.minion_pool[id].owner.auras.add(utils.Aura(id, modifier))
    return True


def water_elemental(game, trigger, id):
    if trigger[0] == 'attack' and id in trigger[1:]:
        enemy = game.minion_pool[filter(lambda x:x != id, trigger[1:])[0]]
        enemy.attacks_left = 0
        enemy.mechanics.add('Frozen')

exceptions = ['actions', 'utils', 'exceptions', 'senjin_shieldmasta']
minion_effects = {utils.func_to_name(key): val for key, val in locals(
).items() if key[0] != '_' and key not in exceptions}
# minion_effects["Sen'jin Shieldmasta"] = senjin_shieldmasta # this is an
# example of how exceptions work
