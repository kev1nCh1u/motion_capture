// sources.v

// Generated using ACDS version 21.1 842

`timescale 1 ps / 1 ps
module sources (
		input  wire [99:0] probe  // probes.probe
	);

	altsource_probe_top #(
		.sld_auto_instance_index ("YES"),
		.sld_instance_index      (0),
		.instance_id             ("SOPR"),
		.probe_width             (100),
		.source_width            (0),
		.enable_metastability    ("NO")
	) in_system_sources_probes_0 (
		.probe (probe)  // probes.probe
	);

endmodule
