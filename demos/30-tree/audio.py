# 一棵树的三十秒 — soundtrack.
# 30 s of pop (F major, 120 BPM) whose drop is the summer crown, not a beat grid.
# Everything is pinned to cues.json frame numbers, so picture and sound cannot drift.
import sys, json, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lib', 'audio'))
import mgaudio as mg
from mgaudio import recipes, sfx, theory, synth, drums, seq

HERE = os.path.dirname(os.path.abspath(__file__))
cues = json.load(open(os.path.join(HERE, 'cues.json'), encoding='utf-8'))
FR = {c['name']: c['frame'] for c in cues['cues']}
FPS = cues['fps']
T = lambda k: FR[k] / FPS
F = lambda n: n / FPS

# ---- bed. 30 s is four 7.5 s seasons, so the form gets four sections, not one drop.
# drop = the summer crown (the visual peak); outro = winter; final = the closing sprout.
m = recipes.pop(
    duration=30.0, bpm=120, key='F', mode='major', prog='I vi IV V',
    build=T('summer_in') - 2.0, drop=T('summer_in'), outro=T('winter_in'),
    music_level=-20.0,
)
print(m.form.summary() if hasattr(m.form, 'summary') else m.form)
print('tracks:', list(m.tracks))
note = lambda t, i=-1, sh=12: m.form.chord_at(t, sh)[i]

# ---- ACT I 春: one seed, one bloom. Almost silent, then a single warm entry.
m.sfx(sfx.whoosh(0.34, 'air', direction=1, peak=0.6), at=T('seed_drop') - F(3), gain=-24)
m.sfx(sfx.pop('soft', pitch=1.05), at=T('seed_land'), gain=-7)
m.sfx(sfx.impact('soft'), at=T('seed_land'), gain=-13)
m.sfx(sfx.pop('mouth', pitch=0.82), at=T('sprout'), gain=-4)
m.sfx(sfx.whoosh(0.5, 'swish', direction=1, peak=0.45), at=T('sprout') + F(2), gain=-18)
# each leaf cluster gets a soft marimba note — the crown literally plays itself into being
mar = m.track('mar', level=-23, sends={'plate': -14, 'delay': -20}, group='music')
for k, n in enumerate(['F5', 'A5', 'C6', 'F6', 'C6', 'A5']):
    mar.add(synth.pluck(n, 0.7, 0.7), T('leaf_a') + k * F(6))
for k, n in enumerate(['F4', 'A4', 'C5', 'E5', 'G5', 'A5', 'C6', 'F6']):
    mar.add(synth.pluck(n, 0.6, 0.55), T('leaf_b') + k * F(4))

# ---- ACT II 夏: the drop. Full groove, the tree is complete.
m.sfx(sfx.impact('punch'), at=T('summer_in'), gain=-5)
m.sfx(sfx.pop('bubble', pitch=1.0), at=T('summer_in') + F(1), gain=-6, pan=-0.3)
m.sfx(sfx.pop('bubble', pitch=1.1), at=T('summer_in') + F(3), gain=-8, pan=0.3)
m.sfx(sfx.sparkle(0.7, key='F'), at=T('first_fruit'), gain=-17, verb=-12)
m.sfx(sfx.ding('F6'), at=T('first_fruit'), gain=-14, pan=-0.25)
m.sfx(sfx.shimmer_hit('A5'), at=T('full_crown'), gain=-12, pan=0.2, verb=-11)
m.sfx(sfx.whoosh(0.6, 'air', direction=1, peak=0.5), at=T('full_crown') - F(4), gain=-18)

# ---- ACT III 秋: the groove thins out one layer at a time; falling leaves get one note each.
for k in range(10):
    m.sfx(sfx.paper('slide', 0.09), at=T('first_fall') + k * F(9), gain=-24, pan=(-1) ** k * 0.35)
    mar.add(synth.pluck(['A4', 'C5', 'E5', 'F5'][k % 4], 0.5, 0.34), T('first_fall') + k * F(9))
m.sfx(sfx.whoosh(1.1, 'air', direction=-1, peak=0.5), at=T('leaf_fall_mid'), gain=-22)
# the moment the tree is bare, everything drops away: one low string, no drums
m.sfx(sfx.impact('thud'), at=T('bare'), gain=-14)
m.sfx(sfx.paper('rustle', 0.5), at=T('bare') + F(3), gain=-22)

# ---- ACT IV 冬: night. Wind, snow, and almost nothing else.
m.sfx(sfx.whoosh(2.4, 'air', direction=1, peak=0.5), at=T('winter_in'), gain=-16, pan=-0.2)
m.sfx(sfx.whoosh(2.0, 'air', direction=-1, peak=0.5), at=T('winter_in') + 1.6, gain=-20, pan=0.25)
m.sfx(sfx.chime(('F5', 'A5', 'C6'), 0.12), at=T('moon_hold'), gain=-19, verb=-14)
m.sfx(sfx.sparkle(1.4, key='F', density=16), at=T('snow_peak'), gain=-25, verb=-14)

# ---- the bookend: a new sprout, the same two notes as the opening seed
m.sfx(sfx.pop('soft', pitch=1.25), at=T('sprout_new'), gain=-9)
m.sfx(sfx.pop('mouth', pitch=1.3), at=T('leaf_new'), gain=-8, pan=0.15)
m.sfx(sfx.chime(('F6', 'A6'), 0.16), at=T('leaf_new') + F(2), gain=-17, verb=-12)
m.sfx(sfx.shimmer_hit('F6'), at=T('hold_end'), gain=-15, verb=-13)

# ---- the mix: duck the bed under every picture event so the hits read
HITS = [T('seed_land'), T('sprout'), T('summer_in'), T('full_crown'),
        T('bare'), T('winter_in'), T('sprout_new'), T('hold_end')]
pts = [(0.0, 0.0)]
for h in HITS:
    pts += [(max(0.0, h - 0.12), 0.0), (max(0.0, h - 0.06), -5.5), (h, 0.0)]
m.group('music').automate('gain', pts + [(30.0, 0.0)])

# Seasons thin the arrangement: midsummer is full, winter is sparse but NEVER silent.
# Earlier this pushed the groove to -13 dB and left an 11 s hole; a winter act needs a
# bed you can hear, just a thinner one.
for k in ('arp', 'hat', 'chords'):
    if k in m.tracks:
        m[k].automate('gain', [(0, -4.0), (T('summer_in'), 0.0), (T('bare'), -5.0),
                               (T('winter_in'), -8.0), (T('sprout_new'), -3.0), (30.0, -1.5)])
# kick/clap carry the winter section — pull them out of the silence instead of muting
for k in ('kick', 'clap', 'bass'):
    if k in m.tracks:
        m[k].automate('gain', [(0, -6.0), (T('summer_in'), 0.0), (T('bare'), -7.0),
                               (T('winter_in'), -9.0), (T('sprout_new'), -2.0), (30.0, -4.0)])

# A pad under winter so the empty stretch still has a floor. Without this the film's
# quietest act is literally 11 s of nothing, which reads as a broken file.
padw = m.track('winterpad', level=-26, sends={'hall': -10}, group='music')
padw.add(synth.pad(['F3', 'A3', 'C4'], 6.2, 0.55, 'strings', attack=1.4, release=2.0), T('winter_in') - 0.6)
padw.add(synth.pad(['D3', 'F3', 'A3'], 5.0, 0.45, 'strings', attack=1.2, release=1.8), T('winter_in') + 5.4)
padw.add(synth.pad(['F3', 'C4', 'F4'], 4.6, 0.5, 'strings', attack=0.8, release=1.6), T('push_in'))

os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
res = m.export(os.path.join(HERE, 'out/audio.wav'), lufs=-14, tp=-2.2,
               spectrogram=os.path.join(HERE, 'out/audio_spec.png'))
print({k: res[k] for k in ('duration', 'lufs', 'true_peak', 'stereo_corr', 'bands', 'warnings') if k in res})
m.report()
