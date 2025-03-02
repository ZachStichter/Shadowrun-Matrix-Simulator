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
            print(f'Rating for {self.name} greater than theoretical maximum. Overwrite settings?')
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

    def get_bonus(self):
        return self.rating

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
        self.initialized = True

class ArmorUtility(DegradableUtility):
    '''
Utility Name: Armor
Type: Operational, Degradable
Description: An Armor program may be used to soak Overload Damage. Instead of applying the damage to the user’s Matrix condition monitor, the user may opt instead to Degrade their Armor utility on a point-for-point basis.
Source: Matrix Refragged, pg 30
    '''
    def __init__(self, maxrating,rating=None,*args):
        super().__init__(maxrating,rating)
        self.name = 'Armor'
        

    def armor(self,count,*args):
        count = int(count[0])
        if self.rating - count >= 0:
            print(f'Blocking overload damage. Current rating {self.rating}; new rating {self.rating-count}')
            for _ in range(count):
                new_rating = self.degrade()
        else:
            print(f'Armor rating too low ({self.rating}). Cannot filter damage. Aborting')

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
                                'lvl':'light',
                                'name': 'Light Overload'
                                    },
                            'mol':{
                                'typ':'overload',
                                'lvl':'moderate',
                                'name':'Moderate Overload'
                                },
                            'sol':{
                                'typ':'overload',
                                'lvl':'serious',
                                'name':'Serious Overload'
                                },
                            'dol':{
                                'typ':'overload',
                                'lvl':'deadly',
                                'name':'Deadly Overload'
                                },
                            'nosebleed':{
                                'typ':'biofeedback',
                                'lvl':'light',
                                'name':'Nosebleed'
                                },
                            'blackout':{
                                'typ':'biofeedback',
                                'lvl':'moderate',
                                'name':'Blackout'
                                },
                            'killjoy':{
                                'typ':'biofeedback',
                                'lvl':'severe',
                                'name':'Killjoy'
                                },
                            'blackhammer':{
                                'typ':'biofeedback',
                                'lvl':'deadly',
                                'name':'Black Hammer'
                                },
                            'slow':{
                                'typ':'initiative',
                                'lvl':'special',
                                'name':'slow'
                            }
                            }
        self.name=self.dmg_type_dict[name]['name']
        self.dmg_type = self.dmg_type_dict[name]['typ']
        self.dmg_level = self.dmg_type_dict[name]['lvl']

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

class SlowDamage(AttackUtility):
    '''
Name: Slow
Type: Combat
Description: Slow is a specialized combat program designed to bog down an icon in sluggish or harmful code, causing the target’s Initiative score to degrade. When a user utilizes Slow in conjunction with the Attack an Icon prompt, they may opt to reduce the target icon’s Initiative score by 3 points for each net success generated on the test (instead of applying them to stage damage) However, should the target icon win the Cybercombat test, it may choose to inflict its own damage, as normal). Initiative degraded in this way may affect subsequent combat phases, and is lost until Initiative is rerolled at the top of the next Combat Turn. Icon’s whose Initiative is reduced to zero within a single turn crash, dumping their users from the Matrix, if applicable, and leaving their icon “frozen” or running in place before they inevitably fade from the Matrix.
Source: Matrix Refragged, pg 
    '''
    def __init__(self,*args):
        super().__init__(0,'slow',*args)

    def attack(self):
        return f"Dealing {self.dmg_level} {self.dmg_type} damage. All successes reduce the target's initiative by 3."


class BabyMonitorUtility(DegradableUtility):
    '''
Utility Name: Baby Monitor
Type: Degradable, Operational
Description: Baby Monitor is an operational program designed to allow a user to get a peek at their current Overwatch level. Whenever the user activates the Scrub Datastream prompt, the GM should relay the number of boxes accrued as Overwatch in terms of wound levels (Light, Moderate, Serious, etc). As a Degradable program, Baby Monitor is reduced by 1 point after each use.
Source: Matrix Refragged, pg 30
    '''
    def __init__(self, maxrating,rating=None,*args):
        super().__init__(maxrating,rating)
        self.name = 'Baby Monitor'
        
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
        self.name = 'Biofeedback Filtering'
        

    def filter(self,count,*args):
        count = int(count[0])
        if self.rating - count >= 0:
            print(f'Filtering biofeedback damage. Current rating {self.rating}; new rating {self.rating-count}')
            for _ in range(count):
                new_rating = self.degrade()
        else:
            print(f'Biofeedback Filterback rating too low ({self.rating}). Cannot filter damage. Aborting')

class BrowseUtility(BaseUtility):
    '''
Name: Browse
Type: Offensive
Description: A Browse program decreases the user’s target number by its rating while utilizing any Index prompts. This includes Index Data Store, Index Subscribed Devices, and Index Users and Scheduling.
Source: Matrix Refragged, pg 30
    '''
    def __init__(self,rating,*args):
        super().__init__()
        self.name = 'Browse'
        self.rating = rating


class DecryptUtility(BaseUtility):
    '''
Name: Decrypt
Type: Offensive
Description: A Decrypt program decreases the user’s target number by its rating while utilizing the Crack Protections prompt to decode an Encrypted target. Base Decrypt time = (Encrypt Rating x10 minutes).
Source: Matrix Refragged, pg 30
    '''
    def __init__(self,rating,*args):
        super().__init__()
        self.name = 'Decrypt'
        self.rating=rating

class EncryptUtility(BaseUtility):
    '''
Name: Encrypt
Type: Operational
Description: An Encrypt program is an operational program designed to Encrypt a target (usually a datafile or datastream). Whenever the user successfully utilizes the Configure Protections prompt, they may choose to Encrypt the target up to the rating of the utility. A single success is all that’s required to complete the action.
Source: Matrix Refragged, pg 31
    '''
    def __init__(self,rating,*args):
        super().__init__()
        self.name = 'Encrypt'
        self.rating=rating

class EvasionUtility(DegradableUtility):
    '''
Name: Evasion
Type: Degradable, Operational
Description: An Evasion program allows the user to utilize the Toggle Visibility prompt to become Hidden, evenwhile currently Link-Locked. As a Degradable program, Evasion is reduced by 1 point after each use.
Source: Matrix Refragged, pg 31
    '''
    def __init__(self,maxrating,rating=None,*args):
        super().__init__(maxrating,rating)
        self.name='Evasion'

    def evasion(self,*args):
        new_rating = self.degrade()
        if new_rating >= 0:
            print(f'Toggling visibility to hidden. Current rating {new_rating+1}; new rating {new_rating}')
        else:
            print(f'Evasion rating too low ({self.rating}). Cannot evade link lock. Aborting')

class ExploitUtility(DegradableUtility):
    '''
Name: Exploit
Type: Degradable, Offensive
Description: An Exploit program decreases the user’s target number by its rating while utilizing the Access Node prompt. As a Degradable program, Exploit is reduced by 1 point after each use.
Source: Matrix Refragged, pg 31
    '''
    def __init__(self,maxrating, rating=None,*args):
        super().__init__(maxrating,rating)
        self.name='Exploit'

    def exploit(self,*args):
        new_rating = self.degrade()
        if new_rating >= 0:
            print(f'Found vulnerability in host node. Exploiting it now. Current rating {new_rating+1}; new rating {new_rating}')
        else:
            print(f'Exploit rating too low ({self.rating}). Cannot boost attack.')
    
    def get_bonus(self):
        bonus = self.rating
        self.exploit()
        return bonus

class JackpotUtility(DegradableUtility):
    '''
Name: Jackpot
Type: Degradable, Operational
Description: A Jackpot program decreases the user’s target number by its rating while utilizing the Siphon Paydata prompt. As a Degradable program, Jackpot is reduced by 1 point after each use.
Source: Matrix Refragged, pg
    '''
    def __init__(self,maxrating, rating=None,*args):
        super().__init__(maxrating,rating)
        self.name='Jackpot'

    def jackpot(self,*args):
        new_rating = self.degrade()
        if new_rating >= 0:
            print(f'Enabling the Judiciously Acquiring Contraband Knowledge Protocol on Terminal (J.A.C.K.P.O.T.). Current rating {new_rating+1}; new rating {new_rating}')
        else:
            print(f'Jackpot rating too low ({self.rating}). Cannot boost siphon operations.')
    
    def get_bonus(self):
        bonus = self.rating
        self.jackpot()
        return bonus

class JamboreeUtility(BaseUtility):
    '''
Name: Jamboree
Type: Offensive
Description: A Jamboree program decreases the user’s target number by its rating while utilizing the Jam Signal prompt to make a target icon eat static.
Source: Matrix Refragged, pg 31
    '''
    def __init__(self,rating,*args):
        super().__init__()
        self.name = 'Jamboree'
        self.rating=rating

class KillSwitchUtility(BaseUtility):
    '''
Name: Kill Switch
Type: Offensive
Description: A Kill Switch program decreases the user’s target number by its rating while utilizing the Crack Protections prompt to disarm a Databombed target. Base Decrypt time = (Encrypt Rating x10 minutes). Failure results in the self-destruction of the target icon.
Source: Matrix Refragged, pg 31
    '''
    def __init__(self,rating,*args):
        super().__init__()
        self.name = 'Kill Switch'
        self.rating=rating


class LockOnUtility(BaseUtility):
    '''
Name: Lock-On
Type: Offensive, Operational
Description: The Lock-On program decreases the user’s target number by its rating while utilizing the Trace Signal prompt against a Visible icon. If the user scores even a single success on the test, they establish a Link-Lock with the target.
Source: Matrix Refragged, pg 31
    '''
    def __init__(self,rating,*args):
        super().__init__()
        self.name = 'Lock On'
        self.rating=rating

class MedicUtility(DegradableUtility):
    '''
Name: Medic
Type: Degradable, Offensive
Description: A Medic program decreases the user’s target numbers by its rating when utilizing the Repair an Icon prompt. As a Degradable program, Medic is reduced by 1 point after each use.
Source: Matrix Refragged, pg 31
    '''
    def __init__(self,maxrating, rating=None,*args):
        super().__init__(maxrating,rating)
        self.name='Medic'

    def medic(self,*args):
        new_rating = self.degrade()
        if new_rating >= 0:
            print(f'Enabling Mobile emergency diagnostic immune classifier (M.E.D.I.C.). Current rating {new_rating+1}; new rating {new_rating}')
        else:
            print(f'Medic rating too low ({self.rating}). Cannot boost healing.')
    
    def get_bonus(self):
        bonus = self.rating
        self.medic()
        return bonus

class MirrorsUtility(DegradableUtility):
    '''
Name: Mirrors
Type: Degradable
Description: A Mirrors program decreases the user’s target number by its rating while being scrutinized by a System Sweep, or the Authenticate ability of some agents (see “Agent Special Abilities” on page 38). The program works by spamming a wave of token icons into the system. The tokens appear to lend credibility to a user’s presence, and appear as falsified employment records, bogus certifications, registries of forged timestamps, counterfeit payroll records, and the like. Upon detailed inspection the tokens are clearly deceptive, but the ruse is often good enough to avoid the scrutiny of many hostile IC. As a Degradable program, Mirrors is reduced by 1 point after each use.
Source: Matrix Refragged, pg 31
    '''
    def __init__(self,maxrating, rating=None,*args):
        super().__init__(maxrating,rating)
        self.name='Mirrors'

    def mirrors(self,*args):
        new_rating = self.degrade()
        if new_rating >= 0:
            print(f'Detecting system sweep. Deploying countermeasures. Current rating {new_rating+1}; new rating {new_rating}')
        else:
            print(f'Mirrors rating too low ({self.rating}). Cannot disguise.')
    
    def get_bonus(self):
        bonus = self.rating
        self.mirrors()
        return bonus

class ReadWriteUtility(BaseUtility):
    '''
Name: Read/Write
Type: Offensive
Description: The Read/Write program decreases the user’s target number by its rating while utilizing any Datafile prompts, including Access, Duplicate/Download, or Edit/Upload prompts.
Source: Matrix Refragged, pg 31
    '''
    def __init__(self,rating,*args):
        super().__init__()
        self.name = 'Read/Write'
        self.rating=rating

class RedirectUtility(DegradableUtility):
    '''
Name: Redirect
Type: Defensive, Degradable
Description: A Redirect program increases the target number by its rating, for enemy icons attempting to target the user with the Trace Signal prompt. As a Degradable program, Redirect is reduced by 1 point after each use.
Source: Matrix Refragged, pg 31
    '''
    def __init__(self,maxrating, rating=None,*args):
        super().__init__(maxrating,rating)
        self.name='Redirect'

    def redirect(self,*args):
        new_rating = self.degrade()
        if new_rating >= 0:
            print(f"Detecting signal trace. Deploying countermeasures. Current rating {new_rating+1}; new rating {new_rating}.\nIncrease the opponent's target number by +{new_rating+1}")
        else:
            print(f'Redirect rating too low ({self.rating}). Cannot counter signal trace.')

class SaboteurUtility(BaseUtility):
    '''
Name: Saboteur
Type: Operational
Description: A Saboteur program is an operational program designed to Databomb a datafile or similar icon. Whenever the user successfully utilizes the Configure Protections prompt, they may choose to Databomb an unprotected target up to the rating of the utility. A single success is all that’s required to complete the action.
Source: Matrix Refragged, pg 32
    '''
    def __init__(self,rating,*args):
        super().__init__()
        self.name = 'Saboteur'
        self.rating=rating

    def databomb(self):
        print(f'Attempting to Databomb icon. One success means this icon can be databombed up to rating {self.rating}.')


class ShieldUtility(DegradableUtility):
    '''
Name: Shield
Type: Operational, Degradable
Description: A Shield program may be used to mitigate the special attacks of many IC Agents that target the user’s hardware (such as their MPCP, Memory, utilities, or utility slots). Instead of applying the degradation to the user’s hardware, the user may opt instead to Degrade their Shield utility on a point-for-point basis.
Source: Matrix Refragged, pg 
    '''
    def __init__(self, maxrating,rating=None,*args):
        super().__init__(maxrating,rating)
        self.name = 'Shield'
        

    def shield(self,count,*args):
        count = int(count[0])
        if self.rating - count >= 0:
            print(f'Blocking hardware damage. Current rating {self.rating}; new rating {self.rating-count}')
            for _ in range(count):
                new_rating = self.degrade()
        else:
            print(f'Shield rating too low ({self.rating}). Cannot absorb damage. Aborting')

class SignalBoostUtility(BaseUtility):
    '''
Name: Signal Booster
Type: Offensive
Description: A Signal Booster program decreases the user’s target number by its rating while utilizing the Send Transmission prompt.
Source: Matrix Refragged, pg 32
    '''
    def __init__(self,rating,*args):
        super().__init__()
        self.name = 'Signal Booster'
        self.rating=rating

class SmokeScreenUtility(DegradableUtility):
    '''
Name: Smoke Screen
Type: Defensive, Degradable
Description: A Smoke Screen program increases the target number by its current rating for enemy icons attempting to target the user with the Search and Render prompt. As a Degradable program, Smoke Screen is reduced by 1 point after each use.
Source: Matrix Refragged, pg 32
    '''
    def __init__(self,maxrating, rating=None,*args):
        super().__init__(maxrating,rating)
        self.name='Smoke Screen'

    def smokescreen(self,*args):
        new_rating = self.degrade()
        if new_rating >= 0:
            print(f"Detecting search and render prompt. Deploying countermeasures. Current rating {new_rating+1}; new rating {new_rating}.\nIncrease the opponent's target number by +{new_rating+1}")
        else:
            print(f'Smoke screen rating too low ({self.rating}). Cannot counter search and render.')

class SnoopUtility(BaseUtility):
    '''
Name: Snoop
Type: Offensive
Description: A Snoop program decreases the user’s target numbers by its rating while utilizing the Tap Datastream, or Spoof Datastream prompts.
Source: Matrix Refragged, pg 32
    '''
    def __init__(self,rating,*args):
        super().__init__()
        self.name = 'Snoop'
        self.rating=rating

class SupressionUtility(DegradableUtility):
    '''
Utility Name: Supression
Type: Degradable, Operational
Description: The Suppression program may be utilized whenever a user crashes an icon. Instead of accruing a point of Overwatch, the user may choose to "suppress the crash" (see "Crash Suppression" on page 26). As a Degradable program, Suppression is reduced by 1 point after each use.
Source: Matrix Refragged, pg 32
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
        'slow':SlowDamage,
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

attacks_list = ['lol','mol','sol','dol','nosebleed','blackout','killjoy','blackhammer','slow']

if __name__ == '__main__':
    temp = SleazeUtility(6)
    temp.sleaze()