from graphviz import Digraph
import os

if __package__:
    from .output_paths import OUTPUT_DIR
else:
    from output_paths import OUTPUT_DIR

no_of_Component = 3

# for CVE-2014-0160, the entry points are on the aggregation server (C1) or radar(C3) firmware  as entry point

# in the protected scenario the setup is partially protected by upgrading the Radar OS to 
# mitigate the fault injection from the Radar side (radar entry point)
# However the entry point on the Command and control  side is not protected, allowing a fault injection point on the system 
def createOneWayGraph():
    # print("Current working directory:", os.getcwd())

    g = Digraph("Resilience", format="png")
    # g.attr(label="Fig1: Resilience Transitions for CPS System", labelloc="b")
    g.attr(rankdir="LR", forcelabels="true")
    g.node_attr.update(shape="box", style="filled", fillcolor="#ffe0b5")

    # Firmware 1 (client)
    g.node("FW1_Ant", label="FW1_ANT", layer="FW", goal = "ANT", compId ="1", compType = "C2", direction = "1") 
    g.node("FW1_With", label="FW1_WITH", layer="FW", goal = "WITH", compId ="1", compType = "C2", direction = "1")
    g.node("FW1_Rec", label="FW1_REC", layer="FW", goal = "REC", compId ="1", compType = "C2", direction = "1")
    g.node("FW1_Adpt", label="FW1_ADPT", layer="FW", goal = "ADPT", compId ="1", compType = "C2", direction = "1")

    # Application 1 (client app)
    g.node("APP1_Ant", label="APPL1_ANT", layer="APPL", goal = "ANT", compId ="1", compType = "C2", direction = "1")
    g.node("APP1_With", label="APPL1_WITH", layer="APPL", goal = "WITH", compId ="1", compType = "C2", direction = "1")
    g.node("APP1_Rec", label="APPL1_REC", layer="APPL", goal = "REC", compId ="1", compType = "C2", direction = "1")
    g.node("APP1_Adpt", label="APPL1_ADPT", layer="APPL", goal = "ADPT", compId ="1", compType = "C2", direction = "1")    

    # Client side (FW1, APP1): edges
    g.edge("FW1_Ant", "FW1_With", label="", type="OT-OT", link = "state")
    g.edge("FW1_With", "FW1_Rec", label="", type="OT-OT", link = "state")
    g.edge("FW1_With", "APP1_Ant", label="", type="OT-OT", link = "state")
    g.edge("FW1_Rec", "FW1_Adpt", label="", type="OT-OT", link = "state")
    g.edge("FW1_Rec", "APP1_Rec", label="", type="OT-OT", link = "data")
    g.edge("FW1_Adpt", "APP1_Adpt", label="",   type="OT-OT", link = "data")
    g.edge("APP1_Ant", "APP1_With", label="", type="OT-OT", link = "state")

    output_path = g.render(
        filename="CVE-2014-0160_one_way_protected",
        directory=str(OUTPUT_DIR),
        cleanup=False,
        view=False
    )

    svg_path = g.render(
        filename="CVE-2014-0160_one_way_protected",
        directory=str(OUTPUT_DIR),
        format="svg",
        cleanup=False,
        view=False
    )

    dot_path = g.save(filename=str(OUTPUT_DIR / "CVE-2014-0160_one_way_protected.dot"))

    #print("PNG created at:", os.path.abspath(output_path))
    #print("DOT created at:", os.path.abspath(dot_path))
    #print("SVG created at:", os.path.abspath(svg_path))

    return g, output_path, dot_path, svg_path

def createOneWayReverseGraph():

    #print("Current working directory:", os.getcwd())
    # models a cyber attack with entry point on 
    # aggregation server (C3) firmware as entry point 

    g = Digraph("Resilience", format="png")
    # g.attr(label="Fig1: Resilience Transitions for CPS System", labelloc="b")
    g.attr(rankdir="LR", forcelabels="true")
    g.node_attr.update(shape="box", style="filled", fillcolor="#ffe0b5")

    # Firmware 1 (client)
    g.node("FW3_Ant", label="FW3_ANT", layer="FW", goal = "ANT", compId ="3", compType = "C2", direction = "2") 
    g.node("FW3_With", label="FW3_WITH", layer="FW", goal = "WITH", compId ="3", compType = "C2", direction = "2")
#    g.node("FW3_Rec", label="FW3_REC", layer="FW", goal = "REC", compId ="3", compType = "C2", direction = "2")
#    g.node("FW3_Adpt", label="FW3_ADPT", layer="FW", goal = "ADPT", compId ="3", compType = "C2", direction = "2")

    # Application 1 (client app)
#    g.node("APP3_Ant", label="APPL3_ANT", layer="APPL", goal = "ANT", compId ="3", compType = "C2", direction = "2")
#    g.node("APP3_With", label="APPL3_WITH", layer="APPL", goal = "WITH", compId ="3", compType = "C2", direction = "2")
#    g.node("APP3_Rec", label="APPL3_REC", layer="APPL", goal = "REC", compId ="3", compType = "C2", direction = "2")
#    g.node("APP3_Adpt", label="APPL3_ADPT", layer="APPL", goal = "ADPT", compId ="3", compType = "C2", direction = "2")    

    g.edge("FW3_Ant", "FW3_With", label="", type="OT-OT", link = "state")
 
#there is no penetration point from the sensor/radar side since its FW has been upgraded
    # Client side (FW3, APP3)
#    g.edge("FW3_Ant", "FW3_With", label="", type="OT-OT")
#    g.edge("FW3_With", "FW3_Rec", label="", type="OT-OT")
#    g.edge("FW3_With", "APP3_Ant", label="", type="OT-OT")
#    g.edge("FW3_Rec", "FW3_Adpt", label="", type="OT-OT")
#    g.edge("FW3_Rec", "APP3_Rec", label="", type="OT-OT")
#    g.edge("FW3_Adpt", "APP3_Adpt", label="",   type="OT-OT")
#    g.edge("APP3_Ant", "APP3_With", label="", type="OT-OT")

    output_path = g.render(
        filename="CVE-2014-0160_one_way_reverse_protected",
        directory=str(OUTPUT_DIR),
        cleanup=False,
        view=False
    )

    svg_path = g.render(
        filename="CVE-2014-0160_one_way_reverse_protected",
        directory=str(OUTPUT_DIR),
        format="svg",
        cleanup=False,
        view=False
    )

    dot_path = g.save(filename=str(OUTPUT_DIR / "CVE-2014-0160_one_way_reverse_protected.dot"))

    #print("PNG created at:", os.path.abspath(output_path))
    #print("DOT created at:", os.path.abspath(dot_path))
    #print("SVG created at:", os.path.abspath(svg_path))

    return g, output_path, dot_path, svg_path
