from graphviz import Digraph
import os

if __package__:
    from .output_paths import OUTPUT_DIR
else:
    from output_paths import OUTPUT_DIR

no_of_Component = 3

def createOneWayGraph():

    #print("Current working directory:", os.getcwd())

    g = Digraph("Resilience", format="png")
    # g.attr(label="Fig1: Resilience Transitions for CPS System", labelloc="b")
    g.attr(rankdir="LR", forcelabels="true")
    g.node_attr.update(shape="box", style="filled", fillcolor="#ffe0b5")

    # Firmware 1 (RADAR SYSTEM)
    g.node("FW1_Ant", label="FW1_ANT",  layer="FW", goal = "ANT", compId ="1", compType = "C2", direction = "1") 
    g.node("FW1_With", label="FW1_WITH",  layer="FW", goal = "WITH", compId ="1", compType = "C2", direction = "1")
    g.node("FW1_Rec", label="FW1_REC",  layer="FW", goal = "REC", compId ="1", compType = "C2", direction = "1")
    g.node("FW1_Adpt", label="FW1_ADPT",  layer="FW", goal = "ADPT", compId ="1", compType = "C2", direction = "1")


    # Application 1 (RADAR SYSTEM)
    g.node("APP1_Ant", label="APPL1_ANT",  layer="APPL", goal = "ANT", compId ="1", compType = "C2", direction = "1")
    g.node("APP1_With", label="APPL1_WITH",  layer="APPL", goal = "WITH", compId ="1", compType = "C2", direction = "1")

    # Network 1 (network radar)
    g.node("NETW1_Ant", label="NETW1_ANT",  layer="NETW", goal = "ANT", compId ="1", compType = "C2", direction = "1")
    g.node("NETW1_With", label="NETW1_WITH",  layer="NETW", goal = "WITH", compId ="1", compType = "C2", direction = "1")

    # Network 2 (network lan)
    g.node("NETW2_Ant", label="NETW2_ANT",  layer="NETW", goal = "ANT", compId ="2", compType = "LAN", direction = "1")
    g.node("NETW2_With", label="NETW2_WITH",  layer="NETW", goal = "WITH", compId ="2", compType = "LAN", direction = "1")

    # Network 3 (network AGGREGATION SYSTEM)
    g.node("NETW3_Ant", label="NETW3_ANT",  layer="NETW", goal = "ANT", compId ="3", compType = "C2", direction = "1")
    g.node("NETW3_With", label="NETW3_WITH",  layer="NETW", goal = "WITH", compId ="3", compType = "C2", direction = "1")

    # Firmware 3 (AGGREGATION SYSTEM)
    g.node("FW3_Ant", label="FW3_ANT",  layer="FW", goal = "ANT", compId ="3", compType = "C2", direction = "1")
    g.node("FW3_With", label="FW3_WITH",  layer="FW", goal = "WITH", compId ="3", compType = "C2", direction = "1")
    g.node("FW3_Rec", label="FW3_REC",  layer="FW", goal = "REC", compId ="3", compType = "C2", direction = "1")

    # Application 3 (RADAR SYSTEM)
    g.node("APP3_Ant", label="APPL3_ANT",  layer="APPL", goal = "ANT", compId ="3", compType = "C2", direction = "1")
    g.node("APP3_With", label="APPL3_WITH",  layer="APPL", goal = "WITH", compId ="3", compType = "C2", direction = "1")
    g.node("APP3_Rec", label="APPL3_REC",  layer="APPL", goal = "REC", compId ="3", compType = "C2", direction = "1")

    # radar side
    g.edge("FW1_Ant", "FW1_With", label="", type="OT-OT")
    g.edge("FW1_With", "FW1_Rec", label="", type="OT-OT")
    g.edge("FW1_Rec", "FW1_Adpt", label="", type="OT-OT")
    g.edge("FW1_With", "APP1_Ant", label="", type="OT-OT")
    g.edge("FW1_With", "APP1_With", label="", type="OT-OT")
    g.edge("FW1_With", "NETW1_Ant", label="", type="OT-OT")
    g.edge("NETW1_Ant", "NETW1_With", label="", type="OT-OT")
    g.edge("NETW1_With", "NETW2_Ant", label="", type="OT-OT")
    g.edge("NETW2_Ant", "NETW2_With", label="", type="OT-OT")
    g.edge("NETW2_With", "NETW3_Ant", label="", type="OT-OT")
    g.edge("NETW3_Ant", "NETW3_With", label="", type="OT-OT")
    g.edge("NETW3_With", "FW3_Ant", label="", type="OT-OT")
    g.edge("FW3_Ant", "FW3_With", label="", type="OT-OT")
    g.edge("FW3_With", "FW3_Rec", label="", type="OT-OT")
    g.edge("FW3_Rec", "APP3_Rec", label="", type="OT-OT")
    g.edge("FW3_With", "APP3_Ant", label="", type="OT-OT")
    g.edge("FW3_With", "APP3_With", label="")

    output_path = g.render(
        filename="CVE-2017-0144_one_way",
        directory=str(OUTPUT_DIR),
        cleanup=False,
        view=False
    )

    svg_path = g.render(
        filename="CVE-2017-0144_one_way",
        directory=str(OUTPUT_DIR),
        format="svg",
        cleanup=False,
        view=False
    )

    dot_path = g.save(filename=str(OUTPUT_DIR / "CVE-2017-0144_one_way.dot"))

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

    # Firmware 3 (AGGREGATION SERVER)
    g.node("FW3_Ant", label="FW3_ANT", layer="FW", goal = "ANT", compId ="3", compType = "C2", direction = "3")
    g.node("FW3_With", label="FW3_WITH", layer="FW", goal = "WITH", compId ="3", compType = "C2", direction = "3")
    g.node("FW3_Rec", label="FW3_REC", layer="FW", goal = "REC", compId ="3", compType = "C2", direction = "3")
    g.node("FW3_Adpt", label="FW3_ADPT", layer="FW", goal = "ADPT", compId ="3", compType = "C2", direction = "3")

    # Application 3 (AGGREGATION SERVER)
    g.node("APP3_Ant", label="APPL3_ANT", layer="APPL", goal = "ANT", compId ="3", compType = "C2", direction = "3")
    g.node("APP3_With", label="APPL3_WITH", layer="APPL", goal = "WITH", compId ="3", compType = "C2", direction = "3")

    # Network 3 (AGGREGATION SERVER)
    g.node("NETW3_Ant", label="NETW3_ANT", layer="NETW", goal = "ANT", compId ="3", compType = "C2", direction = "3")
    g.node("NETW3_With", label="NETW3_WITH", layer="NETW", goal = "WITH", compId ="3", compType = "C2", direction = "3")

    # Network 2 (network lan)
    g.node("NETW2_Ant", label="NETW2_ANT", layer="NETW", goal = "ANT", compId ="2", compType = "LAN", direction = "2")
    g.node("NETW2_With", label="NETW2_WITH", layer="NETW", goal = "WITH", compId ="2", compType = "LAN", direction = "2")

    # Network 1 (network RADAR SYSTEM)
    g.node("NETW1_Ant", label="NETW1_ANT", layer="NETW", goal = "ANT", compId ="1", compType = "C2", direction = "2")
    g.node("NETW1_With", label="NETW1_WITH", layer="NETW", goal = "WITH", compId ="1", compType = "C2", direction = "2")

    # Firmware 1 (RADAR SYSTEM)
    g.node("FW1_Ant", label="FW1_ANT", layer="FW", goal = "ANT", compId ="1", compType = "C2", direction = "2")
    g.node("FW1_With", label="FW1_WITH", layer="FW", goal = "WITH", compId ="1", compType = "C2", direction = "2")
    g.node("FW1_Rec", label="FW1_REC", layer="FW", goal = "REC", compId ="1", compType = "C2", direction = "2")

    # Application 1 (RADAR SYSTEM)
    g.node("APP1_Ant", label="APPL1_ANT", layer="APPL", goal = "ANT", compId ="1", compType = "C2", direction = "2")
    g.node("APP1_With", label="APPL1_WITH", layer="APPL", goal = "WITH", compId ="1", compType = "C2", direction = "2")
    g.node("APP1_Rec", label="APPL1_REC", layer="APPL", goal = "REC", compId ="1", compType = "C2", direction = "2")

    # radar side
    g.edge("FW3_Ant", "FW3_With", label="",type="OT-OT")
    g.edge("FW3_With", "FW3_Rec", label="", type="OT-OT")
    g.edge("FW3_Rec", "FW3_Adpt", label="", type="OT-OT")
    g.edge("FW3_With", "APP3_Ant", label="", type="OT-OT")
    g.edge("FW3_With", "APP3_With", label="", type="OT-OT")
    g.edge("FW3_With", "NETW3_Ant", label="", type="OT-OT")
    g.edge("NETW3_Ant", "NETW3_With", label="", type="OT-OT") 
    g.edge("NETW3_With", "NETW2_Ant", label="", type="OT-OT")
    g.edge("NETW2_Ant", "NETW2_With", label="", type="OT-OT")
    g.edge("NETW2_With", "NETW1_Ant", label="", type="OT-OT")
    g.edge("NETW1_Ant", "NETW1_With", label="", type="OT-OT")
    g.edge("NETW1_With", "FW1_Ant", label="", type="OT-OT")
    g.edge("FW1_Ant", "FW1_With", label="", type="OT-OT")
    g.edge("FW1_With", "FW1_Rec", label="", type="OT-OT")
    g.edge("FW1_Rec", "APP1_Rec", label="", type="OT-OT")
    g.edge("FW1_With", "APP1_Ant", label="", type="OT-OT")
    g.edge("FW1_With", "APP1_With", label="", type="OT-OT")

    output_path = g.render(
        filename="CVE-2017-0144_one_way_reverse",
        directory=str(OUTPUT_DIR),
        cleanup=False,
        view=False
    )

    svg_path = g.render(
        filename="CVE-2017-0144_one_way_reverse",
        directory=str(OUTPUT_DIR),
        format="svg",
        cleanup=False,
        view=False
    )

    dot_path = g.save(filename=str(OUTPUT_DIR / "CVE-2017-0144_one_way_reverse.dot"))

    #print("PNG created at:", os.path.abspath(output_path))
    #print("DOT created at:", os.path.abspath(dot_path))
    #print("SVG created at:", os.path.abspath(svg_path))

    return g, output_path, dot_path, svg_path