import pygame as p
import random as r
import os
from PIL import Image

p.init()
p.mixer.init()

active_jumpscare = None
jumpscare_frame = 0
jumpscare_frame_timer = 0

jumpscare_files = {
    p.K_z: "assets/jumpscares/b.gif",      # Ballora
    p.K_x: "assets/jumpscares/m.gif",      # Mangle
    p.K_c: "assets/jumpscares/s.gif",      # Springtrap
    p.K_v: "assets/jumpscares/tb.gif",     # Toy Bonnie
    p.K_b: "assets/jumpscares/tc.gif",     # Toy Chica
    p.K_n: "assets/jumpscares/tf.gif",     # Toy Freddy
    p.K_g: "assets/jumpscares/j.webp"      # Golden Freddy
}

# ===== JUMPSCARE SOUNDS =====
jumpscare_sounds = {
    p.K_z: p.mixer.Sound("assets/audio/ba.ogg"),   # Ballora
    p.K_g: p.mixer.Sound("assets/audio/g.ogg"),    # Golden Freddy
    p.K_c: p.mixer.Sound("assets/audio/s.ogg"),    # Springtrap
    p.K_v: p.mixer.Sound("assets/audio/t.ogg"),    # Toy Bonnie
    p.K_n: p.mixer.Sound("assets/audio/t.ogg"),    # Toy Freddy
    p.K_b: p.mixer.Sound("assets/audio/t.ogg"),    # Toy Chica
    p.K_x: p.mixer.Sound("assets/audio/t.ogg"),    # Mangle
}
# ===== H2 ARRIVAL SOUNDS =====
h2_sounds = {
    "tb": p.mixer.Sound("assets/audio/tb.ogg"),
    "tf": p.mixer.Sound("assets/audio/tf.ogg"),
    "tc": p.mixer.Sound("assets/audio/tc.ogg"),
    "m":  p.mixer.Sound("assets/audio/m.ogg"),
    "ba": p.mixer.Sound("assets/audio/b.ogg"),
    "s": p.mixer.Sound("assets/audio/s.mp3"),  # optional for Springtrap
}
h2_playing = {}   # code -> channel that is playing its sound

jumpscares = {}

for key, path in jumpscare_files.items():
    frames = []
    durations = []

    with Image.open(path) as img:
        if getattr(img, "is_animated", False):
            for i in range(img.n_frames):
                img.seek(i)

                frame = img.convert("RGBA").resize((800, 600), Image.NEAREST)
                surface = p.image.frombytes(frame.tobytes(), frame.size, "RGBA")
                frames.append(surface)

                durations.append(max(20, img.info.get("duration", 100)))
        else:
            # Static image (Golden Freddy)
            frame = img.convert("RGBA").resize((800, 600), Image.NEAREST)
            surface = p.image.frombytes(frame.tobytes(), frame.size, "RGBA")
            frames.append(surface)
            durations.append(6000)

    jumpscares[key] = {
        "frames": frames,
        "durations": durations,
        "static": len(frames) == 1
    }

print("All seven jumpscares loaded!")

bb_sound = p.mixer.Sound("assets/audio/bb.mp3")
bb_active = False
bb_result = None
bb_timer = 0
bb_target = None
bb_cooldown = 0

# ===== AI levels / chances =====
tb = 5
tf = 5
tc = 5
m = 5
ba = 5
s = 5
j = 1

locations = {
    1: "Entrance", 2: "Stage", 3: "Dining Area", 4: "Party Room",
    5: "Bathroom", 6: "Prize Corner", 7: "Kid's Cove",
    8: "Kitchen", 9: "Spare Parts", 10: "h1", 11: "h2"
}

intro = p.mixer.Sound("menu.ogg")
start = p.mixer.Sound("start.mp3")

screen = p.display.set_mode((800, 600), p.FULLSCREEN)
p.display.set_caption("FNAF Mad Mix (ALPHA)")

icon = p.image.load("jj.jpg")
p.display.set_icon(icon)

button = p.Rect(100, 400, 200, 60)
buttonn = p.Rect(100, 500, 200, 60)

o = p.image.load("op.png")
q = p.image.load("assets/office.jpg")

font = p.font.Font(None, 36)
big_font = p.font.Font(None, 48)
text = font.render("Start", True, (255, 255, 255))
textt = font.render("Continue", True, (255, 255, 255))
text2 = font.render("Night 1", True, (255, 255, 255))

intro.play()
gm = "menu"

tbp = 2
ltbc = 0
tfp = 2
ltfc = 0
tcp = 2
ltcc = 0
sp = 1
ltsc = 0
bap = 4
ltbac = 0
mp = 7
ltmc = 0
ltjc = 0

mi = 5000

# ===== NIGHT TIMER =====
night_start_time = 0          # set when night actually begins
NIGHT_LENGTH = 540000          # 90 seconds = full night
hours = ["12 AM", "1 AM", "2 AM", "3 AM", "4 AM", "5 AM", "6 AM"]

tb_routes = {
    2: [10], 10: [3], 3: [11, 6], 6: [8], 8: [9], 9: [11], 11: []
}
tf_routes = {
    2: [10], 10: [3], 3: [11], 11: []
}
tc_routes = {
    2: [10], 10: [3, 5], 3: [6], 5: [10], 6: [8], 8: [9], 9: [11], 11: []
}
s_routes = {
    1: [3], 3: [10, 11], 10: [5, 3], 5: [10], 11: []
}
ba_routes = {
    4: [10], 10: [5, 3], 5: [10], 3: [11, 6], 6: [8], 8: [9], 9: [11], 11: []
}
m_routes = {
    7: [6], 6: [8, 3], 8: [9], 9: [11], 3: [11], 11: []
}

animatronic_routes = {
    "tb": tb_routes, "tf": tf_routes, "tc": tc_routes,
    "s": s_routes, "ba": ba_routes, "m": m_routes
}

def get_position(name):
    positions = {
        "tb": tbp, "tf": tfp, "tc": tcp,
        "s": sp, "ba": bap, "m": mp
    }
    return positions[name]

def set_position(name, new_pos):
    global tbp, tfp, tcp, sp, bap, mp
    if name == "tb": tbp = new_pos
    elif name == "tf": tfp = new_pos
    elif name == "tc": tcp = new_pos
    elif name == "s": sp = new_pos
    elif name == "ba": bap = new_pos
    elif name == "m": mp = new_pos

camera_open = False
camera_room = 1

camera_names = {
    1: "Entrance", 2: "Stage", 3: "Dining Area", 4: "Party Room",
    5: "Bathroom", 6: "Prize Corner", 7: "Kid's Cove",
    8: "Kitchen", 9: "Spare"
}

camera_folder = {
    1: "Entrance", 2: "Stage", 3: "Dining Area", 4: "Party Room",
    5: "Bathroom", 6: "Prize Corner", 7: "Kid's Cove",
    8: "Kitchen", 9: "Spare"
}

map_img = p.image.load("assets/MAP/map.png").convert_alpha()
map_img = p.transform.smoothscale(map_img, (200, 150))

animatronics = [
    ("tb", "Toy Bonnie", lambda: tbp),
    ("tf", "Toy Freddy", lambda: tfp),
    ("tc", "Toy Chica", lambda: tcp),
    ("s", "Springtrap", lambda: sp),
    ("ba", "Ballora", lambda: bap),
    ("m", "Mangle", lambda: mp),
]

camera_images = {}
for room_id, folder in camera_folder.items():
    folder_path = os.path.join("assets", "MAP", folder)
    camera_images[room_id] = {}
    if os.path.isdir(folder_path):
        for filename in os.listdir(folder_path):
            path = os.path.join(folder_path, filename)
            if not os.path.isfile(path):
                continue
            name, ext = os.path.splitext(filename)
            if ext.lower() not in (".png", ".webp", ".jpg", ".jpeg"):
                continue
            try:
                image = p.image.load(path).convert()
                image = p.transform.scale(image, (800, 600))
                camera_images[room_id][name.lower()] = image
            except p.error:
                print("Could not load camera image:", path)

arrival_order = ["tb", "tf", "tc", "s", "ba", "m"]
h2_attack_deadlines = {}

def note_arrival(code, old_pos, new_pos):
    if new_pos != old_pos:
        arrival_order.append(code)

    if new_pos == 11:
        # Arrived at H2
        h2_attack_deadlines[code] = p.time.get_ticks() + 10000
        print(f"{code} reached H2! 10 seconds!")

        # Play (and remember) the arrival sound
        if code in h2_sounds:
            # Stop previous one if any
            if code in h2_playing:
                h2_playing[code].stop()

            channel = h2_sounds[code].play()
            if channel:
                h2_playing[code] = channel

    elif old_pos == 11:
        # Left H2 → stop the sound
        h2_attack_deadlines.pop(code, None)

        if code in h2_playing:
            h2_playing[code].stop()
            del h2_playing[code]
            print(f"{code} left H2 — sound stopped")

def get_camera_image(room_id):
    states = camera_images.get(room_id, {})
    positions = {
        "tb": tbp, "tf": tfp, "tc": tcp,
        "s": sp, "ba": bap, "m": mp
    }
    room_animatronics = [
        code for code, _, get_pos in animatronics if get_pos() == room_id
    ]

    if room_id == 2:
        for state_name, image in states.items():
            suffix = state_name[1:]
            if not suffix:
                if not room_animatronics:
                    return image
                continue
            found_codes = []
            i = 0
            while i < len(suffix):
                if suffix.startswith("tb", i):
                    found_codes.append("tb"); i += 2
                elif suffix.startswith("tf", i):
                    found_codes.append("tf"); i += 2
                elif suffix.startswith("tc", i):
                    found_codes.append("tc"); i += 2
                elif suffix.startswith("ba", i):
                    found_codes.append("ba"); i += 2
                elif suffix.startswith("m", i):
                    found_codes.append("m"); i += 1
                elif suffix.startswith("s", i):
                    found_codes.append("s"); i += 1
                else:
                    i += 1
            if set(found_codes) == set(room_animatronics):
                return image
        for state_name, image in states.items():
            if state_name.isdigit():
                return image
        return None

    visible_code = None
    for code in reversed(arrival_order):
        if positions.get(code) == room_id:
            visible_code = code
            break

    if visible_code is None:
        for state_name, image in states.items():
            if state_name.isdigit():
                return image
        return None

    for state_name, image in states.items():
        suffix = state_name[1:].replace("(", "").replace(")", "")
        if state_name[0].isdigit() and suffix == visible_code:
            return image

    for state_name, image in states.items():
        suffix = state_name[1:].replace("(", "").replace(")", "")
        if visible_code in suffix:
            return image
    return None

def trigger_jumpscare(key):
    global active_jumpscare, jumpscare_frame, jumpscare_frame_timer
    active_jumpscare = key
    jumpscare_frame = 0
    jumpscare_frame_timer = p.time.get_ticks()
    if key in jumpscare_sounds:
        jumpscare_sounds[key].play()

def force_retreat(code):
    if get_position(code) != 11:
        return
    route = animatronic_routes[code]
    possible_rooms = {
        room for destinations in route.values()
        for room in destinations if room != 11
    }
    if possible_rooms:
        old_pos = get_position(code)
        new_pos = r.choice(list(possible_rooms))
        set_position(code, new_pos)
        note_arrival(code, old_pos, new_pos)
        print(f"{code} retreated to {locations[new_pos]}")

def get_current_hour():
    """Return the current hour string based on night progress."""
    if night_start_time == 0:
        return "12 AM"
    elapsed = p.time.get_ticks() - night_start_time
    # 90 seconds total → 6 hours (12AM to 6AM)
    # each hour = 15 seconds
    hour_index = min(6, int(elapsed / 90000))
    return hours[hour_index]

running = True
bb_delayed_time = None
bb_delayed_target = None

while running:
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False

        if event.type == p.KEYDOWN:
            if event.key in jumpscares and gm == "play" and not camera_open:
                trigger_jumpscare(event.key)

            # BB with 5 second cooldown
            if (event.key == p.K_j and gm == "play"
                    and not bb_active
                    and p.time.get_ticks() >= bb_cooldown):

                bb_sound.play(maxtime=3000)
                targets = [name for name in animatronic_routes if get_position(name) == 11]
                bb_active = True
                bb_timer = p.time.get_ticks()
                bb_cooldown = p.time.get_ticks() + 5000
                bb_target = None
                bb_result = "empty"

                if targets:
                    bb_target = r.choice(targets)
                    chance = r.randint(1, 100)
                    if chance <= 50:
                        bb_result = "retreat"
                        h2_attack_deadlines.pop(bb_target, None)
                    elif chance <= 80:
                        bb_result = "delayed"
                    else:
                        bb_result = "ignore"
                    print("BB targeted:", bb_target, "|", bb_result)
                else:
                    print("BB played, but nobody was at H2!")

            if gm == "play":
                if event.key == p.K_SPACE:
                    camera_open = not camera_open
                elif camera_open and p.K_1 <= event.key <= p.K_9:
                    camera_room = event.key - p.K_0

        if event.type == p.MOUSEBUTTONDOWN and gm == "menu":
            if event.button == 1 and button.collidepoint(event.pos):
                gm = "start"
                intro.stop()
                start.play()
                n1 = p.time.get_ticks()

    # Night intro
    if gm == "start":
        screen.fill((0, 0, 0))
        screen.blit(text2, text2.get_rect(center=(400, 300)))
        if p.time.get_ticks() - n1 >= 6000:
            gm = "play"
            night_start_time = p.time.get_ticks()   # start the night clock

    # Main menu
    if gm == "menu":
        screen.blit(o, (0, 0))
        p.draw.rect(screen, (50, 205, 50), button)
        screen.blit(text, text.get_rect(center=button.center))
        p.draw.rect(screen, (50, 205, 50), buttonn)
        screen.blit(textt, textt.get_rect(center=buttonn.center))

    # Gameplay
    if gm == "play" and active_jumpscare is None:
        now = p.time.get_ticks()

        # ===== NIGHT TIMER CHECK =====
        if night_start_time > 0:
            elapsed = now - night_start_time
            if elapsed >= NIGHT_LENGTH:
                print("6 AM! You survived!")
                running = False

        # BB outcome handling
        if bb_active and now - bb_timer >= 3000:
            if bb_result == "retreat":
                force_retreat(bb_target)
                print(f"BB worked! {bb_target} retreated immediately")
            elif bb_result == "delayed":
                h2_attack_deadlines.pop(bb_target, None)
                bb_delayed_time = now + 5000
                bb_delayed_target = bb_target
                print(f"BB delayed {bb_target} — will retreat in 5 seconds")
            elif bb_result == "ignore":
                print("BB failed. The countdown continues!")

            bb_active = False
            bb_result = None

        # Handle delayed retreat
        if bb_delayed_time is not None and now >= bb_delayed_time:
            force_retreat(bb_delayed_target)
            print(f"Delayed retreat: {bb_delayed_target} left H2")
            bb_delayed_time = None
            bb_delayed_target = None

        # H2 attacks
        for code, deadline in list(h2_attack_deadlines.items()):
            if now >= deadline and not camera_open:
                jumpscare_map = {
                    "tb": p.K_v, "tf": p.K_n, "tc": p.K_b,
                    "s": p.K_c, "ba": p.K_z, "m": p.K_x
                }
                key = jumpscare_map.get(code)
                if key:
                    trigger_jumpscare(key)
                h2_attack_deadlines.pop(code, None)
                print(f"{code} jumpscare!")
                break

        # Golden Freddy
        if now - ltjc >= mi and not camera_open:
            ltjc = now
            if r.random() * 100 < j:
                trigger_jumpscare(p.K_g)
                print("Golden Freddy appeared!")

        # Office / Camera display
        if not camera_open:
            screen.blit(q, (0, 0))
        else:
            screen.fill((0, 0, 0))
            if camera_room in (10, 11):
                screen.blit(font.render("NO CAMERA SIGNAL", True, (220, 220, 220)), (250, 280))
            else:
                image = get_camera_image(camera_room)
                if image:
                    screen.blit(image, (0, 0))
                else:
                    screen.blit(font.render("CAMERA FEED UNAVAILABLE", True, (220, 220, 220)), (200, 280))

            overlay = p.Surface((800, 70), p.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            title = font.render(
                f"CAM {camera_room}: {camera_names[camera_room]} | 1-9: Switch | SPACE: Lower",
                True, (255, 255, 255)
            )
            screen.blit(title, (18, 20))
            screen.blit(map_img, (585, 80))

        # ===== TIME DISPLAY (top left) =====
        current_hour = get_current_hour()
        time_surf = big_font.render(current_hour, True, (255, 255, 255))
        screen.blit(time_surf, (20, 15))

        # Animatronic movement
        if now - ltbc >= mi:
            ltbc = now
            if r.randint(1, 20) <= tb and tb_routes.get(tbp):
                old_pos = tbp
                tbp = r.choice(tb_routes[tbp])
                note_arrival("tb", old_pos, tbp)
                print("Toy Bonnie:", locations[old_pos], "->", locations[tbp])

        if now - ltfc >= mi:
            ltfc = now
            if r.randint(1, 20) <= tf and tf_routes.get(tfp):
                old_pos = tfp
                tfp = r.choice(tf_routes[tfp])
                note_arrival("tf", old_pos, tfp)
                print("Toy Freddy:", locations[old_pos], "->", locations[tfp])

        if now - ltcc >= mi:
            ltcc = now
            if r.randint(1, 20) <= tc and tc_routes.get(tcp):
                old_pos = tcp
                tcp = r.choice(tc_routes[tcp])
                note_arrival("tc", old_pos, tcp)
                print("Toy Chica:", locations[old_pos], "->", locations[tcp])

        if now - ltsc >= mi:
            ltsc = now
            if r.randint(1, 20) <= s and s_routes.get(sp):
                old_pos = sp
                sp = r.choice(s_routes[sp])
                note_arrival("s", old_pos, sp)
                print("Springtrap:", locations[old_pos], "->", locations[sp])

        if now - ltbac >= mi:
            ltbac = now
            if r.randint(1, 20) <= ba and ba_routes.get(bap):
                old_pos = bap
                bap = r.choice(ba_routes[bap])
                note_arrival("ba", old_pos, bap)
                print("Ballora:", locations[old_pos], "->", locations[bap])

        if now - ltmc >= mi:
            ltmc = now
            if r.randint(1, 20) <= m and m_routes.get(mp):
                old_pos = mp
                mp = r.choice(m_routes[mp])
                note_arrival("m", old_pos, mp)
                print("Mangle:", locations[old_pos], "->", locations[mp])

    # Jumpscare display
    if active_jumpscare is not None:
        data = jumpscares[active_jumpscare]
        now = p.time.get_ticks()

        if data["static"]:
            screen.blit(data["frames"][0], (0, 0))
            if now - jumpscare_frame_timer >= 6000:
                print("Game Over! (Golden Freddy)")
                running = False
        else:
            if now - jumpscare_frame_timer >= data["durations"][jumpscare_frame]:
                jumpscare_frame += 1
                jumpscare_frame_timer = now

            if jumpscare_frame >= len(data["frames"]):
                print("Game Over!")
                running = False
            else:
                screen.blit(data["frames"][jumpscare_frame], (0, 0))

    p.display.flip()

p.quit()