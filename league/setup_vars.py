__all__ = [
    "pebblers_per_div", "num_days", "last_division", "start_year", "start_month",
    "real_time", "cur_year", "cur_month", "cur_day", "pebbler_list",
    "rolls" ,"trigger_rates", "division_stats", "generate_schedule",
]

pebblers_per_div = 25
num_days = 25
last_division = "Learner"

start_year = 2023
start_month = 12

# REAL_TIME determines whether or not to use to actual time, set to false and modify
# CUR_YEAR, CUR_MONTH, and CUR_DAY to test the league running for certain amount of time
real_time = True
cur_year = 2025
cur_month = 7
cur_day = 13

pebbler_list = [
    {'name': 'Ally', 'description': 'An imposing yet loving alligator. Lives lavishly and spoils those she cares for.', 'isMale': False, 'trait': 'Skill', 'quirk': 'Proud Pebble', 'ability': 'Tip the Scales'},
    {'name': 'Ally Jr.', 'description': 'Daughter of Ally. Loves to adventure but never gets in too much trouble.', 'isMale': False, 'trait': 'Skill', 'quirk': 'Pity Pebble', 'ability': 'Tip the Scales'},
    {'name': 'Almond', 'description': 'Member of the Choco Chumps. Two-time runner-up on the Super Pebble Circuit.', 'isMale': True, 'trait': 'Power', 'quirk': 'Pity Pebble', 'ability': 'Tip the Scales'},
    {'name': 'Aurora', 'description': 'A gentle and unassuming turtle. Attracts attention due to her intricately designed exterior.', 'isMale': False, 'trait': 'Skill', 'quirk': 'Untouchable', 'ability': 'Miracle'},
    {'name': 'Aversa', 'description': 'A young pegasus who can channel both light and dark. Carries herself well despite her age.', 'isMale': False, 'trait': 'Grace', 'quirk': 'Untouchable', 'ability': 'Lucky Seven'},
    {'name': 'Baby', 'description': 'A young monkey with an unquenchable curiosity. Somehow manages to maintain a safe distance from any threats.', 'isMale': True, 'trait': 'Grace', 'quirk': 'Pity Pebble', 'ability': 'Will to Win'},
    {'name': 'Bamboo', 'description': 'Member of the Panda Posse. Likes to build structures out of whatever he can find.', 'isMale': True, 'trait': 'Grace', 'quirk': 'Pity Pebble', 'ability': 'Generosity'},
    {'name': 'Banji', 'description': 'Member of the Panda Posse. Gets some shuteye whenever given the opportunity.', 'isMale': True, 'trait': 'Grace', 'quirk': 'Even Temper', 'ability': 'Miracle'},
    {'name': 'Barry', 'description': 'An incredibly fast bear. Honors the fallen pebbler of the same name.', 'isMale': True, 'trait': 'Speed', 'quirk': 'Even Temper', 'ability': 'Tip the Scales'},
    {'name': 'Beefcake', 'description': 'A cow with a blocky body shape. Generally does not change his facial expression.', 'isMale': True, 'trait': 'Power', 'quirk': 'Proud Pebble', 'ability': 'Lucky Seven'},
    {'name': 'Berry', 'description': 'Apprentice to Waddles. Enjoys sweet treats and walks by the beach.', 'isMale': True, 'trait': 'Skill', 'quirk': 'Untouchable', 'ability': 'Lucky Seven'},
    {'name': 'Bert', 'description': 'A short fellow with a simple style. Some mistakenly assume he is angry due to his resting face.', 'isMale': True, 'trait': 'Power', 'quirk': 'Oddball', 'ability': 'Lucky Seven'},
    {'name': 'Bload', 'description': 'Member of the Toad Brigade. Three-time champion on the Supper Pebble Circuit.', 'isMale': True, 'trait': 'Speed', 'quirk': 'Pity Pebble', 'ability': 'Miracle'},
    {'name': 'Bloshi', 'description': 'A talented dinosaur capable of achieving great elevation. Widely admired and regarded as "cool".', 'isMale': True, 'trait': 'Skill', 'quirk': 'Pity Pebble', 'ability': 'Generosity'},
    {'name': 'Bloshi Jr.', 'description': 'Son of Bloshi. Aspires to one day live up to the image of his father.', 'isMale': True, 'trait': 'Skill', 'quirk': 'Pity Pebble', 'ability': 'Miracle'},
    {'name': 'Bonez', 'description': 'Member of the Yellow Fellows. Has a passion for travelling across the seas.', 'isMale': True, 'trait': 'Speed', 'quirk': 'Oddball', 'ability': 'Will to Win'},
    {'name': 'Brad', 'description': 'Member of the Toad Brigade. Has great eyesight and often uses it to spot faraway objects.', 'isMale': True, 'trait': 'Speed', 'quirk': 'Pity Pebble', 'ability': 'Will to Win'},
    {'name': 'Bumper', 'description': 'Member of the Fluffy Friends. His unique coloring makes him stand out from the crowd.', 'isMale': True, 'trait': 'Power', 'quirk': 'Even Temper', 'ability': 'Tip the Scales'},
    {'name': 'Buzz', 'description': 'One of the four emperors of the Pebble Kingdom. Controls lightning. Has lots of energy and is not afraid to expend it.', 'isMale': True, 'trait': 'Speed', 'quirk': 'Untouchable', 'ability': 'Tip the Scales'},
    {'name': 'Cammy', 'description': 'Lover to Edward. Can defend herself from evildoers with fierce kicks.', 'isMale': False, 'trait': 'Grace', 'quirk': 'Oddball', 'ability': 'Generosity'},
    {'name': 'Carrotz', 'description': 'Member of the Bunny Bunch. Likes to eat the local vegetation.', 'isMale': True, 'trait': 'Speed', 'quirk': 'Even Temper', 'ability': 'Lucky Seven'},
    {'name': 'Casey', 'description': 'Member of the Panda Posse. Particularly laid back and hard to bother under most circumstances.', 'isMale': True, 'trait': 'Grace', 'quirk': 'Even Temper', 'ability': 'Lucky Seven'},
    {'name': 'Chad', 'description': 'Member of the Toad Brigade. By far the strongest of the bunch and the one tasked with lifting stuff.', 'isMale': True, 'trait': 'Power', 'quirk': 'Proud Pebble', 'ability': 'Will to Win'},
    {'name': 'Chalk', 'description': 'Apprentice to Buzz. Always in a very festive mood no matter the circumstances.', 'isMale': True, 'trait': 'Speed', 'quirk': 'Untouchable', 'ability': 'Miracle'},
    {'name': 'Chaucer', 'description': 'A veteran hippo who has long since lost one eye. Honors the fallen pebbler Dante, his brother.', 'isMale': True, 'trait': 'Power', 'quirk': 'Proud Pebble', 'ability': 'Tip the Scales'},
    {'name': 'Cream', 'description': 'Member of the Fluffy Friends. Somewhat obsessed with keeping up with the latest trends.', 'isMale': False, 'trait': 'Power', 'quirk': 'Even Temper', 'ability': 'Lucky Seven'},
    {'name': 'Croc', 'description': 'Nephew to Ally. Loves to play hide and seek and excels at both sides.', 'isMale': True, 'trait': 'Skill', 'quirk': 'Even Temper', 'ability': 'Tip the Scales'},
    {'name': 'Cuddlez', 'description': 'Can learn any skill almost instantly. Despite his modest appearance, is capable of astronomical feats.', 'isMale': True, 'trait': 'Power', 'quirk': 'Oddball', 'ability': 'Tip the Scales'},
    {'name': 'Daffy', 'description': 'Member of the Dynamic Dinos. Well-acclimated to temperate environments with lots of flowers.', 'isMale': True, 'trait': 'Speed', 'quirk': 'Even Temper', 'ability': 'Will to Win'},
    {'name': 'Dave', 'description': 'Member of the Yellow Fellows. Honors the fallen pebbler of the same name.', 'isMale': True, 'trait': 'Speed', 'quirk': 'Oddball', 'ability': 'Generosity'},
    {'name': 'Dominic Bluey', 'description': 'Lover to Ima Reddy. He is quite charismatic but sometimes prone to worrying.', 'isMale': True, 'trait': 'Power', 'quirk': 'Pity Pebble', 'ability': 'Miracle'},
    {'name': 'Doug', 'description': 'A dog with a clear set of principles that he follows. Ordinary but capable of extraordinary feats.', 'isMale': True, 'trait': 'Speed', 'quirk': 'Proud Pebble', 'ability': 'Tip the Scales'},
    {'name': 'Duke', 'description': 'A dog with a clear set of principles that he follows. Ordinary but capable of extraordinary feats.', 'isMale': True, 'trait': 'Speed', 'quirk': 'Proud Pebble', 'ability': 'Generosity'},
    {'name': 'Duncan', 'description': 'An approachable pink blob. Can morph his body into different forms as needed.', 'isMale': True, 'trait': 'Power', 'quirk': 'Untouchable', 'ability': 'Generosity'},
    {'name': 'Edward', 'description': 'Lover to Cammy. Despite goofiness, possesses a remarkable sense of direction.', 'isMale': True, 'trait': 'Grace', 'quirk': 'Oddball', 'ability': 'Will to Win'},
    {'name': 'Ethan', 'description': 'Brother to Logan. Over time, has built credibility through quality interpersonal skills.', 'isMale': True, 'trait': 'Skill', 'quirk': 'Oddball', 'ability': 'Generosity'},
    {'name': 'Felix', 'description': 'Apprentice to Grumps. Possesses fierce claws and can climb walls.', 'isMale': True, 'trait': 'Power', 'quirk': 'Untouchable', 'ability': 'Will to Win'},
    {'name': 'Flapper', 'description': 'Member of the Fluffy Friends. Favors fashion trends that have gone out of style.', 'isMale': False, 'trait': 'Power', 'quirk': 'Even Temper', 'ability': 'Miracle'},
    {'name': 'Flippo', 'description': 'One of the four emperors of the Pebble Kingdom. Controls air. Rose from the ashes and became reincarnated into a new form.', 'isMale': True, 'trait': 'Grace', 'quirk': 'Untouchable', 'ability': 'Tip the Scales'},
    {'name': 'Frederick', 'description': "An incompressible ball of snow. Experience has taught him to be ready to fly at a moment's notice.", 'isMale': True, 'trait': 'Skill', 'quirk': 'Oddball', 'ability': 'Miracle'},
    {'name': 'Glad', 'description': 'Member of the Toad Brigade. Super friendly and can touch even the darkest of hearts.', 'isMale': True, 'trait': 'Speed', 'quirk': 'Pity Pebble', 'ability': 'Generosity'},
    {'name': 'Gnaf', 'description': 'Apprentice to Flippo. A talented dragon who can wield both fire and ice.', 'isMale': True, 'trait': 'Grace', 'quirk': 'Untouchable', 'ability': 'Generosity'},
    {'name': 'Gregory', 'description': 'A renowned plague doctor. It is said that he has never been met with a case that he could not cure.', 'isMale': True, 'trait': 'Skill', 'quirk': 'Even Temper', 'ability': 'Miracle'},
    {'name': 'Grumps', 'description': 'One of the four emperors of the Pebble Kingdom. Controls food. Led the fat cats to victory in the Super Pebble Circuit.', 'isMale': True, 'trait': 'Power', 'quirk': 'Untouchable', 'ability': 'Tip the Scales'},
    {'name': 'Hayley', 'description': 'Member of the Dynamic Dinos. Well-acclimated to cold environments with lots of snow.', 'isMale': False, 'trait': 'Skill', 'quirk': 'Even Temper', 'ability': 'Will to Win'},
    {'name': 'Hugz', 'description': 'Member of the Panda Posse. A true student of pebble competition who once hosted an invitational.', 'isMale': True, 'trait': 'Grace', 'quirk': 'Even Temper', 'ability': 'Generosity'},
    {'name': 'Ignatius', 'description': 'A creature of impressive stature. Often can be found sleeping, no matter the time of day.', 'isMale': True, 'trait': 'Power', 'quirk': 'Untouchable', 'ability': 'Lucky Seven'},
    {'name': 'Ima Reddy', 'description': 'Lover to Dominic Bluey. A storied pebbler who won Pebbledon enroute to the individual Super Pebble Circuit title.', 'isMale': False, 'trait': 'Power', 'quirk': 'Proud Pebble', 'ability': 'Miracle'},
    {'name': 'Jiggy', 'description': 'A bear who loves to hike across mountainous terrain. Something in his backpack allows him to hover for short periods of time.', 'isMale': True, 'trait': 'Grace', 'quirk': 'Oddball', 'ability': 'Lucky Seven'},
    {'name': 'Jolly', 'description': 'A cool dude with a keen sense of style. Has big dreams for when he grows up.', 'isMale': True, 'trait': 'Speed', 'quirk': 'Untouchable', 'ability': 'Will to Win'},
    {'name': 'Jonathan', 'description': 'An elf with a strong sense of duty. Naturally gifted at the game of hide and seek.', 'isMale': True, 'trait': 'Grace', 'quirk': 'Untouchable', 'ability': 'Miracle'},
    {'name': 'Juan', 'description': 'Am easy-going avocado slice. Enjoys sitting back and watching pebble competition when he is not involved.', 'isMale': True, 'trait': 'Power', 'quirk': 'Oddball', 'ability': 'Generosity'},
    {'name': 'Julie B.', 'description': 'Honorary member of the Yellow Fellows. Enjoys the company of those that can make her smile.', 'isMale': False, 'trait': 'Skill', 'quirk': 'Proud Pebble', 'ability': 'Lucky Seven'},
    {'name': 'Leo', 'description': 'A young tiger with remarkable resolve. Does not take himself too seriously and quick to smile.', 'isMale': True, 'trait': 'Skill', 'quirk': 'Proud Pebble', 'ability': 'Generosity'},
    {'name': 'Liam', 'description': 'A sloth who speaks in a low tone. Is never in any particular rush to go anywhere.', 'isMale': True, 'trait': 'Grace', 'quirk': 'Even Temper', 'ability': 'Tip the Scales'},
    {'name': 'Logan', 'description': 'Brother to Ethan. Is gifted at persuasion by making structured arguments that follow from one another.', 'isMale': True, 'trait': 'Skill', 'quirk': 'Oddball', 'ability': 'Will to Win'},
    {'name': 'Luke', 'description': 'A determined bear who takes his craft seriously. Cooperates well and is an asset in a team setting.', 'isMale': True, 'trait': 'Power', 'quirk': 'Pity Pebble', 'ability': 'Will to Win'},
    {'name': 'Marcel', 'description': 'A dog with a stocky build. Only relaxes after earning it with periods of high exertion.', 'isMale': True, 'trait': 'Speed', 'quirk': 'Proud Pebble', 'ability': 'Will to Win'},
    {'name': 'Marvin', 'description': 'A sea creature of unknown origin. Is a profound thinker despite his seemingly blank expression.', 'isMale': True, 'trait': 'Skill', 'quirk': 'Oddball', 'ability': 'Tip the Scales'},
    {'name': 'Matthew', 'description': 'A modest polar bear unlikely to cause any harm. Calculates potential outcomes before proceeding.', 'isMale': True, 'trait': 'Grace', 'quirk': 'Pity Pebble', 'ability': 'Miracle'},
    {'name': 'Mertz', 'description': 'A diligent handyman who you can count on regardless of the circumstance. Renowned for his innate jumping ability.', 'isMale': True, 'trait': 'Skill', 'quirk': 'Oddball', 'ability': 'Lucky Seven'},
    {'name': 'Monet', 'description': 'A serene squid who is not easily bothered. Finds joy in painting and has become more skilled after years of work.', 'isMale': True, 'trait': 'Grace', 'quirk': 'Proud Pebble', 'ability': 'Tip the Scales'},
    {'name': 'Moshi', 'description': 'Adopted son of Bloshi. Possesses innate talent yet without the years to wield it to its potential.', 'isMale': True, 'trait': 'Skill', 'quirk': 'Pity Pebble', 'ability': 'Lucky Seven'},
    {'name': 'Ness', 'description': 'A mysterious sea creature who prefers to wear plaid. Two-time winner on the Super Pebble Circuit.', 'isMale': True, 'trait': 'Grace', 'quirk': 'Pity Pebble', 'ability': 'Tip the Scales'},
    {'name': 'Nickelby', 'description': 'Stalwart defender of the Pebble Kingdom. Can deflect threats with his massive and bouncy belly.', 'isMale': True, 'trait': 'Power', 'quirk': 'Untouchable', 'ability': 'Miracle'},
    {'name': 'Nut', 'description': 'Member of the Choco Chumps. Stays strong by drinking milk routinely.', 'isMale': True, 'trait': 'Power', 'quirk': 'Even Temper', 'ability': 'Generosity'},
    {'name': 'Osh', 'description': 'A cute sea otter who dreams of being a samurai. Grows along with those he meets.', 'isMale': True, 'trait': 'Skill', 'quirk': 'Pity Pebble', 'ability': 'Will to Win'},
    {'name': 'Owen', 'description': 'A pig who finds pleasure in the simple things. Above all, likes to take in the sun on warm days.', 'isMale': True, 'trait': 'Grace', 'quirk': 'Pity Pebble', 'ability': 'Lucky Seven'},
    {'name': 'Pabu', 'description': 'A ferocious ferret who is tough to track down. Is experienced around fire and rock.', 'isMale': True, 'trait': 'Speed', 'quirk': 'Even Temper', 'ability': 'Miracle'},
    {'name': 'Papa', 'description': 'Guardian to Baby. Somehow manages to cause more damage than his charge despite having seniority.', 'isMale': True, 'trait': 'Grace', 'quirk': 'Proud Pebble', 'ability': 'Will to Win'},
    {'name': 'Pete', 'description': 'A spotted house plant with a strong bite. Sings catchy tunes and often dances while doing so.', 'isMale': True, 'trait': 'Power', 'quirk': 'Oddball', 'ability': 'Miracle'},
    {'name': 'Pigion', 'description': 'Member of the Yellow Fellows. While technically the leader of the band, he  prefers operating as a peer.', 'isMale': True, 'trait': 'Speed', 'quirk': 'Untouchable', 'ability': 'Generosity'},
    {'name': 'Pinky', 'description': 'A flamboyantly colored dolphin in excellent shape. Once volunteered as a guest star in a production.', 'isMale': True, 'trait': 'Skill', 'quirk': 'Even Temper', 'ability': 'Generosity'},
    {'name': 'Pip', 'description': 'Honorary emperor of the Pebble Kingdom. Grows along with those he meets.', 'isMale': True, 'trait': 'Skill', 'quirk': 'Even Temper', 'ability': 'Lucky Seven'},
    {'name': 'Raito', 'description': 'An elderly and battle-tested tiger. While physically not the same as he once was, his aura and wisdom demands respect.', 'isMale': True, 'trait': 'Skill', 'quirk': 'Proud Pebble', 'ability': 'Miracle'},
    {'name': 'Road', 'description': 'Member of the Toad Brigade. A natural leader who quickly gains the trust of his peers.', 'isMale': True, 'trait': 'Speed', 'quirk': 'Pity Pebble', 'ability': 'Tip the Scales'},
    {'name': 'Ruby', 'description': 'Member of the Dynamic Dinos. Well-acclimated to windy environments with lots of leaves.', 'isMale': False, 'trait': 'Power', 'quirk': 'Even Temper', 'ability': 'Will to Win'},
    {'name': 'Ruth', 'description': 'Member of the Choco Chumps. Known for her dependability, she is well-trusted by many.', 'isMale': False, 'trait': 'Power', 'quirk': 'Pity Pebble', 'ability': 'Generosity'},
    {'name': 'Shell', 'description': 'A cute turtle who dreams of firing cannons. Grows along with those he meets.', 'isMale': True, 'trait': 'Skill', 'quirk': 'Untouchable', 'ability': 'Generosity'},
    {'name': 'Shortstop', 'description': 'Member of the Bunny Bunch. Practices his ball-throwing skills whenever he gets the chance.', 'isMale': True, 'trait': 'Speed', 'quirk': 'Untouchable', 'ability': 'Lucky Seven'},
    {'name': 'Simon', 'description': 'Member of the Yellow Fellows. Has a good sense of humor even when jokes are at his expense.', 'isMale': True, 'trait': 'Speed', 'quirk': 'Oddball', 'ability': 'Lucky Seven'},
    {'name': 'Sir Rocco', 'description': 'Member of the Dynamic Dinos. Well-acclimated to arid environments with lots of sand.', 'isMale': True, 'trait': 'Grace', 'quirk': 'Even Temper', 'ability': 'Will to Win'},
    {'name': 'Snow', 'description': 'A little lamb who is highly curious. Prefers to learn something via direct experience.', 'isMale': True, 'trait': 'Grace', 'quirk': 'Oddball', 'ability': 'Miracle'},
    {'name': 'Spencer', 'description': 'A steadfast ram who finds the joy in any situation. Can produce several sustained surges of energy.', 'isMale': True, 'trait': 'Power', 'quirk': 'Oddball', 'ability': 'Will to Win'},
    {'name': 'Spot', 'description': 'A dog with a simple and scheduled lifestyle. Was a top pebbler in the pre Super Pebble Circuit era.', 'isMale': True, 'trait': 'Speed', 'quirk': 'Proud Pebble', 'ability': 'Lucky Seven'},
    {'name': 'Sprinkle', 'description': "A creature with an appetite that belies his small size. Can do anything he puts his mind to, but that often isn't much.", 'isMale': True, 'trait': 'Grace', 'quirk': 'Untouchable', 'ability': 'Will to Win'},
    {'name': 'Stewart', 'description': 'Member of the Yellow Fellows. Often experiences short-lived moments of glory.', 'isMale': True, 'trait': 'Speed', 'quirk': 'Oddball', 'ability': 'Tip the Scales'},
    {'name': 'Straw', 'description': 'An accommodating donut who is easy to get along with. Has a secret talent of designing and decorating.', 'isMale': True, 'trait': 'Grace', 'quirk': 'Proud Pebble', 'ability': 'Miracle'},
    {'name': 'Stretch', 'description': 'A young monkey with exceptional flexibility in his arms and legs. Enjoys playing around and hanging from trees.', 'isMale': True, 'trait': 'Grace', 'quirk': 'Oddball', 'ability': 'Tip the Scales'},
    {'name': 'Stripe', 'description': 'A tiger with intense focus. Holds himself to a high standard and can master repeatable tasks.', 'isMale': True, 'trait': 'Skill', 'quirk': 'Proud Pebble', 'ability': 'Will to Win'},
    {'name': 'Taro', 'description': 'A creature from beyond this world. Using some sort of sorcery he has made himself appear in a more youthful form.', 'isMale': True, 'trait': 'Skill', 'quirk': 'Untouchable', 'ability': 'Will to Win'},
    {'name': 'Timmy', 'description': 'A veteran dog who is respected and admired by those around him. Honors the fallen pebbler Tommy, his brother.', 'isMale': True, 'trait': 'Speed', 'quirk': 'Proud Pebble', 'ability': 'Miracle'},
    {'name': 'Toast', 'description': 'A slice of breakfast bread who likes to wearing a red beret to match his boots. Takes good care of himself and always smells nice.', 'isMale': True, 'trait': 'Grace', 'quirk': 'Proud Pebble', 'ability': 'Lucky Seven'},
    {'name': 'Tom', 'description': 'Member of the Yellow Fellows. Despite being relatively well-behaved always manages to get in trouble.', 'isMale': True, 'trait': 'Speed', 'quirk': 'Oddball', 'ability': 'Miracle'},
    {'name': 'Tonkotsu', 'description': 'A bowl of ramen with a vibrant personality. Cares about everyone and is quick to offer advice or assistance.', 'isMale': True, 'trait': 'Grace', 'quirk': 'Proud Pebble', 'ability': 'Generosity'},
    {'name': 'Tony', 'description': 'A studious and well-conditioned bear usually seen in red. Above all, he is kind and puts his friends above himself.', 'isMale': True, 'trait': 'Speed', 'quirk': 'Even Temper', 'ability': 'Generosity'},
    {'name': 'Waddles', 'description': 'One of the four emperors of the Pebble Kingdom. Controls water. Originally conceived the concept of pebble tournaments.', 'isMale': True, 'trait': 'Skill', 'quirk': 'Untouchable', 'ability': 'Tip the Scales'},
    {'name': 'Wasabi', 'description': 'A gorilla with a strong sense of justice. While initially guarded, is friendly with those he trusts.', 'isMale': True, 'trait': 'Power', 'quirk': 'Proud Pebble', 'ability': 'Generosity'},
    {'name': 'Watson', 'description': 'Member of the Bunny Bunch. What he looks in youthfulness he makes up for with wisdom.', 'isMale': True, 'trait': 'Power', 'quirk': 'Pity Pebble', 'ability': 'Lucky Seven'},
    {'name': 'Yoad', 'description': 'Member of the Toad Brigade. While he can often be found sleeping on the job, you can rest assured he is a valuable asset.', 'isMale': True, 'trait': 'Speed', 'quirk': 'Pity Pebble', 'ability': 'Lucky Seven'},
]

# Setup information needed for running the bouts
rolls = {
    "Power": [1, 1, 2, 5, 5, 6],
    "Grace": [1, 2, 4, 4, 5, 5],
    "Speed": [1, 1, 3, 3, 6, 6],
    "Skill": [1, 3, 3, 4, 4, 6],
}

trigger_rates = {
    "Generosity": 0.36,
    "Will to Win": 0.36,
    "Lucky Seven": 0.12,
    "Miracle": 0.12,
    "Tip the Scales": 0.24,
}

division_stats = {
    "Master"       : {"Quirk": 2, "Ability" : 2},
    "All-Star"     : {"Quirk": 2, "Ability" : 1},
    "Professional" : {"Quirk": 1, "Ability" : 1},
    "Learner"      : {"Quirk": 1, "Ability" : 0},
}

# Create a one indexed schedule for the next month
def generate_schedule():
    left = []
    right = []
    pebblers = pebblers_per_div
    pebblers += 1 # Bye
    matchups = pebblers // 2

    for i in range(1, pebblers + 1, 2):
        left.append(i)
    for i in range(2, pebblers + 1, 2):
        right.append(i)

    schedule = []

    # Hard coded to ensure each pebblers has equal home and away bouts
    homeAtOne = [2, 6, 10, 14, 18, 22, 5, 9, 13, 17, 21, 25]

    for _ in range(25):
        week_schedule = {"bouts": [], "bye": ""}
        for i in range(matchups):
            if left[i] == pebblers or right[i] == pebblers:
                week_schedule["bye"] = left[i] if left[i] != pebblers else right[i]
            else:
                if(i == 0 and right[i] in homeAtOne):
                    week_schedule["bouts"].append({"home": right[i], "away": left[i]})
                else:
                    week_schedule["bouts"].append({"home": left[i], "away": right[i]})

        schedule.append(week_schedule)

        # Rotate the schedule to create a round robin e.g.
        # 1 2    1 4    1 6    1 5    1 3
        # 3 4    2 6    4 5    6 3    5 2
        # 5 6    3 5    2 3    4 2    6 4

        rightToLeft = right[0]
        leftToRight = left[-1]

        for i in range(pebblers // 2 - 2):
            left[-1 - i] = left[-2 - i]

        for i in range(pebblers // 2 - 1):
            right[i] = right[i + 1]

        right[-1] = leftToRight
        left[1] = rightToLeft

    return schedule