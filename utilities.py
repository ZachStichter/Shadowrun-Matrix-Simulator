DECRYPT_BONUS = 0

class BaseUtility():
    '''
A basic utility class. All other utilities inherit from this. This docstring should not be visible in the live environment.
    '''
    def __init__(self,*args):
        self.name = 'utility'
        self.rating = 0
        self.initialized = False
        self.theoreticalMax = 10

    def tostr(self, *args):
        return f"Utility '{self.name}' initialized at rating {self.rating}."

    def boot(self, *args):
        print(f'Booting utility {self.name} at rating {self.rating}')

    def get_doc(self, *args):
        return self.__doc__

    def set_rating(self, rating, *args):
        if type(rating) == list:
            rating = int(rating[0])
        else:
            rating = int(rating)
        if rating > self.theoreticalMax:
            print('Rating greater than theoretical maximum. Overwrite settings?')
            result = ''
            while result.lower().strip() not in ['y','n']:
                result=input('[y/n]')
            if result.lower().strip() == 'y':
                self.rating = rating
            else:
                self.rating = self.theoreticalMax
        else:
            self.rating = rating
        print(self.tostr())

class DegradableUtility(BaseUtility):
    '''
A class for degradable utilities. Adds the degrade() method
    '''
    def __init__(self,maxrating,rating=None,*args):
        super().__init__()
        if maxrating != None:
            self.maxRating = min(int(maxrating),int(self.theoreticalMax))
            self.initialized = True
        else:
            self.maxRating = 0
            self.initialized = False
        if rating != None:
            self.rating = rating
        else:
            self.rating = self.maxRating

    def degrade(self, *args):
        if self.rating > 0:
            self.rating -=1
            return self.rating
        else:
            return -1

    def get_rating(self,*args):
        print(self.tostr())

class SleazeUtility(DegradableUtility):
    '''
Utility Name: Sleaze
Type: Degradable, Operational
Description: A Sleaze program allows the user to harmlessly pass through (ignore) any Matrix barrier with a rating equal-to, or lower than the program's current rating. As a Degradable program, Sleaze is reduced by 1 point after each use.
Source: Matrix Refragged, pg 32
    '''
    def __init__(self, maxrating,rating=None,*args):
        super().__init__(maxrating,rating)
        self.name = 'Sleaze'
        

    def sleaze(self,*args):
        new_rating = self.degrade()
        if new_rating >= 0:
            print(f'Sleazing past barrier. Current rating {new_rating+1}; new rating {new_rating}')
        else:
            print(f'Sleaze rating too low ({self.rating}). Cannot sleaze. Aborting.')

class AnalyzeUtility(BaseUtility):
    '''
Utility Name: Analyze
Type: Offensive
Description: An Analyze program decreases the user's target number by its rating while utilizing the Search and Render prompt.
Source: Matrix Refragged, pg 30
    '''
    def __init__(self,rating,*args):
        super().__init__()
        self.rating=rating
        self.name='Analyze'
        
    def get_bonus(self):
        return self.rating

class ArmorUtility(BaseUtility):
    pass

class AttackUtility(BaseUtility):
    '''
Utility Name: Attack
Type: Combat, Operational
Description: Attack programs are Operational combat programs designed to inflict damage upon other icons and sometimes their meat world users. Standard Attack utilities may be purchased at any damage level, and deal Overload Damage. Overload is resisted by a device's System Rating, with the Security Threshold, or the Firewall of the host acting as armor against the attack. Overload Damage can be further mitigated by utilizing the Armor utility. Each damage level carries with it a different Multiplier, as indicated below: Light x2, Moderate x3, Severe x4, Deadly x5. Some Attack Utilities have made a name for themselves and are designed to bypass a target icon's Matrix condition monitor, dealing direct Biofeedback Damage to the user (the target's User Mode determines whether this damage is dealt to the Stun or Physical track of the their condition monitor). Biofeedback Damage can be further mitigated by utilizing the Biofeedback Filtering utility. These notorious Biofeedback programs are detailed below. Nosebleed (Light) x5, Blackout (Moderate) x10, Killjoy (Severe) x15, Black Hammer (Deadly) x20.
Source: Matrix Refragged, pg 30
    '''
    def __init__(self,rating,name,*args):
        super().__init__()
        self.rating=rating
        self.dmg_type_dict={'lol':{
                                'typ':'overload',
                                'lvl':'light'
                                    },
                            'mol':{
                                'typ':'overload',
                                'lvl':'moderate'
                                },
                            'sol':{
                                'typ':'overload',
                                'lvl':'serious'},
                            'dol':{
                                'typ':'overload',
                                'lvl':'deadly'
                                },
                            'nosebleed':{
                                'typ':'biofeedback',
                                'lvl':'light'
                                },
                            'blackout':{
                                'typ':'biofeedback',
                                'lvl':'light'
                                },
                            'killjoy':{
                                'typ':'biofeedback',
                                'lvl':'severe'
                                },
                            'blackhammer':{
                                'typ':'biofeedback',
                                'lvl':'deadly'
                                }
                            }
        self.name=name
        self.dmg_type = self.dmg_type_dict[self.name]['typ']
        self.dmg_level = self.dmg_type_dict[self.name]['lvl']

    def attack(self, *args):
        return f'Dealing {self.dmg_level} {self.dmg_type} with a target number of {self.rating}'

class LightOverloadDamage(AttackUtility):
    def __init__(self, rating, *args):
        super().__init__(rating, 'lol', *args)
        self.__doc__ = super().__doc__

class ModerateOverloadDamage(AttackUtility):
    def __init__(self, rating, *args):
        super().__init__(rating, 'mol', *args)
        self.__doc__ = super().__doc__

class SeriousOverloadDamage(AttackUtility):
    def __init__(self, rating, *args):
        super().__init__(rating, 'sol', *args)
        self.__doc__ = super().__doc__

class DeadlyOverloadDamage(AttackUtility):
    def __init__(self, rating, *args):
        super().__init__(rating, 'dol', *args)
        self.__doc__ = super().__doc__

class NosebleedDamage(AttackUtility):
    def __init__(self, rating, *args):
        super().__init__(rating, 'nosebleed', *args)
        self.__doc__ = super().__doc__

class BlackoutDamage(AttackUtility):
    def __init__(self, rating, *args):
        super().__init__(rating, 'blackout', *args)
        self.__doc__ = super().__doc__

class KilljoyDamage(AttackUtility):
    def __init__(self, rating, *args):
        super().__init__(rating, 'killjoy', *args)
        self.__doc__ = super().__doc__

class BlackhammerDamage(AttackUtility):
    def __init__(self, rating, *args):
        super().__init__(rating, 'blackhammer', *args)
        self.__doc__ = super().__doc__

class BabyMonitorUtility(DegradableUtility):
    '''
Utility Name: Baby Monitor
Type: Degradable, Operational
Description: Baby Monitor is an operational program designed to allow a user to get a peek at their current Overwatch level. Whenever the user activates the Scrub Datastream prompt, the GM should relay the number of boxes accrued as Overwatch in terms of wound levels (Light, Moderate, Serious, etc). As a Degradable program, Baby Monitor is reduced by 1 point after each use.
Source: Matrix Refragged, pg 30
    '''
    def __init__(self, maxrating,rating=None,*args):
        super().__init__(maxrating,rating)
        self.name = 'Monitor'
        

    def baby(self,*args):
        new_rating = self.degrade()
        if new_rating >= 0:
            print(f'Querying Overwatch. Current rating {new_rating+1}; new rating {new_rating}')
        else:
            print(f'Monitor rating too low ({self.rating}). Cannot monitor. Aborting')


class BiofeedbackFilteringUtility(DegradableUtility):
    '''
Utility Name: Biofeedback Filtering
Type: Degradable, Operational
Description: A Biofeedback Filtering program may be used to soak Biofeedback Damage. Instead of applying the damage to the user’s real world condition monitor, the user may opt instead to Degrade their Biofeedback utility on a point-for-point basis.
Source: Matrix Refragged, pg 30
    '''
    def __init__(self, maxrating,rating=None,*args):
        super().__init__(maxrating,rating)
        self.name = 'Filter'
        

    def filter(self,count,*args):
        count = int(count[0])
        if count - self.rating >= 0:
            print(f'Filtering biofeedback damage. Current rating {self.rating}; new rating {self.rating-count}')
            for _ in range(count):
                new_rating = self.degrade()
        else:
            print(f'Biofeedbac Filterback rating too low ({self.rating}). Cannot filter damage. Aborting')

class BrowseUtility(BaseUtility):
    pass

class DecryptUtility(BaseUtility):
    '''
Name: Decrypt
Type: Offensive
Description: A Decrypt program decreases the user’s target number by its rating while utilizing the Crack Protections prompt to decode an Encrypted target. Base Decrypt time = (Encrypt Rating x10 minutes).
Source: Matrix Refragged, pg 30
    '''
    def __init__(self,maxrating,rating=None,*args):
        global DECRYPT_BONUS
        super().__init__(maxrating,rating)
        self.name = 'Decrypt'
        DECRYPT_BONUS = self.rating

class EncryptUtility(BaseUtility):
    pass

class EvasionUtility(BaseUtility):
    pass

class ExploitUtility(BaseUtility):
    pass

class JackpotUtility(BaseUtility):
    pass

class JamboreeUtility(BaseUtility):
    pass

class KillSwitchUtility(BaseUtility):
    pass

class LockOnUtility(BaseUtility):
    pass

class MedicUtility(BaseUtility):
    pass

class MirrorsUtility(BaseUtility):
    pass

class ReadWriteUtility(BaseUtility):
    pass

class RedirectUtility(BaseUtility):
    pass

class SaboteurUtility(BaseUtility):
    pass

class ShieldUtility(BaseUtility):
    pass

class SignalBoostUtility(BaseUtility):
    pass

class SlowUtility(BaseUtility):
    pass

class SmokeScreenUtility(BaseUtility):
    pass

class SnoopUtility(BaseUtility):
    pass

class SupressionUtility(DegradableUtility):
    '''
Utility Name: Supression
Type: Degradable, Operational
Description: The Suppression program may be utilized whenever a user crashes an icon. Instead of accruing a point of Overwatch, the user may choose to "suppress the crash" (see "Crash Suppression" on page 26). As a Degradable program, Suppression is reduced by 1 point after each use.
    '''
    def __init__(self,maxrating,rating=None,*args):
        super().__init__(maxrating,rating)
        self.name = 'Supression'

    def suppression(self):
        new_rating = self.degrade()
        if new_rating >= 0:
            print(f'Supressing alarm. Current rating {new_rating+1}; new rating {new_rating}')
        else:
            print(f'Supression rating too low ({self.rating}). Cannot supress alarms. Aborting.')


utilities_dictionary = {
        'sleaze':SleazeUtility,
        'analyze':AnalyzeUtility,
        'armor':ArmorUtility,
        'attack':AttackUtility,
        'baby':BabyMonitorUtility,
        'filter':BiofeedbackFilteringUtility,
        'browse':BrowseUtility,
        'decrypt':DecryptUtility,
        'encrypt':EncryptUtility,
        'evasion':EvasionUtility,
        'exploit':ExploitUtility,
        'jackpot':JackpotUtility,
        'jamboree':JamboreeUtility,
        'killswitch':KillSwitchUtility,
        'lockon':LockOnUtility,
        'medic':MedicUtility,
        'mirrors':MirrorsUtility,
        'io':ReadWriteUtility,
        'redirect':RedirectUtility,
        'saboteur':SaboteurUtility,
        'shield':ShieldUtility,
        'signal':SignalBoostUtility,
        'slow':SlowUtility,
        'smokescreen':SmokeScreenUtility,
        'snoop':SnoopUtility,
        'supression':SupressionUtility,
        'supress':SupressionUtility,
        'lol':LightOverloadDamage,
        'mol':ModerateOverloadDamage,
        'sol':SeriousOverloadDamage,
        'dol':DeadlyOverloadDamage,
        'nosebleed':NosebleedDamage,
        'blackout':BlackoutDamage,
        'killjoy':KilljoyDamage,
        'blackhammer':BlackhammerDamage
        }

attacks_list = ['lol','mol','sol','dol','nosebleed','blackout','killjoy','blackhammer']

if __name__ == '__main__':
    temp = SleazeUtility(6)
    temp.sleaze()