floor ={}

# floor = {
#     "type": "plane",
#     "pos" : "0 0 -0.2",
#     "size": "5 5 0.1",
#     "rgba": "0.8 0.8 0.8 1"
# }

# TXT
with open("Result/TXT.txt", "r") as f:
    content = f.read()

data = {}
exec(content, data)

bodies = data["bodies"]
constraints = data["constraints"]

# XML
def molt_to_xml(bodies,
                constraints=None,
                model_name="test",
                actuators=None,
                floor=None):

    constraints = constraints or []
    actuators = actuators or []

    tree = {}
    for b in bodies:
        tree.setdefault(b["parent"], []).append(b)

    # auto name joint
    for body in bodies:
        if "joint" in body:
            body["joint"].setdefault(
                "name",
                f'{body["name"]}_joint'
            )

    def dict_to_attr(d):
        return " ".join(f'{k}="{v}"' for k, v in d.items())

    def body_to_xml(body, indent=4):
        sp = " " * indent
        lines = []

        lines.append(f'{sp}<body name="{body["name"]}" pos="{body["pos"]}">')

        if "joint" in body:
            lines.append(f'{sp}  <joint {dict_to_attr(body["joint"])}/>')

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

        if "site" in body:
            site = body["site"].copy()
            site.setdefault("size", "0.02")
            lines.append(f'{sp}  <site {dict_to_attr(site)}/>')

        for child in tree.get(body["name"], []):
            lines.extend(body_to_xml(child, indent + 2))

        lines.append(f"{sp}</body>")
        return lines

    xml = []
    xml.append(f'<mujoco model="{model_name}">')
    xml.append('  <option gravity="0 0 -9.81" timestep="0.002" solver="Newton" iterations="100"/>')
    xml.append('  <worldbody>')

    # Floor
    if floor:
        xml.append(f'    <geom {dict_to_attr(floor)}/>')

    # Bodies
    for root in tree.get("world", []):
        xml.extend(body_to_xml(root))

    xml.append('  </worldbody>')

    if constraints:
        xml.append('  <equality>')
        for c in constraints:
            xml.append(f'    <connect site1="{c["site1"]}" site2="{c["site2"]}"/>')
        xml.append('  </equality>')

    # if actuators:
    #     xml.append('  <actuator>')
    #     for a in actuators:
    #         actuator_type = a.get("type", "motor")
    #         a_copy = a.copy()
    #         a_copy.pop("type", None)
    #         xml.append(f'    <{actuator_type} {dict_to_attr(a_copy)}/>')
    #     xml.append('  </actuator>')

    xml.append('</mujoco>')

    return "\n".join(xml)

xml_text = molt_to_xml(
    bodies=bodies,
    constraints=constraints,
    floor=floor
)


with open("Result/XML.xml", "w") as f:
    f.write(xml_text)

print("XML.xml generated successfully.")