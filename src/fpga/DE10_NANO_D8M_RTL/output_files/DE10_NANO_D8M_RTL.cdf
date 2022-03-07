/* Quartus Prime Version 20.1.1 Build 720 11/11/2020 SJ Standard Edition */
JedecChain;
	FileRevision(JESD32A);
	DefaultMfr(6E);

	P ActionCode(Ign)
		Device PartName(SOCVHPS) MfrSpec(OpMask(0));
	P ActionCode(Cfg)
		Device PartName(5CSEBA6U23) Path("/home/kevin/src/motion_capture/src/fpga/D8M/DE10_NANO_D8M_RTL/output_files/") File("DE10_NANO_D8M_RTL.sof") MfrSpec(OpMask(1));

ChainEnd;

AlteraBegin;
	ChainType(JTAG);
AlteraEnd;
