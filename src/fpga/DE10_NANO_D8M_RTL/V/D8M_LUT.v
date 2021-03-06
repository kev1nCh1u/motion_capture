module D8M_LUT(
	input			enable,
	input			PIXEL_CLK,
	input			MIPI_PIXEL_HS,
	input			MIPI_PIXEL_VS,
	input	[9:0]		MIPI_PIXEL_D,
	output	reg		NEW_MIPI_PIXEL_HS,
	output	reg		NEW_MIPI_PIXEL_VS,
	output	reg	[9:0]	NEW_MIPI_PIXEL_D
);

reg		Pipe_HS;
reg		Pipe_VS;
reg	[9:0]	Pipe_Data;

always@(posedge PIXEL_CLK)
begin
	Pipe_HS <= MIPI_PIXEL_HS;
	Pipe_VS <= MIPI_PIXEL_VS;
	Pipe_Data <= MIPI_PIXEL_D;
end

always@(posedge PIXEL_CLK)
begin
	NEW_MIPI_PIXEL_HS <= Pipe_HS;
	NEW_MIPI_PIXEL_VS <= Pipe_VS;
	NEW_MIPI_PIXEL_D <= enable?LUT[Pipe_Data]:Pipe_Data;
end

//Loopup Table
//Highlight=1023
//Shadow=280
//Gamma=1.000000

wire [9:0] LUT[1023:0];

assign LUT[0]=0;
assign LUT[1]=0;
assign LUT[2]=0;
assign LUT[3]=0;
assign LUT[4]=0;
assign LUT[5]=0;
assign LUT[6]=0;
assign LUT[7]=0;
assign LUT[8]=0;
assign LUT[9]=0;
assign LUT[10]=0;
assign LUT[11]=0;
assign LUT[12]=0;
assign LUT[13]=0;
assign LUT[14]=0;
assign LUT[15]=0;
assign LUT[16]=0;
assign LUT[17]=0;
assign LUT[18]=0;
assign LUT[19]=0;
assign LUT[20]=0;
assign LUT[21]=0;
assign LUT[22]=0;
assign LUT[23]=0;
assign LUT[24]=0;
assign LUT[25]=0;
assign LUT[26]=0;
assign LUT[27]=0;
assign LUT[28]=0;
assign LUT[29]=0;
assign LUT[30]=0;
assign LUT[31]=0;
assign LUT[32]=0;
assign LUT[33]=0;
assign LUT[34]=0;
assign LUT[35]=0;
assign LUT[36]=0;
assign LUT[37]=0;
assign LUT[38]=0;
assign LUT[39]=0;
assign LUT[40]=0;
assign LUT[41]=0;
assign LUT[42]=0;
assign LUT[43]=0;
assign LUT[44]=0;
assign LUT[45]=0;
assign LUT[46]=0;
assign LUT[47]=0;
assign LUT[48]=0;
assign LUT[49]=0;
assign LUT[50]=0;
assign LUT[51]=0;
assign LUT[52]=0;
assign LUT[53]=0;
assign LUT[54]=0;
assign LUT[55]=0;
assign LUT[56]=0;
assign LUT[57]=0;
assign LUT[58]=0;
assign LUT[59]=0;
assign LUT[60]=0;
assign LUT[61]=0;
assign LUT[62]=0;
assign LUT[63]=0;
assign LUT[64]=0;
assign LUT[65]=0;
assign LUT[66]=0;
assign LUT[67]=0;
assign LUT[68]=0;
assign LUT[69]=0;
assign LUT[70]=0;
assign LUT[71]=0;
assign LUT[72]=0;
assign LUT[73]=0;
assign LUT[74]=0;
assign LUT[75]=0;
assign LUT[76]=0;
assign LUT[77]=0;
assign LUT[78]=0;
assign LUT[79]=0;
assign LUT[80]=0;
assign LUT[81]=0;
assign LUT[82]=0;
assign LUT[83]=0;
assign LUT[84]=0;
assign LUT[85]=0;
assign LUT[86]=0;
assign LUT[87]=0;
assign LUT[88]=0;
assign LUT[89]=0;
assign LUT[90]=0;
assign LUT[91]=0;
assign LUT[92]=0;
assign LUT[93]=0;
assign LUT[94]=0;
assign LUT[95]=0;
assign LUT[96]=0;
assign LUT[97]=0;
assign LUT[98]=0;
assign LUT[99]=0;
assign LUT[100]=0;
assign LUT[101]=0;
assign LUT[102]=0;
assign LUT[103]=0;
assign LUT[104]=0;
assign LUT[105]=0;
assign LUT[106]=0;
assign LUT[107]=0;
assign LUT[108]=0;
assign LUT[109]=0;
assign LUT[110]=0;
assign LUT[111]=0;
assign LUT[112]=0;
assign LUT[113]=0;
assign LUT[114]=0;
assign LUT[115]=0;
assign LUT[116]=0;
assign LUT[117]=0;
assign LUT[118]=0;
assign LUT[119]=0;
assign LUT[120]=0;
assign LUT[121]=0;
assign LUT[122]=0;
assign LUT[123]=0;
assign LUT[124]=0;
assign LUT[125]=0;
assign LUT[126]=0;
assign LUT[127]=0;
assign LUT[128]=0;
assign LUT[129]=0;
assign LUT[130]=0;
assign LUT[131]=0;
assign LUT[132]=0;
assign LUT[133]=0;
assign LUT[134]=0;
assign LUT[135]=0;
assign LUT[136]=0;
assign LUT[137]=0;
assign LUT[138]=0;
assign LUT[139]=0;
assign LUT[140]=0;
assign LUT[141]=0;
assign LUT[142]=0;
assign LUT[143]=0;
assign LUT[144]=0;
assign LUT[145]=0;
assign LUT[146]=0;
assign LUT[147]=0;
assign LUT[148]=0;
assign LUT[149]=0;
assign LUT[150]=0;
assign LUT[151]=0;
assign LUT[152]=0;
assign LUT[153]=0;
assign LUT[154]=0;
assign LUT[155]=0;
assign LUT[156]=0;
assign LUT[157]=0;
assign LUT[158]=0;
assign LUT[159]=0;
assign LUT[160]=0;
assign LUT[161]=0;
assign LUT[162]=0;
assign LUT[163]=0;
assign LUT[164]=0;
assign LUT[165]=0;
assign LUT[166]=0;
assign LUT[167]=0;
assign LUT[168]=0;
assign LUT[169]=0;
assign LUT[170]=0;
assign LUT[171]=0;
assign LUT[172]=0;
assign LUT[173]=0;
assign LUT[174]=0;
assign LUT[175]=0;
assign LUT[176]=0;
assign LUT[177]=0;
assign LUT[178]=0;
assign LUT[179]=0;
assign LUT[180]=0;
assign LUT[181]=0;
assign LUT[182]=0;
assign LUT[183]=0;
assign LUT[184]=0;
assign LUT[185]=0;
assign LUT[186]=0;
assign LUT[187]=0;
assign LUT[188]=0;
assign LUT[189]=0;
assign LUT[190]=0;
assign LUT[191]=0;
assign LUT[192]=0;
assign LUT[193]=0;
assign LUT[194]=0;
assign LUT[195]=0;
assign LUT[196]=0;
assign LUT[197]=0;
assign LUT[198]=0;
assign LUT[199]=0;
assign LUT[200]=0;
assign LUT[201]=0;
assign LUT[202]=0;
assign LUT[203]=0;
assign LUT[204]=0;
assign LUT[205]=0;
assign LUT[206]=0;
assign LUT[207]=0;
assign LUT[208]=0;
assign LUT[209]=0;
assign LUT[210]=0;
assign LUT[211]=0;
assign LUT[212]=0;
assign LUT[213]=0;
assign LUT[214]=0;
assign LUT[215]=0;
assign LUT[216]=0;
assign LUT[217]=0;
assign LUT[218]=0;
assign LUT[219]=0;
assign LUT[220]=0;
assign LUT[221]=0;
assign LUT[222]=0;
assign LUT[223]=0;
assign LUT[224]=0;
assign LUT[225]=0;
assign LUT[226]=0;
assign LUT[227]=0;
assign LUT[228]=0;
assign LUT[229]=0;
assign LUT[230]=0;
assign LUT[231]=0;
assign LUT[232]=0;
assign LUT[233]=0;
assign LUT[234]=0;
assign LUT[235]=0;
assign LUT[236]=0;
assign LUT[237]=0;
assign LUT[238]=0;
assign LUT[239]=0;
assign LUT[240]=0;
assign LUT[241]=0;
assign LUT[242]=0;
assign LUT[243]=0;
assign LUT[244]=0;
assign LUT[245]=0;
assign LUT[246]=0;
assign LUT[247]=0;
assign LUT[248]=0;
assign LUT[249]=0;
assign LUT[250]=0;
assign LUT[251]=0;
assign LUT[252]=0;
assign LUT[253]=0;
assign LUT[254]=0;
assign LUT[255]=0;
assign LUT[256]=0;
assign LUT[257]=0;
assign LUT[258]=0;
assign LUT[259]=0;
assign LUT[260]=0;
assign LUT[261]=0;
assign LUT[262]=0;
assign LUT[263]=0;
assign LUT[264]=0;
assign LUT[265]=0;
assign LUT[266]=0;
assign LUT[267]=0;
assign LUT[268]=0;
assign LUT[269]=0;
assign LUT[270]=0;
assign LUT[271]=0;
assign LUT[272]=0;
assign LUT[273]=0;
assign LUT[274]=0;
assign LUT[275]=0;
assign LUT[276]=0;
assign LUT[277]=0;
assign LUT[278]=0;
assign LUT[279]=0;
assign LUT[280]=0;
assign LUT[281]=1;
assign LUT[282]=2;
assign LUT[283]=4;
assign LUT[284]=5;
assign LUT[285]=6;
assign LUT[286]=8;
assign LUT[287]=9;
assign LUT[288]=11;
assign LUT[289]=12;
assign LUT[290]=13;
assign LUT[291]=15;
assign LUT[292]=16;
assign LUT[293]=17;
assign LUT[294]=19;
assign LUT[295]=20;
assign LUT[296]=22;
assign LUT[297]=23;
assign LUT[298]=24;
assign LUT[299]=26;
assign LUT[300]=27;
assign LUT[301]=28;
assign LUT[302]=30;
assign LUT[303]=31;
assign LUT[304]=33;
assign LUT[305]=34;
assign LUT[306]=35;
assign LUT[307]=37;
assign LUT[308]=38;
assign LUT[309]=39;
assign LUT[310]=41;
assign LUT[311]=42;
assign LUT[312]=44;
assign LUT[313]=45;
assign LUT[314]=46;
assign LUT[315]=48;
assign LUT[316]=49;
assign LUT[317]=50;
assign LUT[318]=52;
assign LUT[319]=53;
assign LUT[320]=55;
assign LUT[321]=56;
assign LUT[322]=57;
assign LUT[323]=59;
assign LUT[324]=60;
assign LUT[325]=61;
assign LUT[326]=63;
assign LUT[327]=64;
assign LUT[328]=66;
assign LUT[329]=67;
assign LUT[330]=68;
assign LUT[331]=70;
assign LUT[332]=71;
assign LUT[333]=72;
assign LUT[334]=74;
assign LUT[335]=75;
assign LUT[336]=77;
assign LUT[337]=78;
assign LUT[338]=79;
assign LUT[339]=81;
assign LUT[340]=82;
assign LUT[341]=83;
assign LUT[342]=85;
assign LUT[343]=86;
assign LUT[344]=88;
assign LUT[345]=89;
assign LUT[346]=90;
assign LUT[347]=92;
assign LUT[348]=93;
assign LUT[349]=95;
assign LUT[350]=96;
assign LUT[351]=97;
assign LUT[352]=99;
assign LUT[353]=100;
assign LUT[354]=101;
assign LUT[355]=103;
assign LUT[356]=104;
assign LUT[357]=106;
assign LUT[358]=107;
assign LUT[359]=108;
assign LUT[360]=110;
assign LUT[361]=111;
assign LUT[362]=112;
assign LUT[363]=114;
assign LUT[364]=115;
assign LUT[365]=117;
assign LUT[366]=118;
assign LUT[367]=119;
assign LUT[368]=121;
assign LUT[369]=122;
assign LUT[370]=123;
assign LUT[371]=125;
assign LUT[372]=126;
assign LUT[373]=128;
assign LUT[374]=129;
assign LUT[375]=130;
assign LUT[376]=132;
assign LUT[377]=133;
assign LUT[378]=134;
assign LUT[379]=136;
assign LUT[380]=137;
assign LUT[381]=139;
assign LUT[382]=140;
assign LUT[383]=141;
assign LUT[384]=143;
assign LUT[385]=144;
assign LUT[386]=145;
assign LUT[387]=147;
assign LUT[388]=148;
assign LUT[389]=150;
assign LUT[390]=151;
assign LUT[391]=152;
assign LUT[392]=154;
assign LUT[393]=155;
assign LUT[394]=156;
assign LUT[395]=158;
assign LUT[396]=159;
assign LUT[397]=161;
assign LUT[398]=162;
assign LUT[399]=163;
assign LUT[400]=165;
assign LUT[401]=166;
assign LUT[402]=167;
assign LUT[403]=169;
assign LUT[404]=170;
assign LUT[405]=172;
assign LUT[406]=173;
assign LUT[407]=174;
assign LUT[408]=176;
assign LUT[409]=177;
assign LUT[410]=178;
assign LUT[411]=180;
assign LUT[412]=181;
assign LUT[413]=183;
assign LUT[414]=184;
assign LUT[415]=185;
assign LUT[416]=187;
assign LUT[417]=188;
assign LUT[418]=190;
assign LUT[419]=191;
assign LUT[420]=192;
assign LUT[421]=194;
assign LUT[422]=195;
assign LUT[423]=196;
assign LUT[424]=198;
assign LUT[425]=199;
assign LUT[426]=201;
assign LUT[427]=202;
assign LUT[428]=203;
assign LUT[429]=205;
assign LUT[430]=206;
assign LUT[431]=207;
assign LUT[432]=209;
assign LUT[433]=210;
assign LUT[434]=212;
assign LUT[435]=213;
assign LUT[436]=214;
assign LUT[437]=216;
assign LUT[438]=217;
assign LUT[439]=218;
assign LUT[440]=220;
assign LUT[441]=221;
assign LUT[442]=223;
assign LUT[443]=224;
assign LUT[444]=225;
assign LUT[445]=227;
assign LUT[446]=228;
assign LUT[447]=229;
assign LUT[448]=231;
assign LUT[449]=232;
assign LUT[450]=234;
assign LUT[451]=235;
assign LUT[452]=236;
assign LUT[453]=238;
assign LUT[454]=239;
assign LUT[455]=240;
assign LUT[456]=242;
assign LUT[457]=243;
assign LUT[458]=245;
assign LUT[459]=246;
assign LUT[460]=247;
assign LUT[461]=249;
assign LUT[462]=250;
assign LUT[463]=251;
assign LUT[464]=253;
assign LUT[465]=254;
assign LUT[466]=256;
assign LUT[467]=257;
assign LUT[468]=258;
assign LUT[469]=260;
assign LUT[470]=261;
assign LUT[471]=262;
assign LUT[472]=264;
assign LUT[473]=265;
assign LUT[474]=267;
assign LUT[475]=268;
assign LUT[476]=269;
assign LUT[477]=271;
assign LUT[478]=272;
assign LUT[479]=273;
assign LUT[480]=275;
assign LUT[481]=276;
assign LUT[482]=278;
assign LUT[483]=279;
assign LUT[484]=280;
assign LUT[485]=282;
assign LUT[486]=283;
assign LUT[487]=285;
assign LUT[488]=286;
assign LUT[489]=287;
assign LUT[490]=289;
assign LUT[491]=290;
assign LUT[492]=291;
assign LUT[493]=293;
assign LUT[494]=294;
assign LUT[495]=296;
assign LUT[496]=297;
assign LUT[497]=298;
assign LUT[498]=300;
assign LUT[499]=301;
assign LUT[500]=302;
assign LUT[501]=304;
assign LUT[502]=305;
assign LUT[503]=307;
assign LUT[504]=308;
assign LUT[505]=309;
assign LUT[506]=311;
assign LUT[507]=312;
assign LUT[508]=313;
assign LUT[509]=315;
assign LUT[510]=316;
assign LUT[511]=318;
assign LUT[512]=319;
assign LUT[513]=320;
assign LUT[514]=322;
assign LUT[515]=323;
assign LUT[516]=324;
assign LUT[517]=326;
assign LUT[518]=327;
assign LUT[519]=329;
assign LUT[520]=330;
assign LUT[521]=331;
assign LUT[522]=333;
assign LUT[523]=334;
assign LUT[524]=335;
assign LUT[525]=337;
assign LUT[526]=338;
assign LUT[527]=340;
assign LUT[528]=341;
assign LUT[529]=342;
assign LUT[530]=344;
assign LUT[531]=345;
assign LUT[532]=346;
assign LUT[533]=348;
assign LUT[534]=349;
assign LUT[535]=351;
assign LUT[536]=352;
assign LUT[537]=353;
assign LUT[538]=355;
assign LUT[539]=356;
assign LUT[540]=357;
assign LUT[541]=359;
assign LUT[542]=360;
assign LUT[543]=362;
assign LUT[544]=363;
assign LUT[545]=364;
assign LUT[546]=366;
assign LUT[547]=367;
assign LUT[548]=368;
assign LUT[549]=370;
assign LUT[550]=371;
assign LUT[551]=373;
assign LUT[552]=374;
assign LUT[553]=375;
assign LUT[554]=377;
assign LUT[555]=378;
assign LUT[556]=380;
assign LUT[557]=381;
assign LUT[558]=382;
assign LUT[559]=384;
assign LUT[560]=385;
assign LUT[561]=386;
assign LUT[562]=388;
assign LUT[563]=389;
assign LUT[564]=391;
assign LUT[565]=392;
assign LUT[566]=393;
assign LUT[567]=395;
assign LUT[568]=396;
assign LUT[569]=397;
assign LUT[570]=399;
assign LUT[571]=400;
assign LUT[572]=402;
assign LUT[573]=403;
assign LUT[574]=404;
assign LUT[575]=406;
assign LUT[576]=407;
assign LUT[577]=408;
assign LUT[578]=410;
assign LUT[579]=411;
assign LUT[580]=413;
assign LUT[581]=414;
assign LUT[582]=415;
assign LUT[583]=417;
assign LUT[584]=418;
assign LUT[585]=419;
assign LUT[586]=421;
assign LUT[587]=422;
assign LUT[588]=424;
assign LUT[589]=425;
assign LUT[590]=426;
assign LUT[591]=428;
assign LUT[592]=429;
assign LUT[593]=430;
assign LUT[594]=432;
assign LUT[595]=433;
assign LUT[596]=435;
assign LUT[597]=436;
assign LUT[598]=437;
assign LUT[599]=439;
assign LUT[600]=440;
assign LUT[601]=441;
assign LUT[602]=443;
assign LUT[603]=444;
assign LUT[604]=446;
assign LUT[605]=447;
assign LUT[606]=448;
assign LUT[607]=450;
assign LUT[608]=451;
assign LUT[609]=452;
assign LUT[610]=454;
assign LUT[611]=455;
assign LUT[612]=457;
assign LUT[613]=458;
assign LUT[614]=459;
assign LUT[615]=461;
assign LUT[616]=462;
assign LUT[617]=463;
assign LUT[618]=465;
assign LUT[619]=466;
assign LUT[620]=468;
assign LUT[621]=469;
assign LUT[622]=470;
assign LUT[623]=472;
assign LUT[624]=473;
assign LUT[625]=475;
assign LUT[626]=476;
assign LUT[627]=477;
assign LUT[628]=479;
assign LUT[629]=480;
assign LUT[630]=481;
assign LUT[631]=483;
assign LUT[632]=484;
assign LUT[633]=486;
assign LUT[634]=487;
assign LUT[635]=488;
assign LUT[636]=490;
assign LUT[637]=491;
assign LUT[638]=492;
assign LUT[639]=494;
assign LUT[640]=495;
assign LUT[641]=497;
assign LUT[642]=498;
assign LUT[643]=499;
assign LUT[644]=501;
assign LUT[645]=502;
assign LUT[646]=503;
assign LUT[647]=505;
assign LUT[648]=506;
assign LUT[649]=508;
assign LUT[650]=509;
assign LUT[651]=510;
assign LUT[652]=512;
assign LUT[653]=513;
assign LUT[654]=514;
assign LUT[655]=516;
assign LUT[656]=517;
assign LUT[657]=519;
assign LUT[658]=520;
assign LUT[659]=521;
assign LUT[660]=523;
assign LUT[661]=524;
assign LUT[662]=525;
assign LUT[663]=527;
assign LUT[664]=528;
assign LUT[665]=530;
assign LUT[666]=531;
assign LUT[667]=532;
assign LUT[668]=534;
assign LUT[669]=535;
assign LUT[670]=536;
assign LUT[671]=538;
assign LUT[672]=539;
assign LUT[673]=541;
assign LUT[674]=542;
assign LUT[675]=543;
assign LUT[676]=545;
assign LUT[677]=546;
assign LUT[678]=547;
assign LUT[679]=549;
assign LUT[680]=550;
assign LUT[681]=552;
assign LUT[682]=553;
assign LUT[683]=554;
assign LUT[684]=556;
assign LUT[685]=557;
assign LUT[686]=559;
assign LUT[687]=560;
assign LUT[688]=561;
assign LUT[689]=563;
assign LUT[690]=564;
assign LUT[691]=565;
assign LUT[692]=567;
assign LUT[693]=568;
assign LUT[694]=570;
assign LUT[695]=571;
assign LUT[696]=572;
assign LUT[697]=574;
assign LUT[698]=575;
assign LUT[699]=576;
assign LUT[700]=578;
assign LUT[701]=579;
assign LUT[702]=581;
assign LUT[703]=582;
assign LUT[704]=583;
assign LUT[705]=585;
assign LUT[706]=586;
assign LUT[707]=587;
assign LUT[708]=589;
assign LUT[709]=590;
assign LUT[710]=592;
assign LUT[711]=593;
assign LUT[712]=594;
assign LUT[713]=596;
assign LUT[714]=597;
assign LUT[715]=598;
assign LUT[716]=600;
assign LUT[717]=601;
assign LUT[718]=603;
assign LUT[719]=604;
assign LUT[720]=605;
assign LUT[721]=607;
assign LUT[722]=608;
assign LUT[723]=609;
assign LUT[724]=611;
assign LUT[725]=612;
assign LUT[726]=614;
assign LUT[727]=615;
assign LUT[728]=616;
assign LUT[729]=618;
assign LUT[730]=619;
assign LUT[731]=620;
assign LUT[732]=622;
assign LUT[733]=623;
assign LUT[734]=625;
assign LUT[735]=626;
assign LUT[736]=627;
assign LUT[737]=629;
assign LUT[738]=630;
assign LUT[739]=631;
assign LUT[740]=633;
assign LUT[741]=634;
assign LUT[742]=636;
assign LUT[743]=637;
assign LUT[744]=638;
assign LUT[745]=640;
assign LUT[746]=641;
assign LUT[747]=642;
assign LUT[748]=644;
assign LUT[749]=645;
assign LUT[750]=647;
assign LUT[751]=648;
assign LUT[752]=649;
assign LUT[753]=651;
assign LUT[754]=652;
assign LUT[755]=654;
assign LUT[756]=655;
assign LUT[757]=656;
assign LUT[758]=658;
assign LUT[759]=659;
assign LUT[760]=660;
assign LUT[761]=662;
assign LUT[762]=663;
assign LUT[763]=665;
assign LUT[764]=666;
assign LUT[765]=667;
assign LUT[766]=669;
assign LUT[767]=670;
assign LUT[768]=671;
assign LUT[769]=673;
assign LUT[770]=674;
assign LUT[771]=676;
assign LUT[772]=677;
assign LUT[773]=678;
assign LUT[774]=680;
assign LUT[775]=681;
assign LUT[776]=682;
assign LUT[777]=684;
assign LUT[778]=685;
assign LUT[779]=687;
assign LUT[780]=688;
assign LUT[781]=689;
assign LUT[782]=691;
assign LUT[783]=692;
assign LUT[784]=693;
assign LUT[785]=695;
assign LUT[786]=696;
assign LUT[787]=698;
assign LUT[788]=699;
assign LUT[789]=700;
assign LUT[790]=702;
assign LUT[791]=703;
assign LUT[792]=704;
assign LUT[793]=706;
assign LUT[794]=707;
assign LUT[795]=709;
assign LUT[796]=710;
assign LUT[797]=711;
assign LUT[798]=713;
assign LUT[799]=714;
assign LUT[800]=715;
assign LUT[801]=717;
assign LUT[802]=718;
assign LUT[803]=720;
assign LUT[804]=721;
assign LUT[805]=722;
assign LUT[806]=724;
assign LUT[807]=725;
assign LUT[808]=726;
assign LUT[809]=728;
assign LUT[810]=729;
assign LUT[811]=731;
assign LUT[812]=732;
assign LUT[813]=733;
assign LUT[814]=735;
assign LUT[815]=736;
assign LUT[816]=737;
assign LUT[817]=739;
assign LUT[818]=740;
assign LUT[819]=742;
assign LUT[820]=743;
assign LUT[821]=744;
assign LUT[822]=746;
assign LUT[823]=747;
assign LUT[824]=749;
assign LUT[825]=750;
assign LUT[826]=751;
assign LUT[827]=753;
assign LUT[828]=754;
assign LUT[829]=755;
assign LUT[830]=757;
assign LUT[831]=758;
assign LUT[832]=760;
assign LUT[833]=761;
assign LUT[834]=762;
assign LUT[835]=764;
assign LUT[836]=765;
assign LUT[837]=766;
assign LUT[838]=768;
assign LUT[839]=769;
assign LUT[840]=771;
assign LUT[841]=772;
assign LUT[842]=773;
assign LUT[843]=775;
assign LUT[844]=776;
assign LUT[845]=777;
assign LUT[846]=779;
assign LUT[847]=780;
assign LUT[848]=782;
assign LUT[849]=783;
assign LUT[850]=784;
assign LUT[851]=786;
assign LUT[852]=787;
assign LUT[853]=788;
assign LUT[854]=790;
assign LUT[855]=791;
assign LUT[856]=793;
assign LUT[857]=794;
assign LUT[858]=795;
assign LUT[859]=797;
assign LUT[860]=798;
assign LUT[861]=799;
assign LUT[862]=801;
assign LUT[863]=802;
assign LUT[864]=804;
assign LUT[865]=805;
assign LUT[866]=806;
assign LUT[867]=808;
assign LUT[868]=809;
assign LUT[869]=810;
assign LUT[870]=812;
assign LUT[871]=813;
assign LUT[872]=815;
assign LUT[873]=816;
assign LUT[874]=817;
assign LUT[875]=819;
assign LUT[876]=820;
assign LUT[877]=821;
assign LUT[878]=823;
assign LUT[879]=824;
assign LUT[880]=826;
assign LUT[881]=827;
assign LUT[882]=828;
assign LUT[883]=830;
assign LUT[884]=831;
assign LUT[885]=832;
assign LUT[886]=834;
assign LUT[887]=835;
assign LUT[888]=837;
assign LUT[889]=838;
assign LUT[890]=839;
assign LUT[891]=841;
assign LUT[892]=842;
assign LUT[893]=844;
assign LUT[894]=845;
assign LUT[895]=846;
assign LUT[896]=848;
assign LUT[897]=849;
assign LUT[898]=850;
assign LUT[899]=852;
assign LUT[900]=853;
assign LUT[901]=855;
assign LUT[902]=856;
assign LUT[903]=857;
assign LUT[904]=859;
assign LUT[905]=860;
assign LUT[906]=861;
assign LUT[907]=863;
assign LUT[908]=864;
assign LUT[909]=866;
assign LUT[910]=867;
assign LUT[911]=868;
assign LUT[912]=870;
assign LUT[913]=871;
assign LUT[914]=872;
assign LUT[915]=874;
assign LUT[916]=875;
assign LUT[917]=877;
assign LUT[918]=878;
assign LUT[919]=879;
assign LUT[920]=881;
assign LUT[921]=882;
assign LUT[922]=883;
assign LUT[923]=885;
assign LUT[924]=886;
assign LUT[925]=888;
assign LUT[926]=889;
assign LUT[927]=890;
assign LUT[928]=892;
assign LUT[929]=893;
assign LUT[930]=894;
assign LUT[931]=896;
assign LUT[932]=897;
assign LUT[933]=899;
assign LUT[934]=900;
assign LUT[935]=901;
assign LUT[936]=903;
assign LUT[937]=904;
assign LUT[938]=905;
assign LUT[939]=907;
assign LUT[940]=908;
assign LUT[941]=910;
assign LUT[942]=911;
assign LUT[943]=912;
assign LUT[944]=914;
assign LUT[945]=915;
assign LUT[946]=916;
assign LUT[947]=918;
assign LUT[948]=919;
assign LUT[949]=921;
assign LUT[950]=922;
assign LUT[951]=923;
assign LUT[952]=925;
assign LUT[953]=926;
assign LUT[954]=927;
assign LUT[955]=929;
assign LUT[956]=930;
assign LUT[957]=932;
assign LUT[958]=933;
assign LUT[959]=934;
assign LUT[960]=936;
assign LUT[961]=937;
assign LUT[962]=939;
assign LUT[963]=940;
assign LUT[964]=941;
assign LUT[965]=943;
assign LUT[966]=944;
assign LUT[967]=945;
assign LUT[968]=947;
assign LUT[969]=948;
assign LUT[970]=950;
assign LUT[971]=951;
assign LUT[972]=952;
assign LUT[973]=954;
assign LUT[974]=955;
assign LUT[975]=956;
assign LUT[976]=958;
assign LUT[977]=959;
assign LUT[978]=961;
assign LUT[979]=962;
assign LUT[980]=963;
assign LUT[981]=965;
assign LUT[982]=966;
assign LUT[983]=967;
assign LUT[984]=969;
assign LUT[985]=970;
assign LUT[986]=972;
assign LUT[987]=973;
assign LUT[988]=974;
assign LUT[989]=976;
assign LUT[990]=977;
assign LUT[991]=978;
assign LUT[992]=980;
assign LUT[993]=981;
assign LUT[994]=983;
assign LUT[995]=984;
assign LUT[996]=985;
assign LUT[997]=987;
assign LUT[998]=988;
assign LUT[999]=989;
assign LUT[1000]=991;
assign LUT[1001]=992;
assign LUT[1002]=994;
assign LUT[1003]=995;
assign LUT[1004]=996;
assign LUT[1005]=998;
assign LUT[1006]=999;
assign LUT[1007]=1000;
assign LUT[1008]=1002;
assign LUT[1009]=1003;
assign LUT[1010]=1005;
assign LUT[1011]=1006;
assign LUT[1012]=1007;
assign LUT[1013]=1009;
assign LUT[1014]=1010;
assign LUT[1015]=1011;
assign LUT[1016]=1013;
assign LUT[1017]=1014;
assign LUT[1018]=1016;
assign LUT[1019]=1017;
assign LUT[1020]=1018;
assign LUT[1021]=1020;
assign LUT[1022]=1021;
assign LUT[1023]=1023;

endmodule
