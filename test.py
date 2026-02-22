# -------------------------------
# MOLT DATA
# -------------------------------

# --- TAY QUAY CON TRUOT ---
# bodies = [
#     {
#         "name": "link1",
#         "parent": "world",
#         "joint": {"type": "hinge", "axis": "0 0 1"},
#         "pos": "0 0 0",
#         "geom": {"type": "capsule", "fromto": "0 0 0 1 0 0"}
#     },
#     {
#         "name": "link2",
#         "parent": "link1",
#         "joint": {"type": "hinge", "axis": "0 0 1"},
#         "pos": "1 0 0",
#         "geom": {"type": "capsule", "fromto": "0 0 0 1 0 0"},
#         "site": {"name": "link2_end", "pos": "1 0 0"}
#     },
#     {
#         "name": "slider",
#         "parent": "world",
#         "joint": {"type": "slide", "axis": "1 0 0"},
#         "pos": "2 0 0",
#         "geom": {"type": "box", "size": "0.15 0.15 0.15"},
#         "site": {"name": "slider_joint", "pos": "0 0 0"}
#     }
# ]

# constraints = [
#     {"type": "connect", "site1": "link2_end", "site2": "slider_joint"}
# ]

# --- CON LAC DON ---
# bodies = [
#     {
#         "name": "pendulum",
#         "parent": "world",
#         "joint": {
#             "type": "hinge",
#             "axis": "1 0 0"
#         },
#         "pos": "0 0 0",
#         "geom": {
#             "type": "capsule",
#             "fromto": "0 0 0 1 0 0",
#             "size": "0.05",
#             "density": "1000"
#         }
#     }
# ]

# constraints = []

# --- 4 KHAU BAN LE ---
bodies = [
    # Khâu 1: Crank
    {
        "name": "link1",
        "parent": "world",
        "joint": {
            "type": "hinge",
            "axis": "0 0 1"
        },
        "pos": "0 0 0",
        "geom": {
            "type": "capsule",
            "fromto": "0 0 0 1 0 0",
            "size": "0.05"
        },
        "site": {
            "name": "link1_end",
            "pos": "1 0 0"
        }
    },

    # Khâu 2: Coupler
    {
        "name": "link2",
        "parent": "link1",
        "joint": {
            "type": "hinge",
            "axis": "0 0 1"
        },
        "pos": "1 0 0",
        "geom": {
            "type": "capsule",
            "fromto": "0 0 0 1 0 0",
            "size": "0.05"
        },
        "site": {
            "name": "link2_end",
            "pos": "1 0 0"
        }
    },

    # Khâu 3: Rocker
    {
        "name": "link3",
        "parent": "world",
        "joint": {
            "type": "hinge",
            "axis": "0 0 1"
        },
        "pos": "2 0 0",
        "geom": {
            "type": "capsule",
            "fromto": "0 0 0 -1 0 0",
            "size": "0.05"
        },
        "site": {
            "name": "link3_end",
            "pos": "-1 0 0"
        }
    }
]

constraints = [
    # Nối coupler với rocker
    {
        "type": "connect",
        "site1": "link2_end",
        "site2": "link3_end"
    }
]


# MOLT → XML

def molt_to_xml(bodies, constraints, model_name="auto_model"):
    # build parent-child tree
    tree = {}
    for b in bodies:
        tree.setdefault(b["parent"], []).append(b)

    def body_to_xml(body, indent=4):
        sp = " " * indent
        lines = []

        lines.append(f'{sp}<body name="{body["name"]}" pos="{body["pos"]}">')

        # Joint
        if "joint" in body:
            j = body["joint"]
            jname = j.get("name", body["name"] + "_joint")
            lines.append(
                f'{sp}  <joint name="{jname}" type="{j["type"]}" axis="{j["axis"]}"/>'
            )

        # Geom
        if "geom" in body:
            g = body["geom"]
            gtype = g["type"]
            geom_attrs = [f'type="{gtype}"']

            for k, v in g.items():
                if k != "type":
                    geom_attrs.append(f'{k}="{v}"')

            # size
            if gtype == "capsule" and "size" not in g:
                geom_attrs.append('size="0.05"')

            lines.append(f'{sp}  <geom ' + " ".join(geom_attrs) + '/>')

        # Site
        if "site" in body:
            s = body["site"]
            size = s.get("size", "0.02")
            lines.append(
                f'{sp}  <site name="{s["name"]}" pos="{s["pos"]}" size="{size}"/>'
            )

        # Children
        for child in tree.get(body["name"], []):
            lines.extend(body_to_xml(child, indent + 2))

        lines.append(f"{sp}</body>")
        return lines

    xml = []
    xml.append(f'<mujoco model="{model_name}">')
    xml.append('  <option gravity="0 0 -9.81" timestep="0.002"/>')
    xml.append('  <worldbody>')

    # root bodies
    for root in tree.get("world", []):
        xml.extend(body_to_xml(root))

    xml.append('  </worldbody>')

    # constraints
    if constraints:
        xml.append('  <equality>')
        for c in constraints:
            if c["type"] == "connect":
                xml.append(
                    f'    <connect site1="{c["site1"]}" site2="{c["site2"]}"/>'
                )
        xml.append('  </equality>')

    xml.append('</mujoco>')
    return "\n".join(xml)


# -------------------------------
# GENERATE XML FILE
# -------------------------------

xml_text = molt_to_xml(bodies, constraints, model_name="name")

with open("XML.xml", "w") as f:
    f.write(xml_text)

print("XML.xml generated successfully.")
