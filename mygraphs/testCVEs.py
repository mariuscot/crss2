import CVE_2014_0160_radar_entry_one_way
import mygraphs.old.CVE_2014_0160_radar_entry_one_way_reverse as CVE_2014_0160_radar_entry_one_way_reverse
import CVE_2017_0144_radar_entry_one_way
import mygraphs.old.CVE_2017_0144_radar_entry_one_way_reverse as CVE_2017_0144_radar_entry_one_way_reverse


def testCVEs():
    # Test the CVE-2014-0160 radar entry one-way reverse graph generation
    g, output_path, dot_path, svg_path = CVE_2014_0160_radar_entry_one_way.createOneWayGraph()
    g, output_path, dot_path, svg_path = CVE_2014_0160_radar_entry_one_way_reverse.createOneWayReverseGraph()
    g, output_path, dot_path, svg_path = CVE_2017_0144_radar_entry_one_way.createOneWayGraph()
    g, output_path, dot_path, svg_path = CVE_2017_0144_radar_entry_one_way_reverse.createOneWayReverseGraph()



def main():
    testCVEs()

if __name__ == "__main__":
    main()